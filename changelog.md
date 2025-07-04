# Change Log
<br/>

## [0.9.584] - 2025-05-12

### Fixed
- Autoranging not working when voltage or current is set through the board model

## [0.9.583] - 2025-04-25

### Fixed
- Fixed giving the channel numbers for a multi-channel-measurement not in acending order throws an error

## [0.9.581] - 2025-02-07

### Fixed
- Fixed command future was requested AFTER queueing the command which could lead to invalid future when command finished execution in its thread before the request was executed

## [0.9.577] - 2024-11-05

### Fixed
- Fixed autoranging using sample count AND measurement count for measurements which lead to long measurement times

### Added
- Measurement count in autoranging can be changed
- Delay after current range switching in autoranging can be adjusted
- Added numpy as a dependency to the python wheel

## [0.9.568] - 2024-11-05

### Fixed
- Fixed a bug where TRACE file log level was ignored when logging binary protocol


## [0.9.566] - 2024-11-04

### Fixed
- Fixed a bug where deinitialization did not reset the device state to "not initialized"

### Added
- More configuration options for logging


## [0.9.559] - 2024-10-30

### Added
- changelog file

### Changed
- Current range enums now prefixed with "Range_" instead of underscore
- The parameter names 'channel_Id' were largely renamed to 'channel_name'
- Updated jupyter notebook, documentation, tutorials to reflect changes
- Rework of tutorial titles
