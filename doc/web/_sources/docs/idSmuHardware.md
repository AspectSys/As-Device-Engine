The idSMU hardware
==================

## idSMU features


The basic concept of the API is the modelling of the various hardware components of idSMU.  
In order to better understand this concept, the hardware components of idSMU will be briefly introduced.

:::{figure-md} markdown-fig
<img src="/_assets/overview/idSMUModule.png" alt="idSMUModule" width="500px">

idSMU Module
:::

__Features__

- Single channel high current (1200mA) voltage source (idSMU1)
- 4 channel voltage and current source (idSMU2)
- Voltage and current measurement
- +/- 12V (idSMU1), +/-11V (idSMU2) default output range
- Asymetric Operation -22V to 24V (idSMU1), -16V to 22V (idSMU2)
- External trigger
- Current clamps / Compliance
- Measurement: 16Bit DAC/ADC, 400uV, 200pA resolution, 250kS/s
- Data rate via USB 3 up to 3.2 Gbit/s
- 26 digital 3.3 IOs
- Optional Pattern generator
- 128 MB DDR RAM


As the name suggests, idSMU is a source measurement unit, i.e. a device with which a voltage (or current) can be forced and measured at the same time. Accordingly, there is at least one SMU unit on an idSMU module. This can have one or more channels.  

The idSMU hardware also offers other interesting features that make it a mini test system. In the context of the API, only the Digital IO from idSMU should be mentioned here.  
Each idSMU module offers 36 digital input/output channels that can also be controlled via the API.
Further hardware is integrated on the modules, e.g. a DRAM. If required, all these components can be used to realise applications that go far beyond forcing and measuring voltages and currents. If required, aSpect Systems can develop customised firmware for various fields of application. One example would be the recording of sensor data, the control of image sensors and the streaming of image data.  

:::{note}
If you are interested in these possibilities, please contact *aSpect Systems* or visist the website https://www.aspect-sys.com
:::


The focus of this document is the description of the API which in its standard version enables the control of the SMU modules and additionally the digital IOs.

## idSMU variants

There are two main variants of idSMU. These differ essentially in the chip used for forcing and measuring voltage or current.  
*idSMU1* and the new variant, *idSMU3*, have only one 'SMU channel'. However, this channel can supply up to __1200mA__. This type of idSMU can only force voltages, but no current.  
For easier differentiation and following the official designation of the chip used, this type idSMU is also called DPS. No distinction is made between idSMU1 and idSMU3, as there are no significant differences in terms of features in programming from the user's point of view. idSMU3 can generate the necessary voltage supply on the module itself, so that the full current range is available here.
For more detailed features, please refer to the relevant product documentation.  

The idSMU2 type offers four channels with 70mA each. This type of idSMU is also called SMU.  
There are a few differences in the voltage range between SMU and DPS. The digital resources do not differ between the two variants.
The names DPS and SMU can be found in the API and are used there as synonyms for the variants mentioned above.

## idSMU boards

### Mb-X1

In order to operate an idSMU module, it is usually connected to a mainboard.  
The API also models this part of the hardware so that several modules can be easily addressed and programmed as a group.
With the help of such a board, the various resources and connections can be made available to the user. 
aSpect Systems already offers ready-made solutions for this.  

The [The Mb-X1](mbx1-fig) offers space for a single idSMU module. 

:::{figure-md} mbx1-fig
<img src="/_assets/overview/mbx1_idSMU.jpg" alt="arch1" width="500px">

idSMU module on a **Mb-X1** board
:::

This board provides connections for the power supply and USB for communication with the module.
The (voltage/current) force lines, trigger, as well as sense lines and digital IOs are connected to the connector on the opposite side.  
Both idSMU1 and idSMU2 and the latest idSMU version, idSMU3, can be plugged into this board.  
For idSMU1, the high current ranges, 500mA and 1200mA, can only be operated in the positive range and only up to 5V.
This restriction does not apply to idSMU3.  

aSpect Systems also offers a [housing](mbx1_housing-fig) for this board.

:::{figure-md} mbx1_housing-fig
<img src="/_assets/overview/mbx1_chassis_idSMU.png" alt="mbx1housing" width="350px">

idSMU module on a **Mb-X1** board with housing
:::

### Mb-X16

If you want to operate several modules at the same time, aSpect Systems offers the [The Mb-X16](mbx16-fig) from aSpect Systems. This offers space for up to 16 idSMU modules. This means that up to 64 SMU channels and 544 digital IOs can be operated.  


:::{figure-md} mbx16-fig
<img src="/_assets/overview/mbx16_idSMU.png" alt="mbx16" width="400px">

idSMU modules on a **Mb-X16** board
:::  
