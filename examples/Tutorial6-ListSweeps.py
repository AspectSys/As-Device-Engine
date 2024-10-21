#!/usr/bin/env python
# coding: utf-8

# # Getting startet with the Aspect Device Engine Python API 6
# 
# ## IV Measurements with List Sweeps

# This is the sixth introductory overview of programming the Aspect Device Engine Python API.  
# This document is available as pdf and interactive jupyter notebook.
# The introduction includes the following objectives:
# - Learn how to use the ListSweep class to perform multi-channel sweeps in sub-milliseconds resolution
# 
# The *function generator* methods already discussed can be used to generate simple sweeps in real time.
# With the so-called *list sweeps*, more complex measurements can be carried out simultaneously on several channels of a module.
# 
# ---
# 
# > Please note: In this example, an idSMU board equipped with LEDs wit series resistors at the outputs was used. If a differently configured board is used, the measurement curves may look different. In the case of open outputs, the sweep can also be performed via the voltage instead of the current. The voltage is measured back correctly, even with open outputs!
# ---
# 

# In[1]:


from aspectdeviceengine.enginecore import IdSmuService, IdSmuServiceRunner, IdSmuBoardModel, MeasurementMode, FunctionGeneratorType, generate_function_generator_data, CurrentRange
from aspectdeviceengine.enginecore import IdSmuBoardModel, ListSweepChannelConfiguration, ListSweep
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
srunner = IdSmuServiceRunner()
mbX1 : IdSmuBoardModel = srunner.get_idsmu_service().get_first_board()


# In[2]:


# It is always a good idea to check if the modules on the board are initialized
print(mbX1.is_board_initialized())
print(mbX1.device_information)


# ### Preparation
# We prepare some variables and enable 2 channels of one idSMU module for the sweep with the multi-side methods. Nothing new here:

# In[3]:


device_id = "M1.S1"
channel1_id = f'{device_id}.C1'
channel2_id = f'{device_id}.C3'

# assign meaningful alias names for the channels
mbX1.set_channel_name(channel1_id, "LED1")
mbX1.set_channel_name(channel2_id, "LED2")
mbX1.set_device_name(device_id, "My_LED_Module")
channel_list = ['LED1', 'LED2']

# enable the two channels together
mbX1.set_enable_channels(True,channel_list)
idSmu2 = mbX1.idSmu2Modules['M1.S1']

# print some channel information
for i, channel in enumerate(idSmu2.smu.channels.as_list()):
    print(f"Channel {i+1} with name {channel.name}" + 
          " is enabled: " + ("YES" if channel.enabled else "NO"))


# ### Preparing the parameters before a sweep
# It is **important to understand** that the sweep works with the previously set configurations for the **force type**
# (voltage for DSP and SMU or current for SMU types) and the **measurement type** (voltage or current). These configurations are *not* part of the parameterisation of the sweep.  
# With a SMU type there is the option of forcing voltage or current, with a DPS type only voltage.
# The `set_voltages()` method encapsulates switching to the force type voltage and setting the output value. Although there are also dedicated methods for switching the force type, this is the simplest (for the SMU there is a corresponding `set_currents()` method).
# To measure a current in the sweep, we set the measurement type to current *(isense)*.  
# We then adjust the current range to the maximum expected current. An autorange does not currently exist for the list sweeps.

# In[4]:


mbX1.set_voltages(1, channel_list)
mbX1.set_measurement_mode(MeasurementMode.isense, channel_list)
mbX1.set_current_ranges(CurrentRange._2mA_SMU, channel_list) # Note: the ranges for DPS-Modules differ from SMU modules!
mbX1.get_output_force_value(channel_list[0])


# ### Configuring the sweep
# The `ListSweepChannelConfiguration` and `ListSweep` classes are involved in the parameterisation of a sweep.  
# `ListSweepChannelConfiguration` is used to configure the form of the sweep for a channel.  
# `ListSweep` executes the sweep and saves the measurement results for each sweep.  
# In addition, parameters common to all sweeps are set here, such as the measurement delay.

# ### Single channel sweep

# ##### Configuration
# We configure a simple linear sweep from 1V to 3V with 20 steps for a single channel.
# The start and end values are always included in the sweep.   
# This is why you can expect *number of steps + 1* measurement results.  
# **Important note:**  
# > The number of sweep steps is currently limited to 52 steps for a single channel sweep
# > as the memory from which the sweep is executed is limited (see advanced topics)
# 
# With 4 lines of code you can configure an executable sweep. In addition, the measurement delay is adjusted in this example:

