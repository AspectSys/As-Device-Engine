#!/usr/bin/env python
# coding: utf-8

# # Getting startet with the Aspect Device Engine Python API 8b
# ## Parameter tables II

# This is the 8th introductory overview of programming the Aspect Device Engine Python API.  
# This document is available as pdf and interactive jupyter notebook.
# The introduction includes the following objectives:    
# - How to export the state of the hardware into a parameter table file
# - Filtering
#   
# ### Introduction
# The basics of the parameter tables were presented in the last chapter.  
# Further options will now be discussed.

# In[1]:


from aspectdeviceengine.enginecore import IdSmuService, IdSmuSettingsService, IdSmuServiceRunner, IdSmuBoardModel, IdSmuSettingsService
from aspectdeviceengine.enginecore import IdSmuBoardModel, IdqTable, IdqTableGroup
import plotly.graph_objects as go
import pathlib,os
import numpy as np
srunner = IdSmuServiceRunner()
mbX1 : IdSmuBoardModel = srunner.get_idsmu_service().get_first_board()


# The `IdSmuSettingsService` class is used to load and apply tables:

# In[2]:


setting_service : IdSmuSettingsService = srunner.get_idsmu_service().get_settings_service()


# ### Exporting a table
# The Methode get_parameter_settings_for_board() is used to read out the current status of the hardware and generate a parameter table.  
# We first change a few parameters and then analyse the table: 

# In[3]:


mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C1'].voltage = 1
mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C2'].voltage = 2
mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C3'].voltage = 3
mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C4'].voltage = 4
mbX1_settings : IdqTable = setting_service.get_parameter_settings_for_board('M1')
print(mbX1_settings.name)
print(setting_service.print_settings(mbX1_settings.name, False, False, 10))


# Before saving the table, it is advisable to change the name of the table.  
# The default name is the board address.  
# The name of a table to be loaded later should therefore be different from this default value so that this table is not overwritten by the method executed above.

# In[4]:


mbX1_settings.name = "M1_voltages_set"
print(mbX1_settings.name)
print(setting_service.get_parameter_settings_names())


# The table is now exported using the `export_settings_to_csv()` method. The three parameters of the method are self-explanatory.  
# The reason why `setting_names` is a list is that it is also possible to write several tables to one file.  
# In the example here, we only write the table just created to the file:

# In[15]:


setting_service.export_settings_to_csv(file_path=os.path.join(os.path.abspath(""),
                                        mbX1_settings.name + ".csv"), setting_names=['M1_voltages_set'],
                                        append_to_file=False)


# The result looks like this:  
# ![title](idqtable2.png)  

# ### Filtering and applying sub-tables
# Previously, all entries in a table or group were always sent to the hardware.  
# But what if you only want to use certain entries?  
# There are various filter methods. You can then send only the filtered table to the hardware instead of the entire table.
# 
# #### Row filter
# The parameters of the `filter_rows()` method are the column name, the value in this column and whether to search for whole words and not just substrings (exact_match).  
# To print the filtered version of a table, the second parameter in `the print_settings()` method is set to True.

# In[5]:


filtered_table = mbX1_settings.filter_rows(column_name='HardwareId', filter_value='M1.S1.C2', exact_match=False) 
print(setting_service.print_settings('M1_voltages_set', True, False, 10))


# The pipe character (|) can be used to realise a logical ‘or’:

# In[6]:


filtered_table = mbX1_settings.filter_rows(column_name='HardwareId', filter_value='M1.S1.C2|M1.S1.C4', exact_match=False) 
print(setting_service.print_settings('M1_voltages_set', True, False, 10))


# If the ‘filtered’ flag of the ‘apply_parameter_setting()’ method is set,  
# only the filtered version is written to the hardware instead of the entire table:

# In[8]:


mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C1'].voltage = 5
mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C2'].voltage = 5
mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C3'].voltage = 5
mbX1.idSmu2Modules['M1.S1'].smu.channels['M1.S1.C4'].voltage = 5
setting_service.apply_parameter_setting(setting_name='M1_voltages_set', board_address='M1', filtered=True, table_group_name='SMU-Channel')


# We export the status of the hardware to a new table. Now only the values of the filtered table should have been written.  
# The voltages of channels 1 and 3 were set to 5 volts. The remaining channels retain their values.

# In[9]:


mbX1_settings : IdqTable = setting_service.get_parameter_settings_for_board('M1')
print(setting_service.print_settings(mbX1_settings.name, False, False, 10))


# In[10]:


srunner.shutdown()

