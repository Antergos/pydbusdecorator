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


class DBusSignal(Decorator):
    """
    https://docs.python.org/2/howto/descriptor.html#properties
    """

    def __init__(self, meth=None, iface=None):
        self.attr = meth
        self.handler = None
        self.iface = iface
        self._update_me(meth)

    def __call__(self, meth):
        self.attr = meth
        self._update_me(meth)
        return self

    def __get__(self, obj, objtype=None):
        if obj:
            return self.handler

        # static call
        return self

    def __set__(self, obj, value):
        if obj:
            _dbus = getattr(obj, ATTR_KEY)
            interface = _dbus.interface

            def handle(*args, **kwds):
                h = self.handler
                h and h(*args, **kwds)

            if not self.handler:
                interface.connect_to_signal(self.attr.__name__, handle,
                                            dbus_interface=self.iface)
            self.handler = value
        else:  # static call
            self.attr = value

    def __delete__(self, obj):
        self.handler = None


if __name__ == '__main__':
    from .interface import DBusInterface
    from .utils import get_mainloop

    mainloop = get_mainloop()
    print('mainloop', mainloop)


    @DBusInterface('org.mpris.MediaPlayer2.player',
                   '/org/mpris/MediaPlayer2')
    class Example(object):
        @DBusSignal
        def Seeked(self):
            pass


    d = Example(
        dbus_interface_info={
            'dbus_uri': 'org.mpris.MediaPlayer2.gmusicbrowser'})


    def handler(self, *args):
        print(args)


    d.Seeked = handler
    mainloop and mainloop.run()