# In[5]:


# Instantiation of a channel configuration
config_ch1 : ListSweepChannelConfiguration = ListSweepChannelConfiguration()

# Configuration of a 20-steps linear sweep from 1 to 3 including 1 and 3, in units of volt 
# (because the output force typ was set to voltage before)
config_ch1.set_linear_sweep(1, 3, 20)

# Instantiation of a ListSweep object
sweep_1ch : ListSweep = ListSweep("My_LED_Module", mbX1)

# By adding at least one channel configuration to the list sweep, the sweep is ready to start.
sweep_1ch.add_channel_configuration("LED1", config_ch1)

# The default measurement delay of 0 (plus some overhead in the lower us-range)
# is often to short. To allow the output voltage to settle before the measurement
# this time is increased to 100 microseconds
sweep_1ch.set_measurement_delay(100)

# let's examine the sweep array before execution:
print(f'Size of sweep array: {len(config_ch1.force_values)}')
print(f'Type of sweep array: {type(config_ch1.force_values)}')
print(f'Values: {config_ch1.force_values}')


# ##### Execution and results
# The sweep is executed by calling the `run()` method.

# In[6]:


# The run() method starts the sweep and returns after the measurement sweep is finished
sweep_1ch.run()
# The get_measurement_result() method returns the measured values
currents_LED1 = sweep_1ch.get_measurement_result("LED1")

# The get_force_values() of the configuration object returns the forced values
voltages_LED1 = config_ch1.force_values

# The measurement times (=sample times in case of the sample count = 1 which is default)
# can be obtained via the sweep object
sample_times = sweep_1ch.timecode


# #### Plotting the results
# The results are visualised as plots below:

# In[7]:


fig = make_subplots(rows=1, cols=2,  subplot_titles=("LED current vs sample time", "LED current vs voltage"))
fig.add_trace(go.Scatter(x=sample_times, y=currents_LED1,
                    mode='lines+markers',
                    name='LED1 (Ch1)'),  row=1, col=1)
fig.add_trace(go.Scatter(x=voltages_LED1, y=currents_LED1,
                    mode='lines+markers',
                    name='LED1 (Ch1)'),  row=1, col=2)
fig.update_xaxes(title_text="Time [us]", row=1, col=1)
fig.update_yaxes(title_text="Current [A]", row=1, col=1)
fig.update_xaxes(title_text="Voltage [V]", row=1, col=2)
fig.update_yaxes(title_text="Current [A]", row=1, col=2)
fig
#uncomment in pure python script:
#fig.show()


# ### Multi channel sweep
# With a few simple modifications for a second channel, a multi-channel sweep is parameterised. 
# The sweeps can be of different lengths. 
# Here we parameterise both channels differently to show the possibility of flexibly setting the sweep parameters for each channel.
# Instead of the built-in method for a linear sweep,  
# this time we use an array with its own force values on the first channel  
# (even if the numpy arange() function again generates linear values with equidistant values)

# In[82]:


mbX1.set_current_ranges(CurrentRange._2mA_SMU, channel_list)
# first channel configruation
config_ch1 : ListSweepChannelConfiguration = ListSweepChannelConfiguration()
# custom force values
force_values = np.arange(1, 4, 0.20)
# We modify the numpy array a little to distinguish the sweep curve from the linear case
force_values[0:3] = 3
config_ch1.force_values = force_values

# second channel configuration with linear sweep
config_ch2 : ListSweepChannelConfiguration = ListSweepChannelConfiguration()
config_ch2.set_linear_sweep(1, 4, 40)

sweep : ListSweep = ListSweep("My_LED_Module", mbX1)
sweep.add_channel_configuration("LED1", config_ch1)
sweep.add_channel_configuration("LED2", config_ch2)
sweep.set_measurement_delay(100)
sweep.run()

currents_LED1 = sweep.get_measurement_result("LED1")
currents_LED2 = sweep.get_measurement_result("LED2")
sample_times = sweep.timecode


# #### Plotting the results
# The results are visualised as plots below:

# In[83]:


fig = make_subplots(rows=1, cols=2,  subplot_titles=("LED current vs sample time", "LED current vs voltage"))
fig.add_trace(go.Scatter(x=sample_times, y=currents_LED1,
                    mode='lines+markers',
                    name='LED1 (Ch1)'), row=1, col=1)
