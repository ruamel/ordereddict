#! /usr/bin/env python
# coding: utf-8

from __future__ import with_statement

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

# < from ruamel.util.new.setupinc import get_version, _check_convert_version
def get_version():
    v_i = 'version_info = '
    for line in open('__init__.py'):
        if not line.startswith(v_i):
            continue
        s_e = line[len(v_i):].strip()[1:-1].split(', ')
        elems = [x.strip()[1:-1] if x[0] in '\'"' else int(x) for x in s_e]
        break
    return elems


def _check_convert_version(tup):
    """create a PEP 386 pseudo-format conformant string from tuple tup"""
    ret_val = str(tup[0])  # first is always digit
    next_sep = "."  # separator for next extension, can be "" or "."
    nr_digits = 0  # nr of adjacent digits in rest, to verify
    post_dev = False  # are we processig post/dev
    for x in tup[1:]:
        if isinstance(x, int):
            nr_digits += 1
            if nr_digits > 2:
                raise ValueError("too many consecutive digits " + ret_val)
            ret_val += next_sep + str(x)
            next_sep = '.'
            continue
        first_letter = x[0].lower()
        next_sep = ''
        if first_letter in 'abcr':
            if post_dev:
                raise ValueError("release level specified after "
                                 "post/dev:" + x)
            nr_digits = 0
            ret_val += 'rc' if first_letter == 'r' else first_letter
        elif first_letter in 'pd':
            nr_digits = 1  # only one can follow
            post_dev = True
            ret_val += '.post' if first_letter == 'p' else '.dev'
        else:
            raise ValueError('First letter of "' + x + '" not recognised')
    return ret_val


# < from ruamel.util.new.setupinc import version_info, version_str
version_info = get_version()
version_str = _check_convert_version(version_info)
# < from ruamel.util.new.setupinc import MyInstallLib
class MyInstallLib(install_lib.install_lib):
    def run(self):
        install_lib.install_lib.run(self)

    def install(self):
        fpp = full_package_name.split('.')  # full package path
        full_exclude_files = [os.path.join(*(fpp + [x]))
                              for x in exclude_files]
        alt_files = []
        outfiles = install_lib.install_lib.install(self)
        for x in outfiles:
            for full_exclude_file in full_exclude_files:
                if full_exclude_file in x:
                    os.remove(x)
                    break
            else:
                alt_files.append(x)
        return alt_files


# <

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
    install_requires = []
    packages = [full_package_name] + [(full_package_name + '.' + x) for x
                                     in find_packages(exclude=['tests'])]

    setup(
        name=full_package_name,
        version=version_str,
        description='a version of dict that keeps keys in '\
                    'insertion resp. sorted order',
        install_requires=install_requires,
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
            'Development Status :: 5 - Production/Stable',
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
    if os.name != 'nt' and len(sys.argv) > 1 and sys.argv[1] == 'sdist':
        assert full_package_name == os.path.abspath(os.path.dirname(
            __file__)).split('site-packages' + os.path.sep)[1].replace(
                os.path.sep, '.')
    main()
#if __name__ == '__main__':
#    main()
