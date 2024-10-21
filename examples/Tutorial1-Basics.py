#!/usr/bin/env python
# coding: utf-8

# # Getting startet with the Aspect Device Engine Python API
# ## Basics

# This is the introductory overview of programming the Aspect Device Engine Python API.  
# This document is available as pdf and interactive jupyter notebook.
# The introduction includes the following objectives:
# 
# - The few steps to initializing software and hardware
# - How to retreive information about the hardware
# - Providing a basic understanding of the structure of the API
# - The programming of essential channel parameters
# - Setting a voltage and measuring voltage and current 
# 
# The following spoiler shows a python code snippet and few lines of code that are necessary with the API to generate and measure a voltage:  
# 
# ```Python
# from aspectdeviceengine.enginecore import IdSmuServiceRunner
# from aspectdeviceengine.enginecore import IdSmuService, IdSmuBoardModel
# 
# # 3 lines of code for the setup
# srunner = IdSmuServiceRunner()
# mbX1 : IdSmuBoardModel = srunner.get_idsmu_service().get_first_board()
# channel1 = mbX1.idSmu2Modules['M1.S1'].smu.channels[1]
# 
# # 3 lines of code for configuration and measurement
# channel1.enabled = True
# channel1.voltage = 2
# print(channel1.voltage)  # output : ~2.0
# ```
# At the end of this document, this code and some of the background to it should be understandable.

# --------
# ### Python imports  
# There are only a few python imports needed for this introduction. Everthing is imported from the *aspectdeviceengine.engincore* module.
# Actually, only the IdSmuServiceRunner would be needed since this is the only class that will be instantiated. The other classes are only imported for type hinting. The objects of these types are intantiated by the API services. 

# In[1]:


from aspectdeviceengine.enginecore import IdSmuService, IdSmuServiceRunner, IdSmuBoardModel


# ### Starting the services and hardware initialization
# 
# #### IdSmuServiceRunner
# The *IdSmuServiceRunner* holds the references to the background services.
# If it goes out of scope, all services are shut down (cleanup processes).
# The lifetime should therefore be guranteed until the end of the session:

# In[2]:


srunner = IdSmuServiceRunner()


# #### IdSmuService
# idSmu devices are detected by the **IdSmuService**. If the *get_first_board()* 
# method is called prior to the detection method, the detection and initialization
# is performed automatically. This is useful for situations where
# no specific configuration needs to be done before initialization.  
# 
# **Important note:** At the end of a session (be it a jupyter notebook or a python script) the services must be shut down. In the case of the termination of a python script, this happens automatically. When moving from one notebook tutorial to the next, either the kernel must be terminated or the shutdown() method must be executed manually (see last cell in the notebook).
# 
# #### The IdSmuBoardModel
# The IdSmuBoardModel is the host and (multiside-)controller for idSmu devices.

# In[3]:


mbX1 : IdSmuBoardModel = srunner.get_idsmu_service().get_first_board()


# With this single line of code the Hardware is detected and initialized!  
# Let's print some basic information about the detected devices for this board.  
# The most relevant information is the **DeviceId** and the device type.
# The DeviceId is used as resource identifier/ locator for the different
# parts of the hardware. The format is \Mx.Sy.Cz, where x is the mainboard address,
# y is the device/slot number and z is the channel number.  
# In the case of the API, the terms *Resource-Id* and *Address* are sysnonyms for the same thing.
# 

# In[4]:


print(mbX1.device_information)


# -------
# ### Programming the hardware with the API
# #### idSmu Modules/Devices and Channels
# With this system of hierarchical resource localization, each resource is uniquely identifiable, 
# even in a multi-board setup.  
# As we can see (in a single idSmu board setup), there is 
# exactly one device with the address "M1.S1".  
# An idSmu device (sometimes called module) can contain one or more channels. We can obtain more information about these channels, 
# for example their IDs/addresses:

# In[5]:


for idSmu2 in mbX1.idSmu2Modules.as_list():
    print(f'idSmu2 ID:    {idSmu2.hardware_id}')
    print(f'idSmu2 name:  {idSmu2.name}')
    print(f'channel IDs:  {idSmu2.channel_ids}')


# #### IdSmuDeviceModel
# The idSmuModules classes are proxy classes that implement the [ ] operator for quick access to a device/module of type IdSmuDeviceModel and the as_list() method to get all devices of the same type on the board. There are implementations for the all types of idSmu.  
# 
# To access a module we can simply use `idSmu2Modules['address or name of module']`

