# pyConfigFiles

## Purpose

The primary purpose of this library is to facilitate the creation of complex configuration files that cannot be efficiently or effectively described using conventional formats like CSV or JSON. While it retains the capability to manage simpler configurations, its design is specifically tailored for handling sophisticated setups, akin to those required in build systems. This makes it an ideal tool for developers who need to manage intricate configurations in their projects.

This library offers the flexibility to define configuration values that range from simple data types, like numbers and strings, to complex entities such as entire functions. This capability is particularly useful for scenarios where dynamic behavior is required as part of the configuration. For instance, consider the custom scripts in the .git/hooks directory, which are essentially bash scripts executed in response to specific git events. With our library, these could be seamlessly integrated into a single pyConfigFile, allowing for the writing of hook scripts directly in Python. This not only provides the convenience of maintaining configurations and executable scripts in one place but also leverages the full power of Python's extensive functionality for these injected functions, enabling more sophisticated and powerful configuration possibilities.



## Features

- Python Script Based Configuration: At the heart of this library is its ability to use ordinary Python scripts for defining configurations. This approach leverages the full power of Python, offering flexibility and expressiveness that static configuration files can't match.
- Familiar Environment: Python developers will find themselves in a familiar environment, allowing them to define configurations using the syntax and structures they are already comfortable with. This reduces the learning curve and enhances productivity.
- Debugging Capability: One of the significant advantages of using Python scripts for configuration is the ability to debug the configuration process. Developers can step through the configuration logic using their preferred Python debugger, making it easier to diagnose and fix issues.



## Getting Started with an Example

To begin using our library, you should first install it via PyPI using pip:

```bash
pip install pyConfigFiles
```

## Basic Example

Below is a basic example of how to use the library:

```python 
import pyConfigFiles as pcf

# Define your configuration class by inheriting from pcf.base
class MyConfiguration(pcf.base):
    def __init__(self) -> None:
        super().__init__()
        # Initialize configuration properties
        self.test = None

# Create an instance of your configuration class
obj = MyConfiguration()

# Add configuration modules, which are Python files that modify the configuration object's properties
obj.add_modules(["SomeConfiguration.py"])

# Display the value set by the configuration file to demonstrate how it modifies the class properties
print(obj.test)
```


In this example:

1. Import the Library: Begin by importing pyConfigFiles as pcf. This is the package that provides the base functionality for creating and managing configuration files.
1. Define a Configuration Class: Create a custom configuration class by extending pcf.base. This base class makes the structure of the configuration class itself immutable post-construction to prevent the addition of new properties, ensuring that only predefined properties are used.
1. Configurable Properties: While the structure of the configuration class is immutable, its members, such as self.test, are intended to be mutable and modifiable by the configuration script.
1. Load and Apply Configuration: The add_modules method loads external Python scripts that define the actual settings, modifying the properties of the obj instance according to the configuration logic contained in these scripts.
1. Demonstration: The print(obj.test) statement demonstrates that the test property of the configuration object has been successfully set or modified by the loaded configuration script.


This setup allows for a secure and structured approach to defining and modifying complex configurations, ensuring that the configuration's structure remains consistent while allowing for the flexibility needed to adjust its individual properties.

## Configuration File Example

The configuration file itself is a fully-featured Python script that utilizes the pyConfigFiles library, along with any other Python libraries needed for the configuration logic. In this example, we use the platform library to determine whether the operating system is Windows or Linux.

Example Configuration Script

```python
import pyConfigFiles as pcf 
import platform

@pcf.configuration
def MyWindowsConfiguration(obj):
    if platform.system() != 'Windows':
        return
   
    obj.test = "config_0:MyWindowsConfiguration: adding obj.test"

@pcf.configuration
def MyLinuxConfiguration(obj):
    if platform.system() != 'Linux':
        return
    
    obj.test1 = "config_0:MyLinuxConfiguration: adding obj.test1"

```

In this script:

- Importing Libraries: It starts with importing pyConfigFiles as pcf and the platform library.
- Using Decorators: The @pcf.configuration decorator is used to mark functions as entry points for the configuration process. These functions will be called by the pyConfigFiles library to modify the configuration object.
- Defining Entry Points: This example has two entry points: MyWindowsConfiguration and MyLinuxConfiguration, for Windows and Linux configurations, respectively.
- Conditional Logic: Each function first checks the operating system and returns immediately if the current OS does not match the intended target of the configuration function, ensuring that only the appropriate configuration is applied.
- Modifying the Configuration Object: The functions modify the obj parameter, which is an instance of the MyConfiguration class, by setting its properties based on the OS.
- Type Hint and Error Handling: If the configuration object definition (MyConfiguration) is accessible and properly defined, type hints help prevent and identify errors. For example, in the MyLinuxConfiguration function, there is a deliberate typo (test1 instead of test), illustrating how an error would be flagged, providing the developer with a full stack trace indicating the non-existent member.

## Handling Configuration Errors

In the provided configuration script, the typo in MyLinuxConfiguration (obj.test1 instead of obj.test) serves as an example of how errors are handled. Users on Linux would encounter an error message with a stack trace, clearly indicating that test1 is not a member of the MyConfiguration object, demonstrating the library's robust error detection and handling mechanisms.


## Extending Configuration with Additional Files
Our library supports the inclusion of additional configuration files from within a configuration file itself, allowing for modular and reusable configuration setups. This feature enables developers to structure complex configurations across multiple files for better organization and maintainability.

Including Additional Configuration Files
In the configuration script, you can include other configuration files using a method provided by pyConfigFiles. This allows for a hierarchical or modular configuration structure, where each part of the configuration can be separated into its own file.


```python 
@pcf.configuration
def includeOtherConfigurations(obj):
    obj.add_modules(["additional_config.py"])

```
In this example, additional_config.py would be another configuration file that gets included and executed as part of the configuration process.

The path for including additional configuration files is always relative to the location of the current configuration file being processed.


Prevention of Infinite Loops
To ensure robustness and prevent potential infinite loops, the library enforces a rule that each configuration file can be included only once. If a configuration file attempts to include a file that has already been processed, the subsequent inclusion will be ignored. This safeguard prevents infinite recursion and potential stack overflow errors, ensuring that the configuration process completes successfully.

By utilizing this feature, developers can create complex, layered configurations that are easy to manage and understand, while the built-in safeguards maintain the integrity and reliability of the configuration process.