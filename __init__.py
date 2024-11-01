# __init__.py

def classFactory(iface):
    from .Bacurbpara import BacurbparaPlugin
    return BacurbparaPlugin(iface)
