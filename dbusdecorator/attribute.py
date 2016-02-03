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


class DBusAttribute(Decorator):
    """
    https://docs.python.org/2/howto/descriptor.html#properties
    """

    def __init__(self, meth=None, produces=lambda resp: resp):
        self.attr = meth
        self.produces = produces
        self._update_me(meth)

    def __call__(self, meth):
        self.attr = meth
        self._update_me(meth)
        return self

    def __get__(self, obj, objtype=None):
        # static call
        if not obj:
            return self

        _dbus = getattr(obj, ATTR_KEY)
        props = _dbus.properties
        iface = _dbus.iface
        result = props.Get(iface, self.attr.__name__)
        produces = self.produces
        return produces(result)

    def __set__(self, obj, value):
        if obj:
            _dbus = getattr(obj, ATTR_KEY)
            props = _dbus.properties
            iface = _dbus.iface
            props.Set(iface, self.attr.__name__, value)
        else:  # static call
            self.attr = value

    def __delete__(self, obj):
        raise AttributeError('can not delete attribute')


if __name__ == '__main__':
    # examples
    from .interface import DBusInterface


    @DBusInterface('org.mpris.MediaPlayer2',
                   '/org/mpris/MediaPlayer2')
    class Example(object):
        @DBusAttribute
        def Identity(self):
            pass


    d = Example(
        dbus_interface_info={
            'dbus_uri': 'org.mpris.MediaPlayer2.vlc'})

    assert d.Identity == 'VLC media player'
