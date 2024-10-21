#!/usr/bin/env python
# coding: utf-8

# # Getting startet with the Aspect Device Engine Python API 3
# ## Multi-side and high performance

# This is the third introductory overview of programming the Aspect Device Engine Python API.  
# This document is available as pdf and interactive jupyter notebook.
# The introduction includes the following objectives:
# - Understanding the parallel or multi-side programming of idSMU resources
# 
# ---
# 
# ### Intoduction
# In the previous chapters, the idSMU channels were always programmed individually and sequentially.  
# This is the simplest and quickest approach to programming the hardware. This approach is sufficient in cases where a high-performance application is not important.  
# With its multi-threading approach, the aspect device engine also offers the possibility to programme and measure resources efficiently in parallel. 

# In[1]:


from aspectdeviceengine.enginecore import IdSmuService, IdSmuServiceRunner, IdSmuBoardModel, MeasurementMode
import plotly.graph_objects as go
import numpy as np
srunner = IdSmuServiceRunner()


# In[2]:


mbX1 : IdSmuBoardModel = srunner.get_idsmu_service().get_first_board()
mbX1.is_board_initialized()


# The IdSmuBoardModel class is the host and controller for the detected hardware on an idSMU board.  
# A board can, for example, contain a single idSMU module (MbX-1) or 16 (MbX-16). 
# Parallelisation is optimised for one board, i.e. all theoretically possible 160 channels of an MbX-16 board could be set to 0V at once and the engine would attempt to carry out this process as efficiently as possible.  
# Parallelism between several boards is also given in the sense that the programming of a resource is a non-blocking process running in the background.  
# The most frequently used methods for parameterising and measuring a channel are also available as board methods.  
# For example, the property `.voltage` of a channel corresponds to the `set_voltages()` method of a board.  
# The plural in the method name already indicates that several channels can be programmed simultaneously here.

# In[3]:


# The anatomy of a board method usually consists of the combination parameter-value,
# followed by a list of device or channel names (or identifiers)
# We could set a voltage for each channel separately:
mbX1.set_voltages(3.14, ["M1.S1.C1"])
mbX1.set_voltages(4.13, ["M1.S1.C2"])
# or in parallel:
mbX1.set_voltages(3.14, ["M1.S1.C1", "M1.S1.C2"])

# After assigning some alias names... 
mbX1.idSmu2Modules['M1.S1'].smu.channels["M1.S1.C1"].name = "channel1"
mbX1.idSmu2Modules['M1.S1'].smu.channels["M1.S1.C2"].name = "channel2"
# ...the new names can be used in the board methods:
mbX1.set_voltages(3.14, ["channel1", "channel2"])
# Changing the measurement mode and enabling the channels is done in a similar way:
mbX1.set_measurement_modes(MeasurementMode.vsense, ["channel1", "channel2"])
mbX1.set_enable_channels(True,["channel1", "channel2"] )


# ### Parallel measurements in detail

# In[4]:


smuchannel1 = mbX1.idSmu2Modules['M1.S1'].smu.channels['channel1']
smuchannel2 = mbX1.idSmu2Modules['M1.S1'].smu.channels['channel2']


# In[5]:


print(smuchannel1.enabled, smuchannel2.enabled)


# In[6]:


print(smuchannel1.voltage, smuchannel2.voltage)


# We have set and measured the output voltage using the simple and intuitive method via channel properties, as presented in the last tutorials. These measurements run sequentially. Next, we will learn about the high-performance parallel method.
# The IdSmuBoardModel has numerous methods for programming and measuring the resources it manages.
# One of these methods is `set_voltages()`, which can be used to set any number of channels together to the same voltage value.

# In[7]:


mbX1.set_voltages(voltage=2.5, channel_names=["channel1", "channel1"]) 
# for SMU-based modules, set_currents() can be called as well


# We can still use the "channel-method" to query the voltages:

# In[27]:


print(smuchannel1.voltage, smuchannel2.voltage)


# ### Synchronous and asynchronous measurements
# When performing a measurement via the board controller (*IdSmuBoardModel*) on one or more channels, you have the choice of either waiting for the result until the measurement has been performed or letting the measurement run in the background. The latter is particularly useful for triggered measurements or for GUI applications or other asynchronous tasks.  
# This is set with the `wait_for_result` parameter of the `measure_channels()` method.   
# The `measure_channels()` method also offers the advantage of being able to set other parameters, such as the sample count or the number of measurements.
# Let's perform a synchronous measurement with 2 repetitions on 2 channels:

# In[28]:


