Initialization
==============

## Introduction

The first steps when working with the API consist of detecting and initializing the hardware.  
During hardware detection, the device engine searches for connected idSMU hardware. If this is found, a hardware model is created. This model has already been briefly described in the introductory chapters.  
However, detection of the hardware is not sufficient to communicate with the hardware. In a second step, the hardware must be initialized: In this step, for example, all default register values are set, the necessary power supply for the SMU/DPS chips is set and calibration data is read from a memory.  

## IdSmuService

The IdSmuService is the class that takes over the task of device detection and triggers the construction of the hardware model for each idSMU board found. This service class stores a reference to each board model and the user can then access it.  

## IdSmuServiceRunner

The IdSmuServiceRunner class encapsulates the rather complicated construction and lifetime management of the IdSmuService object.    
The API user therefore has the option of instantiating this object instead. It is recommended to instantiate the IdSmuService via this object.  
As soon as the IdSmuServiceRunner goes out of scope, it ensures that all necessary connections to the hardware are automatically closed cleanly.  
When using the IdSmuService alone, the user would be responsible for this clean-up work. If this is forgotten, the software cannot be restarted without restarting the hardware.

 ```Python
    srunner = IdSmuServiceRunner()
    idsmu_service = srunner.get_idsmu_service()
 ```

## Device detection

:::{note}
Normally, the 'detection' and 'initialization' steps can be combined. Nevertheless, the individual steps are briefly described here.
:::

The `detect_devices()` method of IdSmuService can be used to trigger the device detection. 
This method returns a CommandReply object. This is an object which, if devices were detected, contains a list of idSMU devices found.  
If desired, the user can examine this object very quickly with his ‘to_json’ method.
However, as the IdSmuService automatically creates a hardware model when hardware is found, the user has the option of accessing this directly.  
After detection, some information can be retrieved:  
With `get_board_addresses()` a list of all board addresses is returned. The `print_device_information()` returns a string table displaying some usefull information about the detected hardware.  

## Device initialization

Initialization takes place for all idSMU devices on a board (remember: a board is the container for one or more idSMU devices).  
Once the hardware has been detected, this board can be initialized using the board address.

Example initializing a board with the address 'M1':
```Python
   idsmu_service.initialize_board('M1')
```
Similar to the `detect_devices()` method, this method returns the result of this process. This time it returns a list of CommandReply objects,
one entry for each idSMU device that has been initialized.  

Full example detection and initialization:
```Python
   smu_service = srunner.get_idsmu_service()
   # detection
   smu_service.detect_devices()
   print(smu_service.print_device_information())
   # initialization
   print(smu_service.initialize_board('M1')[0].to_json())
   # since the CommandReply content is quite verbose, 
   # we check the status of the device with the print_device_information again
   print(smu_service.print_device_information())
```
## Combining detection and initialization

Separate detection and initialization is rarely necessary (e.g. for special power settings).  
It is therefore possible to combine both steps in one.  
The method `detect_and_initialize_devices()` does what the name says: It detects the hardware and then initializes it.   
The method `get_first_board()` is very similar with the difference that it returns the first detected and initialized board. This is particularly useful for single module boards.

Full example detection and initialization:
```Python
   smu_service = srunner.get_idsmu_service()
   myboard = smu_service.get_first_board()
```

## Shutdown / deinitialization

The method `shutdown_devices()` does the opposite of initialization.
It can be used in combination with another initialization to reset the devices to their initial state.

## Summary: Methods for device detection and initialization 

IdSmuService methods:

| Method                            | Explenation                                                              |
| :-------------------------------- | :----------------------------------------------------------------------- |
| detect_devices()                  | detects all connected idSmu devices<br>and builds a hardware model       |
| get_board_addresses()             | returns a list of all board addresses of <br>the detected hardware       |
| print_device_information()        | returns a formatted string table<br>containing useful device information |
| initialize_board(<board_address>) | Initializes a board (the devices on it)                                  |
| detect_and_initialize_devices()   | Detects and initializes all devices                                      |
| get_first_board()                 | Detects and initializes all devices<br>and returns the first board       |
| shutdown_devices()                | Shutdown & Deinitialization of all devices                               |




