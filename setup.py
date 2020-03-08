from setuptools import setup, find_packages

def get_reqs(file_path):
    from pip._internal.req import parse_requirements

    def clear_titles(title):
        import re
        return re.sub('[\t\r\n]', '', title).strip()

    reqs = open(file_path).read().replace('\n\r', '\n').split('\n')
    req = list(parse_requirements(file_path, session='hack'))

    ans = []

    minus_idx = 0

    for idx, el in enumerate(reqs):

        el = clear_titles(el)
        if len(el) < 1 or (len(el) > 0 and el[0] == '#'):
            minus_idx += 1
            continue

        egg = False

        try:
            eqq_idx = el.rindex('#egg=') + 5
            final_idx = eqq_idx
            egg = True
        except ValueError:
            eqq_idx = -1

        if not egg:

            if req[idx - minus_idx].name:
                ans.append(el)
                continue

            try:
                rsidx = el.rindex('/') + 1
            except ValueError:
                rsidx = -1
            try:
                lsidx = el.rindex('\\') + 1
            except ValueError:
                lsidx = -1
            final_idx = max(rsidx, lsidx)
        name = el[final_idx:]

        ans.append(name + ' @ ' + el)
    return ans

setup(
    name="utasker_core",
    version='0.0.1',
    description="Tasks controller for you team!",
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3'  ,
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='team task tasks control controller work universal',
    author='Hacker',
    author_email='bulat.shaekhov@gmail.com',
    url='https://github.com/IHackerI/utasker_core',
    packages=find_packages(),
    install_requires=#['pymysql']
        get_reqs('requirements.txt')
        #open('requirements.txt').read().split('\n\r|\n')
    ,
    #dependency_links=['https://github.com/IHackerI/time_tools'],
    include_package_data=True,
    zip_safe=False,
)