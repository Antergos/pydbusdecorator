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


from .base import Decorator, ATTR_KEY


def kw_to_dbus(**kw):
    return kw


def args_to_dbus(*args):
    return args


class DBusMethod(Decorator):
    def __init__(self, meth=None,
                 iface=None,
                 produces=lambda resp: resp,
                 args_to_dbus=args_to_dbus,
                 kw_to_dbus=kw_to_dbus):
        self.meth = meth
        self.handler = None
        self.produces = produces
        self.iface = iface
        self.args_to_dbus = args_to_dbus
        self.kw_to_dbus = kw_to_dbus
        self.obj = None
        self._update_me(meth)

    def __call__(self, meth=None):
        self.meth = meth
        self._update_me(meth)
        return self

    def __get__(self, obj=None, cls=None):
        if obj is None:
            return self
        self.obj = obj
        return self._call_dbus

    def _call_dbus(self, *args, **kwds):
        _dbus = getattr(self.obj, ATTR_KEY)
        if self.iface:
            iface = self.iface
        else:
            iface = _dbus.iface
        bus_obj = _dbus.object
        bus_meth = bus_obj.get_dbus_method(self.meth.__name__, iface)
        args = self.convert_args_to_dbus_args(*args)
        kwds = self.convert_kw_to_dbus_kw(**kwds)
        result = bus_meth(*args, **kwds)
        return self.produces(result)

    def convert_args_to_dbus_args(self, *args):
        args_to_dbus = self.args_to_dbus
        if callable(args_to_dbus):
            return args_to_dbus(*args)

        # iterate over args
        result = []
        for arg in args:
            i = args.index(arg)
            if i < len(args_to_dbus):
                make = args_to_dbus[i]
                if callable(make):
                    arg = make(arg)
            result.append(arg)
        return tuple(result)

    def convert_kw_to_dbus_kw(self, **kw):
        kw_to_dbus = self.kw_to_dbus
        if callable(kw_to_dbus):
            return kw_to_dbus(**kw)

        if hasattr(self.kw_to_dbus, 'keys'):
            for key, val in kw.items():
                make = kw_to_dbus.get(key, lambda v: v)
                kw[key] = make(val)
        return kw


if __name__ == '__main__':
    # examples
    from .interface import DBusInterface


    @DBusInterface('org.freedesktop.DBus', '/')
    class Example:
        @DBusMethod
        def GetId(self):
            pass

        @DBusMethod
        def GetNameOwner(self, name):
            pass


    d = Example(
        dbus_interface_info={
            'dbus_uri': 'org.freedesktop.DBus'})

    assert d.GetId()
    assert d.GetNameOwner('org.freedesktop.DBus') == 'org.freedesktop.DBus'
