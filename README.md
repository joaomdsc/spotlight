# Spotlight

Retrieving Microsoft's Spotlight images.

## Usage

### `spotlight.cmd`

The `spotlight.cmd` command is scheduled to run once a day, using Windows' Task
Scheduler. It can also be run directly here. It writes image files and other
information in `%localappdata%\spot`.

The `log.txt` file has one entry for each run. When a new snapshot is written,
the image files themselves are written under `%localappdata%\spot\img\<date>`,
and a text version of the snapshot is written in
`%localappdata%\spot\snap_<date>.txt`. 

### `copy_images.py`

Collecting images from the snapshots is done with `copy_images.py` (this
requires the activation of the virtualenv). It copies image files to the
`master` sub-directory. This must then be manually copied off-site.