# In[6]:


idSmu2 = mbX1.idSmu2Modules['M1.S1']
print(f"The module's id is {idSmu2.hardware_id} and the name is {idSmu2.name}")


# #### Alias names
# Devices can be renamed, either programmatically or by so-called parameter settings. 
# Parameter settings are applied during initialization and the changed name can thus be used immediately. (programming via parameter settings is an advanced topic and will not be dealt with here).  
# The advantage of renaming resources is that you can use an alias name for addressing 
# instead of the rather abstract resource IDs / addresses:

# In[7]:


idSmu2.name = 'MyFavoriteModule'
# now we can reference the module with the new name
my_fav_module = mbX1.idSmu2Modules['MyFavoriteModule']

print(f"The module's id is still {my_fav_module.hardware_id} and the new name is {my_fav_module.name}")


# The board's device information now lists the new name:

# In[8]:


print(mbX1.device_information)


# ### Descending further into the model hierarchy  
# The idSmu-Hardware is not just a source measurement unit, but combines various hardware components. 
# For example, digital signals can be generated or a RAM memory can be used, depending on the hardware/software support. 
# The software therefore models the hardware in dedicated units. One of the most important elements of the IdSmuDeviceModel 
# mentioned above is the unit with which currents and voltages can be generated and measured. 
# These units are called SMU or DPS, depending on the device type. 
# 

# In[9]:


print(idSmu2.smu)


# #### The channel models
# The smu/dps subcomponents are again proxy objects and contain a Channels object.  
# This Channels object implements the [ ] operator for fast access to the channels of the source measurement unit. There is also a as_list() method again to itearate over the channels.
# The objects returned by the channels object are of type AnalogChannelModel. 
# This class contains a large part of the methods and properties
# that you have to deal with in your daily work with the API.
# 

# In[10]:


for i, channel in enumerate(idSmu2.smu.channels.as_list()):
    print(f"Channel number {i+1} with name {channel.name}"
          f" and identifier {channel.hardware_id}")
    channel.name = f'MyChannel{i+1}'


# After renaming a channel, there are 3 ways to address it:
# - through the channel number (starting from 1)
# - through the unique channel identifier
# - through the channel name

# In[11]:


print(idSmu2.smu.channels[1].hardware_id)
print(idSmu2.smu.channels["M1.S1.C1"].hardware_id)
print(idSmu2.smu.channels["MyChannel1"].hardware_id)


# > **Importante Note**: Attempting to assign the same name to two different channels leads to an exception. Channel names must be unique. 
# The reason is that the engine accepts names as resource identifiers for many operations. If the user were given the option to overwrite this name, bugs that are difficult to identify would be possible:

# In[13]:


try:
    idSmu2.smu.channels[2].name="MyChannel1"
except Exception as e:
    print(f"Exception: {str(e)}")


# ### Parameterization and measurements  
# Now we have a reference to the channel object and can finally parameterize it and take measurements.
# A channel must be active so that a voltage (or a current) can be output or meaningful measurements can be made.  
# Let's check if the channel is enabled, and if it is not, enable it:

# In[12]:


channel1 = idSmu2.smu.channels["MyChannel1"]
print(f'Channel enabled? {channel1.enabled}')
if not channel1.enabled:
    channel1.enabled = True
print(f'Channel enabled? {channel1.enabled}')


# #### Measuring voltage and current  
# The quickest and easiest way to measure a voltage or a current are the properties `voltage` and `current`

# In[15]:


print(f'Measured voltage: {channel1.voltage:6f}')
print(f'Measured current: {channel1.current:6f}')


# #### Setting voltage and current  
# The quickest and easiest way to set a voltage or a current are the setters `voltage` and `current`

# In[16]:


channel1.voltage = 3.14
print(f'Measured voltage: {channel1.voltage:6f}')

# Setting a current is only usefull if there is a load at the outputs
# wheras voltages can be measured on an open output
# channel1.current = 1E-3
# print(f'Measured current: {channel1.current:6f}')


# #### Bonus: Getting the maximum output voltage and output current ratings

# In[17]:


vMin, vMax, iMin, iMax = channel1.output_ranges
print(f'Output voltage range: [{vMin:6f}, {vMax:6f}] V')
print(f'Output current range: [{iMin:6f}, {iMax:6f}] A')


# In[18]:


srunner.shutdown()


# ---
