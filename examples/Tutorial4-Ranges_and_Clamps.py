#!/usr/bin/env python
# coding: utf-8

# # Getting startet with the Aspect Device Engine Python API 4
# ## Current Range and Clamps

# This is the forth introductory overview of programming the Aspect Device Engine Python API.  
# This document is available as pdf and interactive jupyter notebook.
# The introduction includes the following objectives:
# - Understanding the current range and clamps of idSMU devices
# 
# ---

# In[1]:


from aspectdeviceengine.enginecore import IdSmuService, IdSmuServiceRunner, IdSmuBoardModel, MeasurementMode, SmuCurrentRange, DpsCurrentRange, CurrentRange
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
srunner = IdSmuServiceRunner()


# In[17]:


mbX1 : IdSmuBoardModel = srunner.get_idsmu_service().get_first_board()
print(mbX1.is_board_initialized())
smu_channel = mbX1.idSmu2Modules['M1.S1'].smu.channels["M1.S1.C1"]
smu_channel.name = "ch1"
smu_channel.enabled = True


# Python can always be used to analyse the properties and methods of an object.  
# We search for current range and clamp in the list, the topics of this tutorial: 

# In[3]:


# Let's list all properties and methods of the smu channel object
[m for m in dir(smu_channel) if not m.startswith('_')]


# ### Current Range
# As an API user, you have the option of manually setting different current ranges.  
# It often makes sense to select a current range that is as close as possible to the current flowing through the DUT.  
# For small currents, the smallest possible matching current range should be selected.  
# This increases the accuracy when measuring a current.
# The two possible device types of an idSMU (SMU and DPS) each have different current ranges.  
# 
# #### Setting and querying the current ranges
# 
# The enum class for the current ranges only contains the respective valid members at channel level for SMU or DPS.  
# The enum at board level is a union of both.    
# In the latter case, the user is responsible for not selecting the wrong value.

# In[4]:


print(list(SmuCurrentRange.__members__))
print(list(DpsCurrentRange.__members__))
print(list(CurrentRange.__members__))


# The default value (after initialization) of a SMU based device is 70mA (and 500mA for a DPS device).
# The `current_range` property of a channel or the `get_current_range()` method of a board
# can be used to query the current range:

# In[5]:


print(smu_channel.current_range)
print(mbX1.get_current_range("ch1"))


# The corresponding setter and board method are `current_range` and `set_current_ranges()`

# In[8]:


smu_channel.current_range = SmuCurrentRange._2mA
print(mbX1.get_current_range("ch1"))
mbX1.set_current_ranges(CurrentRange._200uA_SMU, ["ch1"])
print(smu_channel.current_range)


# More about current ranges and autoranging in the next tutorial.
# ### Current and voltage clamps

# An SMU or DPS channel has clamps. 
# If a voltage is forced, the clamp is a current clamp.   
# If a current is forced (SMU types only), a voltage is clamped.  
# The clamp is active by default. We can check this with the ‘clamp_enabled’ property:

# In[12]:


print(f'Is clamp enabled? {smu_channel.clamp_enabled}')


# In voltage force mode, the default clamp value is 70mA

# In[14]:


print(f'The default upper clamp value is {smu_channel.clamp_high_value}A')


# To see the clamp in action, the voltage is swept across an LED and the current is measured (more on IV sweeps in the next chapters).  
# The clamp is first set to 100uA and the current range is adjusted to this current range:

# In[127]:


currents = np.zeros(40);voltages = np.zeros(40)
smu_channel.clamp_enabled = True

smu_channel.clamp_high_value=0.0001
# an alternative to set lower and upper clamp together is to use the board method:
# mbX1.set_clamps_low_and_high_values(-0.001, 0.0001, ["ch1"])
smu_channel.current_range = SmuCurrentRange._200uA
for i in range(1,40):
    smu_channel.voltage = 2.0+0.2*i
    currents[i] = smu_channel.current
    voltages[i] = smu_channel.voltage


# As can be seen in the plot, the clamp becomes active slightly above the set maximum.
# (Deviations can occur if the clamp is not calibrated)

# In[128]:


fig = make_subplots(rows=1, cols=2,  subplot_titles=("LED current", "LED voltage"))
fig.add_trace(go.Scatter(x=np.arange(1,40), y=currents,
                    mode='lines+markers+text',
                    textposition="top center",
                    name='LED current'),  row=1, col=1)
fig.add_trace(go.Scatter(x=np.arange(1,40), y=voltages,
                    mode='lines+markers+text',
                    textposition="top center",
                    name='LED voltage'),  row=1, col=2)
fig.update_layout(height=600)
fig.update_xaxes(title_text="Step", row=1, col=1);fig.update_yaxes(title_text="Current [A]", row=1, col=1)
fig.update_xaxes(title_text="Step", row=1, col=1);fig.update_yaxes(title_text="Coltage [V]", row=1, col=2)
fig
#uncomment in pure python script:
#fig.show()


# The clamp will now be disabled and the current measurement will be repeated:

# In[114]:


currents = np.zeros(40);voltages = np.zeros(40)

smu_channel.clamp_high_value=0.0001
smu_channel.clamp_enabled = False
smu_channel.current_range = SmuCurrentRange._2mA
for i in range(1,40):
    smu_channel.voltage = 2.0+0.2*i
    currents[i] = smu_channel.current
    voltages[i] = smu_channel.voltage


# In[115]:


fig = make_subplots(rows=1, cols=2,  subplot_titles=("LED current", "LED voltage"))
fig.add_trace(go.Scatter(x=np.arange(1,40), y=currents,
                    mode='lines+markers+text',
                    textposition="top center",
                    name='LED current'),  row=1, col=1)
fig.add_trace(go.Scatter(x=np.arange(1,40), y=voltages,
                    mode='lines+markers+text',
                    textposition="top center",
                    name='LED voltage'),  row=1, col=2)
fig.update_layout(height=600)
fig.update_xaxes(title_text="Step", row=1, col=1);fig.update_yaxes(title_text="Current [A]", row=1, col=1)
fig.update_xaxes(title_text="Step", row=1, col=1);fig.update_yaxes(title_text="Coltage [V]", row=1, col=2)
fig
#uncomment in pure python script:
#fig.show()


# In[129]:


srunner.shutdown()


# ---

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

# In[4]:


srunner.shutdown()

