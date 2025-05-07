#!/usr/bin/env python
# coding: utf-8

# # Part 4: Clamps, Compliance & Current Range 

# This is the forth introductory overview of programming the Aspect Device Engine Python API.  
# This document is available as pdf and interactive jupyter notebook.
# The introduction includes the following objectives:
# - Understanding the current range and clamps/compliance of idSMU devices
# 
# ---

# In[1]:


from aspectdeviceengine.enginecore import IdSmuService, IdSmuServiceRunner, IdSmuBoardModel, MeasurementMode, SmuCurrentRange, DpsCurrentRange, CurrentRange
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
srunner = IdSmuServiceRunner()


# In[2]:


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


smu_channel.current_range = SmuCurrentRange.Range_2mA
print(mbX1.get_current_range("ch1"))
mbX1.set_current_ranges(CurrentRange.Range_200uA_SMU, ["ch1"])
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

# In[9]:


currents = np.zeros(40);voltages = np.zeros(40)
smu_channel.clamp_enabled = True

smu_channel.clamp_high_value=0.0001
# an alternative to set lower and upper clamp together is to use the board method:
# mbX1.set_clamps_low_and_high_values(-0.001, 0.0001, ["ch1"])
smu_channel.current_range = SmuCurrentRange.Range_200uA
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
smu_channel.current_range = SmuCurrentRange.Range_2mA
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

