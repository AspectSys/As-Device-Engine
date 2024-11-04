Api architecture and concepts
=============================

## The hierarchical hardware model of the API

The core element of the API are the classes that model the idSMU hardware. The part that relates to the measurement and control of current and voltage (SMU) is the most extensive part of the API.  
There is also a smaller API part that deals with programming the digital IOs. This part is kept very simple and will be discussed in a later chapter.  
Any customised software is not part of the core API and will not be discussed in this document.  

The lowest in this hardware model that the user has to deal with are the channels. 
A large part of the parameterisation of the SMU properties of idSMU is carried out in the channel model. For example, the channel model has the property 'output foce value' or 'clamp enabled'.  
The next hierarchical level is the 'Analogue Device Model'. This models the device on idSMU that is responsible for generating and measuring currents and voltages, i.e. the actual SMU (or DPS) chip.  
The analogue device model can contain one or more channels, depending on the type of idSMU. In addition to the channels, the device itself also has some programmable parameters. An example of this is an internal resistor that can be switched on if required. Otherwise, the user has very little contact with other properties of the device model.  
One level further up you will find the idSMU device model. This contains the analogue device model and the digital IO in the standard API. The idSMU device model is the container that contains the various hardware components of idSMU. In idSMU3 there is also a power module at this level. This is not shown in the following images for the sake of simplicity.  
The board model is located at the top level. There can be one or more idSMU devices on a board.  

:::{figure-md} markdown-fig
<img src="/_assets/overview/api_architecture1.png" alt="arch1" width="500px">

High level view on the API architecture
:::

The internal functionality of the device engine is briefly presented here. 
The hardware of idSMU is parameterised internally via registers. This applies to the channel parameters, the analogue device parameters or the digital IOs.  
If a user sets a channel parameter using a method such as ‘SetVoltage’, this is converted into a register value and saved in a register model.  
At the same time, this change is communicated to the board model, which also serves as a control unit. Communication with the hardware is command-orientated.  
To stay with the example of setting a voltage, a command is assembled that contains the channel to be programmed as an address and the register value that represents this voltage. This command is assembled by the board model and sent to other parts of the device engine, which finally communicate with the hardware via USB.  
These register models and the commands normally remain hidden from the user. Instead, they can work with the descriptive methods and properties of the hardware models.  

:::{figure-md} markdown-fig2
<img src="/_assets/overview/api_architecture2.png" alt="arch2" width="500px">

The state of the hardware is modeled through registers
:::