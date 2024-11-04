#!/usr/bin/env python
# coding: utf-8

# # Part 1b: Basics - Logging

# This is the introductory overview of programming the Aspect Device Engine Python API.  
# This document is available as pdf and interactive jupyter notebook.
# The introduction includes the following objectives:
# 
# - How to log to the console and file

# --------
# ## Logging
# In case of programming problems with the hardware, it can be helpful to get a detailed text output with the processes in the software.  
# For this purpose, different levels of detail can be set in this text output, so-called log levels. By default, the log level is set to NONE (0). This means that no log is output.  
# The log levels can have the values 0 to 5. The API provides an enum value for each of these levels.  
# These are as follows: None_(0), Error(1), Warning(2), Info(3), Debug(4), Trace(5).  
# If, for example, the LogLevel Info(3) is set, errors, warnings and some useful information are output. If the 'Trace' level is set, even the communication protocol with the hardware is output.  
# The more detailed the log is, the lower the performance of the engine. You should therefore only switch on (detailed) logging in the event of problems that are not understood or a suspected bug.  
# There are two types of logging: console logging and file logging. Both can be switched on and configured independently of each other.  
# The configuration is relatively straightforward and is briefly described below using code examples. 

# In[1]:


from aspectdeviceengine.enginecore import IdSmuService, IdSmuServiceRunner, IdSmuBoardModel, LogLevel


# ## Console logging
# 
# Console logging can be switched on ready with the construction of the `IdSmuServiceRunner`.  
# The first parameter in the constructor is the log level as a numerical value from 0-5 (default is 0).  
# This log level can be set later using the `LogLevel` enum and the `LogService` object.
# > Note: The log is displayed in the standard console and not in Jupyter Notebook

# In[2]:


# Initialisation of the log level via the ServiceRunner in the highest level ‘Trace’
srunner = IdSmuServiceRunner(5)


# In[3]:


mbX1 : IdSmuBoardModel = srunner.get_idsmu_service().get_first_board()


# In[4]:


# Check the log level via the console_log_level_property of the LogService object
print(srunner.log_service.console_log_level)
# Set a new console log level via the same property
srunner.log_service.console_log_level = LogLevel.Info
print(srunner.log_service.console_log_level)


# ## File logging
# 
# File logging must be activated in a separate step via the LogService object.  
# To do this, first tell the Log Service the path to the file to be logged. The file log level is then set.

# In[7]:


srunner.log_service.file_log_level = LogLevel.Trace
srunner.log_service.set_log_file("C:\\tmp\\log.txt")
print(srunner.log_service.file_log_level)


# In[8]:


# We issue a command to produce a log entry
mbX1.set_enable_clamps(True, ["M1.S1.C1"])


# The output in the file will then look something like this:  
# > Device: Execution of commands triggered...  
# CommandService: Removing command from queue: Name = WriteIdSmuConfigurationCommand, Identifier = 24  
# CommandService: Waiting for commands to execute...  
# Device: Executing command: Name = WriteIdSmuConfigurationCommand, Identifier = 24  
# WriteReadCommand: Executing write read cycles...  
# WriteReadCommand: Executing write read cycle number = 0  
# FtdiService: Setting FTDI pipe timeout = 5000  
# FtdiDevice: Writing to FTDI pipe...  
# FtdiDevice: Successfully wrote to FTDI pipe. Bytes written = 36  
# FtdiDevice: Word# written 00000: 0x00030000  
# FtdiDevice: Word# written 00001: 0x00000001  
# FtdiDevice: Word# written 00002: 0x0000001b

# In[9]:


srunner.shutdown()

