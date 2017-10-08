#!/usr/bin/python
# -*- coding: utf-8 -*-

VERSION = '0.3'

from distutils.core import setup

modules = ['pyllist.dllist',
           'pyllist.sllist',
           'pyllist.compat'
          ]

setup(name='pyllist',
      description='Linked list data structures (in pure Python)',
      long_description=open('README').read(),
      author=u'Rafał Gałczyński <rafal.galczynski@gmail.com>, '
             u'Adam Jakubek <ajakubek@gmail.com>, '
             u'Oleksandr Pryymak',
      version=VERSION,
      url='https://github.com/rgsoda/pypy-llist',
      download_url='http://pypi.python.org/pypi/pyllist/%s' % VERSION,
      license='MIT',
      keywords='linked list, list',
      py_modules=modules,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      )
