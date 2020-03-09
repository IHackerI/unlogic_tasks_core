import pymysql  # require PyMySQL in requirements.txt
import json
import os

import __main__
full_path = os.path.dirname(os.path.abspath(__main__.__file__))

db_settings_file_name = 'db_settings.json'

try:
    file = open(full_path + os.sep + db_settings_file_name, 'r')
except:
    raise Exception('I don\'t read database settings file! file path: ' + full_path + '\\' + db_settings_file_name + '\n' + 
                    'file content structure: {"utasks_core": {"NAME": "unlogic_controller", "USER": "root", "PASSWORD": "qweqwe123", "HOST": "127.0.0.1"}}')

DATABASES = json.loads(file.read())

file.close()

id_field_name = "id"
db_address = DATABASES['utasks_core']['HOST']
db_user = DATABASES['utasks_core']['USER']
db_password = DATABASES['utasks_core']['PASSWORD']
db_name = DATABASES['utasks_core']['NAME']


def build_header_and_data(header, data):
    building_row = {}
    for idx, columnName in enumerate(header):
        building_row[columnName] = data[idx]
    return building_row


class MySQLDatabase:
    #instances = []

    def __init__(self, address, user, password, loc_db_name):
        self.conn = pymysql.connect(address, user, password, loc_db_name)
        self.cursor = self.conn.cursor()
        self.dbName = loc_db_name
        #MySQLDatabase.instances.append(self)

    def table_exist(self, table_name):
        # print("SHOW TABLES")
        self.cursor.execute("SHOW TABLES")
        all_tables = self.cursor.fetchall()

        for table in all_tables:
            if table[0].lower() == table_name.lower():
                return True
        return False

    def convert_column_type(self, column_type):
        if column_type == int:
            return 'INT'
        if column_type == str:
            return 'TEXT'
        if column_type == bool:
            return 'BOOLEAN DEFAULT 0 NOT'

        raise NotImplementedError('type: ' + str(column_type))

    def create_table(self, table_name, columns, pk):

        query = 'CREATE TABLE `' + self.dbName + '`.`' + table_name + '` ( ' + '`' + pk + \
                '` INT NOT NULL AUTO_INCREMENT '

        for column_num in columns:
            query += ', `' + column_num + '` '
            query += self.convert_column_type(columns[column_num])
            query += ' NULL '

        query += ', PRIMARY KEY (`' + pk + '`) ) ENGINE = InnoDB;'

        # print(query)
        self.cursor.execute(query)
        self.conn.commit()

        # CREATE TABLE `video_poster`.`testTable` ( `id` INT NOT NULL AUTO_INCREMENT , `testColumn` TEXT NULL ,
        # PRIMARY KEY (`id`)) ENGINE = InnoDB;

    def get_table_columns(self, table_name, only_names=True):
        ans = self.exec("SHOW COLUMNS FROM `" + table_name + "`")

        if only_names:
            sans = []
            for column in ans[1]:
                sans.append(column[0])
            ans = sans

        return ans

    def add_table_columns(self, table_name, columns):

        query = "ALTER TABLE `" + table_name + "` "

        first_col = True

        for key in columns.keys():
            query += (", " if not first_col else "") + "ADD COLUMN `" + key + "` " + self.convert_column_type(
                columns[key]) + " NULL"
            first_col = False

        self.exec(query)

    def add_data(self, table_name, data, pk):
        if not self.table_exist(table_name):
            columns = {}
            for dataKey in data:
                columns[dataKey] = type(data[dataKey])
            self.create_table(table_name, columns, pk)

        query = 'INSERT INTO `' + table_name + '` ( `' + pk + '` '

        for data_key in data:
            query += ', `' + data_key + '` '

        query += ') VALUES (NULL'

        for data_key in data:
            if type(data[data_key]) == bool:
                query += ", '" + str(1 if data[data_key] else 0) + "' "
            else:
                query += ", '" + pymysql.escape_string(str(data[data_key])) + "' "

        query += ')'

        # print(query)
        self.cursor.execute(query)
        self.conn.commit()

        return self.exec("SELECT LAST_INSERT_ID();")[1][0]

        # INSERT INTO `autotestTable` (`id`, `testCol`, `testIntCol`) VALUES (NULL, 'kbmbmnbmnmnb', '3')
        # print('addData')

    def upd_data(self, table_name, data, pk):

        query = 'UPDATE `' + table_name + '` SET '

        first = True

        for data_key in data:
            if not first:
                query += ', '
            first = False
            if type(data[data_key]) == bool:
                query += '`' + data_key + "` = '" + str(1 if data[data_key] else 0) + "' "
            else:
                query += '`' + data_key + "` = '" + pymysql.escape_string(str(data[data_key])) + "' "

        query += ' WHERE `' + table_name + '`.`' + pk + '` = ' + str(data[pk])

        # print(query)
        self.cursor.execute(query)
        self.conn.commit()

        # UPDATE `autotestTable` SET `testCol` = 'kbmbmnbfff' WHERE `autotestTable`.`id` = 1
        # print('upd')

    def get_all_rows(self, table_name):
        if not self.table_exist(table_name):
            return None

        query = 'SELECT * FROM `' + table_name + '`'

        return self.exec(query)

    def get_rows_where(self, table_name, logic):

        # TODO fix SQL injection!

        if not self.table_exist(table_name):
            return None

        query = 'SELECT * FROM `' + table_name + '` WHERE ' + str(logic)

        return self.exec(query)

    def delete_row(self, table_name, pk, pk_value):
        if not self.table_exist(table_name):
            return

        query = 'DELETE FROM `' + table_name + '` WHERE `' + table_name + '`.`' + pk + '` = ' + str(pk_value)

        # print(query)
        self.cursor.execute(query)
        self.conn.commit()

        # "DELETE FROM `autotestTable` WHERE `autotestTable`.`ololid` = 1"

    def exec(self, sql):
        # print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
        ret = self.cursor.fetchall()

        header = []

        if not (self.cursor.description is None):
            for descTuple in self.cursor.description:
                header.append(descTuple[0])

        return header, ret


def get_db_worker_instance() -> MySQLDatabase:
    #if len(MySQLDatabase.instances) < 1:
    #    MySQLDatabase(db_address, db_user, db_password, db_name)
    return MySQLDatabase(db_address, db_user, db_password, db_name)  # MySQLDatabase.instances[0]

#def close_all_connections():
#
#    cur_inst = MySQLDatabase.instances
#    MySQLDatabase.instances = []
#
#    for instance in cur_inst:
#        try:
#            instance.cursor.close()
#        except:
#            print('don\'t close cursor')
#        try:
#            instance.conn.close()
#        except:
#            print('don\'t close conn')

# if __name__ == '__main__':

# db = MySQLDatabase('db4free.net', 'nyry64m2', 'Y8rGrWfE', 'video_poster')

# if not db.table_exist('autotestTable'):
#     db.create_table('autotestTable', {'testColumn': str, 'intTestColumn': int}, pk='ololid')

# db.add_data('autotestTable', {'testColumn': 'forView', 'intTestColumn': 5}, pk='ololid')

# rows = db.get_all_rows('autotestTable')

# buildedRow = db.buildHeaderAndData(rows[0], rows[1][0])

# buildedRow['testCol'] = 'ChangedWithUpdate'

# db.updData('autotestTable', buildedRow, pk='ololid')

# db.deleteRow('autotestTable', 'ololid', rows[1][len(rows[1])-3][0])

# all = db.exec('Select * from autotestTable')

# print (all)
