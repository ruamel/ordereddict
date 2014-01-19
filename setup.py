#! /usr/bin/env python
# coding: utf-8

import sys
import os
from textwrap import dedent

name_space = 'ruamel'
package_name = 'ordereddict'
full_package_name = name_space + '.' + package_name

exclude_files = [
    'setup.py',
]

if __name__ == '__main__':
    # put here so setup.py can be imported more easily
    from setuptools import setup, find_packages, Extension
    from setuptools.command import install_lib

    module1 = Extension('_ordereddict',
                        sources = ['ordereddict.c',],
                       )

version = [0, 4, 6]
version_str = '.'.join([str(x) for x in version])

class MyInstallLib(install_lib.install_lib):
    "create __init__.py on the fly"
    def run(self):
        install_lib.install_lib.run(self)
        init_txt = dedent('''\
            # coding: utf-8
            # Copyright © 2013 Anthon van der Neut, RUAMEL bvba
            "generated __init__.py "
            try:
                __import__('pkg_resources').declare_namespace(__name__)
            except ImportError:
                pass
        ''')
        init_path = full_package_name.split('.')[:-1]
        for product_init in [
            os.path.join(
                *([self.install_dir] + init_path[:p+1] + ['__init__.py']))
                for p in range(len(init_path))
        ]:
            if not os.path.exists(product_init):
                print('creating %s' % product_init)
                with open(product_init, "w") as fp:
                    fp.write(init_txt)
        setup = os.path.join(self.install_dir, 'setup.py')
        print '>' * 72
        print 'setup', os.path.exists(setup), setup

    def install(self):
        fpp = full_package_name.split('.')  # full package path
        full_exclude_files = [os.path.join(*(fpp + [x]))
                         for x in exclude_files]
        alt_files = []
        outfiles = install_lib.install_lib.install(self)
        #print '<' * 60, '\n', outfiles
        for x in outfiles:
            for full_exclude_file in full_exclude_files:
                if full_exclude_file in x:
                    os.remove(x)
                    break
            else:
                alt_files.append(x)
        print '<' * 60
        for x in alt_files:
            print '   ', x.split('site-packages/')[-1]

        return alt_files


long_description = """
A derivation of the pyton dictobject.c module that implements
Key Insertion Order (KIO: the insertion order of
new keys is being tracked, updating values of existing keys does not
change the order), Key Value Insertion Order (KVIO: KIO, but updates change
order), and Key Sorted Order (KSO: key are kept sorted).

The basic C structure is exented with a pointer to a list of item pointers.
When a *new* key is added, this list is extended with a pointer to the item.
The implementation compacts the list of pointers on every deletion (unless
the last added key is removed, such as in popitem()). That
involves a memmove of all the pointers behind the pointer to the item in
question.

The .keys, .values, .items, .iterkeys, itervalues, iteritems, __iter__
return things in the order of insertion.

.popitem takes an optional argument (defaulting to -1), which is the
order of the item.

the representation of the ordereddict is the same with Larosa/Foord:
"ordereddict([(key1, val1), (key2, val2)])"

support for slices

And some more (see README.rst).
"""


def main():
    install_requires = [
        ]
    packages = [full_package_name] + [(full_package_name + '.' + x) for x
                                     in find_packages(exclude=['tests'])]

    setup(
        name=full_package_name,
        version=version_str,
        description='a version of dict that keeps keys in '\
                    'insertion resp. sorted order',
        install_requires=[
        ],
        #install_requires=install_requires,
        long_description=open('README.rst').read(),
        url='https://bitbucket.org/ruamel/' + package_name,
        author='Anthon van der Neut',
        author_email='a.van.der.neut@ruamel.eu',
        license="MIT license",
        package_dir={full_package_name: '.'},
        namespace_packages=[name_space],
        packages=packages,
        ext_modules = [module1],
        cmdclass={'install_lib': MyInstallLib},
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
        ],
    )


def mainX():
    setup (name = 'ordereddict',
           version = version_str,
           description = 'a version of dict that keeps keys in '\
                         'insertion resp. sorted order',
           author = 'Anthon van der Neut',
           author_email = 'anthon@mnt.org',
           url = 'http://www.xs4all.nl/~anthon/ordereddict',
           long_description = long_description,
           ext_modules = [module1],
          )

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'sdist':
        assert full_package_name == os.path.abspath(os.path.dirname(
            __file__)).split('site-packages' + os.path.sep)[1].replace(
                os.path.sep, '.')
    main()
#if __name__ == '__main__':
#    main()
