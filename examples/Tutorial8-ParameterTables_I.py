#!/usr/bin/env python
# coding: utf-8

# # Getting startet with the Aspect Device Engine Python API 8a
# ## Parameter tables I

# This is the 8th introductory overview of programming the Aspect Device Engine Python API.  
# This document is available as pdf and interactive jupyter notebook.
# The introduction includes the following objectives:    
# - How to load parameter setting tables
# - Inspecting the contents of a table
# - How to modify the parameters in the table
# - Sending the parameters of a table to the hardware
#   
# ### Introduction
# There are two basic options for programming the idSMU hardware:  
# Firstly, by calling object methods or setting properties of the hardware models, as described in the previous chapters.  
# The second method is a tabular method.  
# Here, tables are used to hold the values of the hardware parameters. These can be modified and applied.  
# The tabular method is slower than the direct method calls. 
# However, if performance is not the highest priority,   
# this method can be used to export the state of the hardware and apply it again later.  
# Instead of dozens of method calls, just one is then sufficient to set all parameters at once. 

# In[1]:


from aspectdeviceengine.enginecore import IdSmuService, IdSmuSettingsService, IdSmuServiceRunner, IdSmuBoardModel, IdSmuSettingsService
from aspectdeviceengine.enginecore import IdSmuBoardModel, IdqTable, IdqTableGroup
import plotly.graph_objects as go
import pathlib,os
import numpy as np
srunner = IdSmuServiceRunner()
mbX1 : IdSmuBoardModel = srunner.get_idsmu_service().get_first_board()


# The `IdSmuSettingsService` class is used to load and apply tables:

# In[39]:


setting_service : IdSmuSettingsService = srunner.get_idsmu_service().get_settings_service()


# ### Import a table from csv
# The parameter tables, also known as setting tables, have a special format.   
# If you open one of the CSV files with such a table, it looks like this, for example:  
# ![title](idqtable.png)  

# Firstly, the name of the table is given in square brackets [].  
# A table can consist of several groups. As the parameters for the idSMU device are different to the channel parameters,  
# the parameters are each in their own group with their own column headers. 
# The table name is followed by the group name (#).  
# This is followed by the column header of the group and then the actual data.
# This is followed by the entries for the data type or, in the case of enumeration types, the valid values for this parameter.  
# These entries are automatically appended when exporting a table - the user does not have to worry about them.  
# A table can be loaded with the `import_settings_from_csv()` method of the SettingService:

# In[6]:


setting_service.import_settings_from_csv(os.path.join(os.path.abspath(""), "setting_tables_m1.csv" ))
# List all parameter setting names
print(setting_service.get_parameter_settings_names())
# We only print 10 columns so that the output fits on the screen
print(setting_service.print_settings('M1_test', False, False, 10))


# ### Modification of table entries
# The entire table with its groups is managed by an actual table of the type `IdqTable`.  
# The `dqTableGroup` type represents a group.

# In[12]:


paratable : IdqTable = setting_service.get_parameter_setting('M1_test')
group : IdqTableGroup = paratable.get_table_group('SMU-Channel')


# To change a table entry, we need the row index and the column name of the cell.  
# The helper method `get_row_index()` is used to find the row index for a known entry in the table:

# In[30]:


row_idx = [group.get_row_index('HardwareId', 'M1.S1.C1'), group.get_row_index('HardwareId', 'M1.S1.C2')]
print(row_idx)


# The *set_parameter_value()* method is now used to change a value in a table group.  
# All values in the table are of type string:

# In[31]:


group.set_parameter_value(row_index=row_idx[0], parameter_name='OutputForceValue', parameter_value='5')
group.set_parameter_value(row_index=row_idx[1], parameter_name='OutputForceValue', parameter_value='6')
print(setting_service.print_settings('M1_test', False, False, 10))


# ### Writing the parameters
# The `apply_parameter_setting()` method can now be used to write the parameters of a group or the entire table to the hardware.  
# We then examine a few channel parameters:

# In[23]:


setting_service.apply_parameter_setting(setting_name='M1_test', board_address='M1', filtered=False, table_group_name='SMU-Channel')
print(mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C1'].enabled)
print(mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C1'].voltage)
print(mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C2'].enabled)
print(mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C2'].voltage)


# In[41]:


group.at[row_idx[0], 'OutputForceValue'] = "0"
group.at[row_idx[1], 'EnableOutput'] = "0"
print(setting_service.print_settings('M1_test', False, False, 10))
setting_service.apply_parameter_setting('M1_test', 'M1', False, 'SMU-Channel')


# In[42]:


srunner.shutdown()

