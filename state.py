from typing import Any
class UIstate:
    focused = False
class Design:
    thick = 200
    grid = False
    gridstyle = (0,0,0,.2)
    gridwidth = 1
    placedebug = False
    true_dupe = False
    hub = False
class UsefulMod:
    def __init__(self):
        self.warn = False
        # Do not modify directly. Call self.enable or self.disable.
        self.enabled = False
        self.purge = False
    def enable(self, floor_types, state=True):
        self.enabled = state
        if state:
            for tag in ["Buttont", "PlayerButtont"]:
                if tag not in floor_types:
                    floor_types.append(tag)
        else:
            for tag in ["Buttont", "PlayerButtont"]:
                floor_types.remove(tag)
    def disable(self, floor_types, state=True):
        self.enabled = not state
        if state:
            for tag in ["Buttont", "PlayerButtont"]:
                floor_types.remove(tag)
        else:
            for tag in ["Buttont", "PlayerButtont"]:
                if tag not in floor_types:
                    floor_types.append(tag)
"""
class _FrameDebug(dict):
    def __init__(self):
        dict.__init__(self)
        self._print = []
    def ensure(self, __name: str, default: Any=None) -> None:
        if not (__name in self): 
            self[__name] = default
    def __getattr__(self, __name: str) -> None:
        return self[__name]
    def __setattr__(self, __name: str, __value: Any) -> None:
        self[__name] = __value
    def print(self,code):
        self._print.append(str(code))
    def printload(self):
        ret = '\n'.join(self._print)
        self._print = []
        return(ret)
FrameDebug=_FrameDebug()
"""
usefulmod = UsefulMod()
