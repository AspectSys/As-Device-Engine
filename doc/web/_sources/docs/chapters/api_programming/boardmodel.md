The Board Model
===============

## Introduction

The central elements of the API are the classes that model the idSMU hardware.  
This model basically has two tasks: It stores the __state__ of the hardware and it provides simplified access to the __command interface__ that is used to communicate with the hardware.  
The model is a mixture of composition and inheritance.  
The board model is at the top level. This is represented in the API via the `IdSmuBoardModel` class. As already shown in the [introductory overview](intro-hardware-model), this model is the container class for the underlying components.  
The IdSmuBoardModel class is not instantiated directly by the user. The entire hardware model is built by the IdSmuService during [hardware detection](device-detection). Access to these objects is then obtained via the `IdSmuService`.  
An IdSmuBoardModel contains one or more `IdSmuModel`s. An IdSmuModel represents a single idSMU hardware module. This in turn contains an SMU chip, represented by the `AnalogueDeviceModel`.  
Most of the parameterisation and state storage ultimately takes place in the AnalogChannelModel.  
Another central paradigm of the idSmuBoardModel is the possibility of highly parallel (multiside) programming of the hardware. For this purpose, the board model manages a reference to all channels. This means that parameterisation and measurements can be carried out on several or dozens of channels in parallel.  
This high level of scalability means that the user can work with individual modules at channel level as well as with many modules in parallel at board level.

:::{figure-md} classdiag-fig
<img src="/_assets/api_programming/classdiag.png" alt="classdiag" width="600px">

Simplified class diagram of hardware model
:::

## Addressing & Identifier Scheme

The model components Board, SmuModel/Module and Channel presented above can each be addressed by unique identifiers in the API.  
When initialising the hardware, the firmware of an idSmu module determines its own unique address. As this address is unique in a network of idSMU modules, it is also referred to as the identifier.  
The firmware uses special address pins on the hardware interface to determine this address. 
The structure of this identifier is divided into three parts and follows the hardware hierarchy: board address, module address, channel address.
The board address can be set by the user and is *M1* by default. The module address (or slot address) is defined by the position of a module on a board. For a single module board, this is *S1* by default. The channel address results from the logical numbering of the channels of a module and has the format *Cz*, where 'z' is a channel number starting from 1.  
The itentifier is a string composed of these three parts and has the format Mx.Sy.Cz.  
The identifier (or resource address) is a string made up of these three parts and has the format Mx.Sy.Cz for a channel, Mx.Sy for a module and Mx for a board.   Many of the API functions expect this identifier as an input parameter. As an example: The `set_voltages` method of the board model expects a list of channel IDs in addition to the voltage value: 
```Python
   myboard.set_voltages(2.5, ['M1.S1.C1', 'M1.S1.C2'])
```

## Programming via board model vs channel model

As a user of the API, you can choose whether to set the parameters (and measurements) on channel objects or via the board model.
Configuration via the channel model is somewhat more intuitive and can be done (in Python) via properties.  
The same functionality can be achieved in the board model via class methods.  
If you want high parallelism (multiside), the user must use these methods.

## Accessing a board model

An IdSmuBoardModel can be accessed via the IdSmuService.  
There are basically 2 methods for this: `get_first_board()`and `get_board(<board_address>)`.  
The first of these methods,`get_first_board()`, takes over the detection and initialisation of the hardware, if not already done, and returns the first detected board.  
The second method, `get_board(<board_address>)`, assumes that a board with the address *'board_address'* has already been detected. 

## Obtaining information about the board and administrative methods

:::{note}
In the context of the IdSmuBoardModel, an idSmu module or its model IdSmuModel is usually referred to as a *device*.
:::

As soon as you have received an IdSmuBoard model instance via the IdSmuService, you can query some useful information about the board.  
In addition, alias names can be assigned to channels and modules/devices.
Below is a list of these methods:

| Method                                                      | Comment                                                                           |
| :---------------------------------------------------------- | :-------------------------------------------------------------------------------- |
| get_address()                                               | Returns the board address in the format Mx                                        |
| get_all_hardware_ids()                                      | Returns a list of all device/module and channel<br>IDs                            |
| get_number_of_devices()                                     | Returns the number of devices (idSMU Modules)<br>detected on this board           |
| is_board_initialized()                                      | Returns true if all devices on this board are<br>initialized                      |
| print_device_information()<br>(device_information property) | Prints and returns tabular information about<br>the deteced idSMU Modules/devices |
| channel_information property                                | Prints and returns tabular information about<br>all channels                      |
| get_channel_name(<channel_id>)                              | Returns the (alias) name of a channel if it<br>was set                            |
| set_channel_name(\<ID\>, \<name\>)                          | Sets an (alias) name for a channel                                                |
| set_device_name(\<ID\>, \<name\>)                           | Sets an (alias) name for a device                                                 |

*Example script using the above methods:*  

```Python
   from aspectdeviceengine.enginecore import IdSmuService, IdSmuServiceRunner, IdSmuBoardModel
   srunner = IdSmuServiceRunner()

   my_board = srunner.get_idsmu_service().get_first_board()
   print(my_board.device_information)
   print(my_board.is_board_initialized())  
   print(my_board.get_all_hardware_ids())
   my_board.set_channel_name("M1.S1.C1", "my_channel")
   print(my_board.get_channel_name("M1.S1.C1"))
   print(my_board.channel_information)
   # output:
   '''
   +----------+------------+-------+----------+-------------+
   | DeviceId | IdSmu-Type | Name  | Firmware | Initialized |
   +----------+------------+-------+----------+-------------+
   | M1.S1    | IdSmu2     | M1.S1 | 0x08191f | true        |
   +----------+------------+-------+----------+-------------+
   True
   ['M1.S1', 'M1.S1.C1', 'M1.S1.C2', 'M1.S1.C3', 'M1.S1.C4']
   my_channel
   +----------+------------+-----------+----------+-------------+
   | DeviceId | IdSmu-Type | Name      | Firmware | Initialized |
   +----------+------------+-----------+----------+-------------+
   | M1.S1    | IdSmu2     | my_module | 0x08191f | true        |
   +----------+------------+-----------+----------+-------------+
   +----------+------------+--------------+
   | Channel# | Channel_ID | Channel_Name |
   +----------+------------+--------------+
   | 1        | M1.S1.C1   | my_channel   |
   | 2        | M1.S1.C2   | M1.S1.C2     |
   | 3        | M1.S1.C3   | M1.S1.C3     |
   | 4        | M1.S1.C4   | M1.S1.C4     |
   +----------+------------+--------------+
   '''
```


| Python        | C++           | Comment                                                                                                                  |
| ------------- | ------------- |:------------------------------------------------------------------------------------------------------------------------ |
| idSmu1Modules | idSmu1Modules | Proxy object representing all<br>idSMU 1(3) modules on the board<br>allowing to select a device with bracket<br>operator |
| idSmu2Modules | IdSmu2Modules | Proxy object representing all<br>idSMU 2 modules on the board<br>allowing to select a device with bracket<br>operator    |