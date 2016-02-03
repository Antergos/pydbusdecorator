#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#  setup.py
#
#  Copyright © 2016 Antergos
#  Copyright © 2011-2016 Hugo Sena Ribeiro
#
#  This file is part of pydbusdecorator.
#
#  pydbusdecorator is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  pydbusdecorator is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  The following additional terms are in effect as per Section 7 of the license:
#
#  The preservation of all legal notices and author attributions in
#  the material or in the Appropriate Legal Notices displayed
#  by works containing it is required.
#
#  You should have received a copy of the GNU General Public License
#  along with pydbusdecorator; If not, see <http://www.gnu.org/licenses/>.


from distutils.core import setup
import dbus

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(name='pydbusdecorator',
      version='2.0',
      description='Python decorator for dbus interface clients',
      author='Antergos Developers',
      author_email='dev@antergos.com',
      url='https://github.com/antergos/pydbusdecorator',
      keywords=["dbus"],
      packages=('dbusdecorator',),
      requires=(),
      license="GPL",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5"
      ],
      long_description=readme
      )
