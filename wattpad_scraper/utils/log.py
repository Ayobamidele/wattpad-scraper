from os import environ
import json
from datetime import datetime

class Log:
    def __init__(self, name,**kwargs):
        self.name = name
        self.store = {"verbose":True,"show_time":True,"show_name":True}
        self.keys = ["verbose","show_time","show_name","time_color","name_color","override_verbose"]

        if kwargs:
            for key in kwargs:
                self[key] = kwargs[key]
        
        if name in environ:
            self.store = self._get_env(name)
        else:
            self._set_env(name,self.store)
        
        self.colors = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            'reset': '\033[0m'
        }
    
    def get_time(self):
        # time format is %Y-%m-%d %H:%M:%S AM/PM
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + ("AM" if datetime.now().hour < 12 else "PM")

    def show_verbose(self,val:bool):
        self.store['verbose'] = val
        self._set_env(self.name,self.store)
    
    def show_time(self,val:bool):
        self.store['show_time'] = val
        self._set_env(self.name,self.store)
    
    def show_name(self,val:bool):
        self.store['show_name'] = val
        self._set_env(self.name,self.store)
    
    def print(self,*args, **kwargs) -> None:
        """
        Prints the given arguments to the console.
        If the verbose flag is set to False, nothing will be printed.
        If the time flag is set to False, the time will not be printed.

        Arguments:
            args: The arguments to print.
            kwargs:
                color: The color to print the arguments in.
        """
        if "override_verbose" in self.store:
            if not self.store["override_verbose"]:
                return

        if self.store['verbose']:
            if "color" in kwargs:
                c = kwargs["color"]
                color = self.colors[c] if c in self.colors else self.colors["reset"]
                kwargs.pop("color")
            else:
                color = self.colors["reset"]

            if self.store['show_time'] or self.store['show_name']:
                print("[",end=" ")
            
            if self.store['show_time']:
                print(self.get_time(), end=" ")
            
            if self.store['show_name']:
                print(f"({self.name})", end=" ")
            
            if self.store['show_time'] or self.store['show_name']:
                print("]",end=" ")

            print(color,*args,self.colors["reset"],**kwargs)

    def debug(self,*args, **kwargs):
        self.print(*args, color="magenta", **kwargs)
    
    def error(self,*args, **kwargs):
        self.print(*args, color="red", **kwargs)
    
    def warning(self,*args, **kwargs):
        self.print(*args, color="yellow", **kwargs)
    
    def success(self,*args, **kwargs):
        self.print(*args, color="green", **kwargs)
    
    def info(self,*args, **kwargs):
        self.print(*args, color="cyan", **kwargs)

    def _set_env(self,key,value):
        environ[key] = json.dumps(value)
    
    def _get_env(self,key):
        return json.loads(environ[key])
    
    def __str__(self):
        return {
            "name":self.name,
            "verbose":self.store["verbose"],
            "show_time":self.store["show_time"],
        }
    
    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self,key):
        return self.store[key]
    
    def __setitem__(self,key,value):
        if key in self.keys:
            self.store[key] = value
            self._set_env(self.name,self.store)
        elif key.startswith("ver") or key.startswith("show"):
            self.store["verbose"] = value
            self._set_env(self.name,self.store)
        elif key.startswith("time"):
            self.store["show_time"] = value
            self._set_env(self.name,self.store)
        else:
            raise KeyError("Allowed keys are: "+str(self.keys))