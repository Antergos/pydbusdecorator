# pydbusdecorator
### Decorators that make using dbus in Python applications much less annoying.


## Use It
#### Import decorators
```python
from dbusdecorator import DBusAttribute, DBusInterface, DBusMethod
```
#### Define a dbus interface
```python
@DBusInterface('com.antergos.cnchi', '/com/antergos/cnchi')
class Installer:

    @DBusMethod
    def select_desktop(self, desktop):
        pass
    
    @DBusAttribute
    def packages(self): 
        pass

```
#### Use your definition
```python
cnchi = Installer(dbus_interface_info={'dbus_uri': 'com.antergos.cnchi'})
 
cnchi.select_desktop('gnome')
print(cnchi.packages)
cnchi.packages = []

```