measresults = mbX1.measure_channels(wait_for_result=True, sample_count=1, repetitions=2, channel_names=["channel1", "channel2"])


# **Important Note:**
# > The user is responsible to provide a valid list of channel names/identifiers.
# > In addition to the valid names, care must also be taken to ensure that the channel names
# > in the list are unique without duplicate entries. Otherwise errors will occur!
# 
# #### Measurement Results
# The result of a measurement via a board is a vector (list) of measurement results.  
# Each of these measurement results relates to an idSmu module/device.   
# As the `measure_channels()` method can be used to measure several channels on several modules quasi-parallel, this result list can contain more than one entry.
# As we only measured on one module on two channels, the list only has one entry:

# In[29]:


print(len(measresults))
measresult0 = measresults[0]
type(measresult0)


# The elements of the result are of type `ReadAdcCommandIdSmuResult`.
# Useful properties are `device_id , channel_ids, channel_names, execution_time`:

# In[30]:


print(f'The results come from the measurement on the device with the id {measresult0.device_id}')
print(f'The total execution time (including data transfer via usb etc) was {measresult0.execution_time} microseconds.')


# To further simplify the assignment of the results to the measured resources, we can query the IDs of the channels or their names
# (the names must have been set before execution, see above)

# In[31]:


print(measresult0.channel_ids, measresult0.channel_names)


# There are now several ways to obtain the result for a specific channel (as numpy array), which are all equivalent:

# In[32]:


print(measresult0.get_float_values("M1.S1.C1"))
print(measresult0["M1.S1.C1"])
print(measresult0["channel1"])
print(measresult0[measresult0.channel_names[0]])

# example of averaging the results for each channel:
for channel_name in measresult0.channel_names:
    print(f'{channel_name} with an average value of {np.mean(measresult0[channel_name]):.4f} V')


# ### Asynchronous measurements

# With asynchronous measurements, there is no waiting for a measurement. The commanded measurements are started in the background in high-performance C++ threads. 
# The measurement results can be retrieved in python at any time. 
# The result of the non-waiting `measure_channels()` method is therefore an empty array as shown below:

# In[34]:


measresults = mbX1.measure_channels(wait_for_result=False, sample_count=1, repetitions=2, channel_names=["channel1", "channel2"])
print(measresults)


# The `get_measurement_results_for_channel()` method returns the result of at least the specified channel. 
# If several channels are measured simultaneously on one device, as in this example, 
# all results are returned (a device cannot return the results separately for each channel).
# Since *chanel1* and *channel2* channels are on the same device, 
# an object is returned that bundles the results for these two channels. 
# It is of the same type as the element already from the array after the synchronous call of the measurement. 
# To recognize it, we call it “measresult0” again

# In[35]:


measresult0 = mbX1.get_measurement_results_for_channel("channel1")


# In[36]:


print(measresult0["channel1"])
print(measresult0.timecode)


# #### Timecode generation during measurements
# In addition to the actual measurement data, a time code can be generated that tracks the exact time at which a measurement was started. 
# The following method is used to activate this (after restarting a device, the default is *disabled*):

# In[37]:


mbX1.enable_timecode("M1.S1")


# The timecode is counted in multiples od 10ns (100Mhz clock). 
# It is generated by counter that always runs when enabled, not only when commands are sent.
# We substract the first value from the array for an offset of zero and devide by 100 to get the time in units of microseconds.

# In[39]:


measresults = mbX1.measure_channels(wait_for_result=False, sample_count=1, repetitions=20, channel_names=["channel1", "channel2"])
measresult0 = mbX1.get_measurement_results_for_channel("channel1")

timecode = (measresult0.timecode-measresult0.timecode[0])/100


# Now we can display the measurement results in a plot over an axis that displays the normalized time vs the measurement results

# In[41]:


x_ = timecode
# Create traces
fig = go.Figure()
fig.add_trace(go.Scatter(x=x_, y=measresult0["channel1"],
                    mode='lines+markers',
                    name='ch1'))
fig.add_trace(go.Scatter(x=x_, y=measresult0["channel2"],
                    mode='lines+markers',
                    name='ch2'))
fig.update_layout(  title={'text': "Parallel 2 channel measurement",  'y':0.9,  'x':0.5, 'xanchor': 'center',  'yanchor': 'top'},
                   xaxis_title='Time [us]',  yaxis_title='Voltage [V]', margin=dict(l=20, r=20, t=55, b=20))
fig
#uncomment in pure python script:
#fig.show()


# Do not forget to shut down the services before proceeding:

# In[42]:


srunner.shutdown()

