import importlib.util
import sys
import base64
import inspect
import os


import hashlib

def calculate_hash(file_path):
    hash_algo = hashlib.sha256()  # You can use other algorithms like SHA-1, MD5, etc.
    with open(file_path, 'rb') as file:
        # Read the file in chunks to avoid memory issues with large files
        for chunk in iter(lambda: file.read(4096), b''):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()


l = []

def add_function(name, function):
    l.append(function)
    

def configuration(func):
    # Get the frame object for the caller of the decorated function
    caller_frame = inspect.currentframe().f_back
    # Extract the filename from the frame object
    filename = caller_frame.f_globals['__file__']
    
    # Print or use the encoded filename as needed
    add_function(filename, func)
    
    return func





def import_from_filepath(filepath):
    l.clear()
    # Extract module name from filepath
    module_name = filepath.split('/')[-1].split('.')[0]
   
    # Create a module spec from the filepath
    spec = importlib.util.spec_from_file_location(module_name, filepath)
   
    # Create a new module based on the spec
    module = importlib.util.module_from_spec(spec)
   
    # Add the module to sys.modules
    sys.modules[module_name] = module
   
    # Execute the module (run its code)
    spec.loader.exec_module(module)
    ret = l.copy()
    l.clear()
    return ret



class LockAttributesMeta(type):
    def __call__(cls, *args, **kwargs):
        # Create the instance using the default mechanism
        instance = super().__call__(*args, **kwargs)
        # After the instance is created and initialized, set the flag to lock attribute additions
        instance._locked = True
        return instance
    




class base(metaclass=LockAttributesMeta):
    def __init__(self) -> None:
        self.__files__ = []

    def __setattr__(self, key, value):
        if getattr(self, '_locked', False) and not hasattr(self, key):
            raise AttributeError(f"Cannot add new attribute '{key}' to instances of {self.__class__.__name__}")
        super().__setattr__(key, value)

    def add_modules(self, files):
        fs = {}
        caller_frame = inspect.currentframe().f_back
        # Extract the file path from the frame
        file_path = caller_frame.f_code.co_filename
        
        directory_path = os.path.dirname(file_path)

        for f in files:

            new_path = os.path.join(directory_path, f)
            file_hash =  calculate_hash(new_path) 
            if file_hash in  self.__files__: 
                continue
            fs[new_path] =  import_from_filepath(new_path)
            self.__files__.append(file_hash)


        for file in fs.keys():
            for fun in fs[file]:
                fun(self)

        
         