fig.add_trace(go.Scatter(x=sample_times, y=currents_LED2,
                    mode='lines+markers',
                    name='LED2 (Ch3)'), row=1, col=1)
fig.add_trace(go.Scatter(x=config_ch1.force_values, y=currents_LED1,
                    mode='lines+markers',
                    name='LED1 (Ch1)'), row=1, col=2)
fig.add_trace(go.Scatter(x=config_ch2.force_values, y=currents_LED2,
                    mode='lines+markers',
                    name='LED2 (Ch3)'), row=1, col=2)
fig.update_xaxes(title_text="Time [us]", row=1, col=1)
fig.update_yaxes(title_text="Current [A]", row=1, col=1)
fig.update_xaxes(title_text="Voltage [V]", row=1, col=2)
fig.update_yaxes(title_text="Current [A]", row=1, col=2)
fig
#uncomment in pure python script:
#fig.show()


# ### Advanced topics
# #### Changing the current range during a sweep
# The list sweep does not support autoranging. However, it is possible to change the range at user-defined points in the sweep.  
# The last sweep ran with a range of 2mA. 
# We plot the last sweep again and annotate the step indices to the plot.  
# The switch-on behaviour becomes visible at steps 20-21 or 10-20 microamperes:

# In[84]:


def create_fig():  
    fig = make_subplots(rows=2, cols=1,  subplot_titles=("LED current vs sample time", "LED current vs sample time"))
    fig.add_trace(go.Scatter(x=sweep.timecode, y=sweep.get_measurement_result("LED2"),
                        mode='lines+markers+text',
                        text = [str(i) for i in range(1, len(sample_times) + 1)],
                        textposition="top center",
                        name='LED1 (Ch1)'),  row=1, col=1)
    fig.add_trace(go.Scatter(x=sweep.timecode, y=sweep.get_measurement_result("LED2"),
                        mode='lines+markers+text',
                        text = [str(i) for i in range(1, len(sample_times) + 1)],
                        textposition="top center",
                        name='LED1 (Ch1)'),  row=2, col=1)
    fig.update_yaxes(type="log", range=[np.log(0.0001),np.log(1)], row=2, col=1)
    fig.update_layout(height=600)
    return fig
fig = create_fig()
fig
#uncomment in pure python script:
#fig.show()


# Once you have identified useful points for switching,  
# you can use the `change_current_range_at()` method to switch the range at these points.  
# First, we remove any current range switching from the configuration by calling `clear_current_ranges()`.  
# In this example the sweep starts with a range u 5uA, switches to 20uA at index 18uA and to 200uA at index 20.  
# As can be seen in the plots below, the range below 20 microamperes is now much better resolved than in the last sweep.

# In[80]:


mbX1.set_voltages(1, channel_list)
mbX1.set_current_ranges(CurrentRange._5uA, channel_list)
config_ch2.clear_current_ranges()
sweep.set_sample_count(1)
sweep.set_measurement_delay(500)
config_ch2.change_current_range_at(18, CurrentRange._20uA_SMU)
config_ch2.change_current_range_at(20, CurrentRange._200uA_SMU)
sweep.run()
fig = create_fig()
fig
#uncomment in pure python script:
#fig.show()


# #### Constant force mode and sweep reusage
# Sweeps can be repeated as often as required.  
# The parameters can remain the same or be changed between two runs.  
# This is illustrated by the following example where the last sweep is reused.  
# The first channel is set to ‘constant force’ mode.  
# In this mode, only measurements are made and the force value at the output is not varied. 

# In[89]:


config_ch1.set_constant_force_mode(number_of_steps=41)
sweep.run()
currents_LED1 = sweep.get_measurement_result("LED1")
currents_LED2 = sweep.get_measurement_result("LED2")
sample_times = sweep.timecode


# In[90]:


fig = make_subplots(rows=1, cols=1,  subplot_titles=("LED current vs sample time", "LED current vs voltage"))
fig.add_trace(go.Scatter(x=sample_times, y=currents_LED1,
                    mode='lines+markers',
                    name='LED1 (Ch1)'), row=1, col=1)
fig.add_trace(go.Scatter(x=sample_times, y=currents_LED2,
                    mode='lines+markers',
                    name='LED2 (Ch3)'), row=1, col=1)

fig.update_xaxes(title_text="Time [us]", row=1, col=1)
fig.update_yaxes(title_text="Current [A]", row=1, col=1)
fig
#uncomment in pure python script:
#fig.show()


# In[91]:


srunner.shutdown()

