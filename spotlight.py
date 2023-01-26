# spotlight.py - check for new files

import os
from datetime import datetime
from shutil import copyfile

# C:\Users\joao.moreira\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets

#-------------------------------------------------------------------------------
# $HOME/.spot directory to store the snapshots of the assets directory
# snap_yyyy-mm-dd_hh-mm-ss.txt
# log.txt write an entry each time the script is run
# img subdir: when a change is detected, all files are copied here
# subdirectories named yyyy-mm-dd_hh-mm-ss
#
# C:\x\img\Spotlight final destination after rename (manual)
#-------------------------------------------------------------------------------

# Directory where the Spotlight service drops the image files
drop_path = (r'C:\Users\joao.moreira\AppData\Local\Packages'
    + r'\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy'
            + r'\LocalState\Assets')

#-------------------------------------------------------------------------------
# file_info
#-------------------------------------------------------------------------------

def file_info(path, f):
    """Get file's size, last modified time, name."""
    filepath = os.path.join(path, f)
    sz = os.stat(filepath).st_size
    secs = os.path.getmtime(filepath)
    dt = datetime.fromtimestamp(secs)
    return sz, dt, f

#-------------------------------------------------------------------------------
# dir_snapshot
#-------------------------------------------------------------------------------

def dir_snapshot(path):
    """Get a snapshot of the directory."""
    # List of files, most recent one first
    files = os.listdir(path)
    sfiles = sorted([file_info(path, f) for f in files], key=lambda x: x[1],
                    reverse=True)
    s = '   Size Date                Name\n'
    for sz, dt, f in sfiles:
        s += f"{sz:>7} {dt.strftime('%Y-%m-%d %H:%M:%S')} {f}\n"
    return s

#-------------------------------------------------------------------------------
# get_latest
#-------------------------------------------------------------------------------

def get_latest():
    """Get the latest snapshot that we have."""
    path = os.path.join(os.environ['HOME'], '.spot')

    # List of snap_*.txt files, most recent one first
    files = [f for f in os.listdir(path)
                 if f.startswith('snap_') and f.endswith('.txt')]
    sfiles = sorted([file_info(path, f) for f in files], key=lambda x: x[1],
                    reverse=True)
    if len(sfiles) == 0:
        return None
    
    # Return latest snapshot's contents
    sz, dt, latest = sfiles[0]
    with open(os.path.join(path, latest), 'r') as f:
        return f.read()

#-------------------------------------------------------------------------------
# snaphost
#-------------------------------------------------------------------------------

def snapshot(drop_path):
    spot_path = os.path.join(os.getenv('HOME'), '.spot')

    # Current time for logging and filenames
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    s1 = dir_snapshot(drop_path)
    s2 = get_latest()

    # Are there any changes since the last saved snapshot ?
    if s2 is not None and s1 == s2:
        with open(os.path.join(spot_path, 'log.txt'), 'a') as f:
            f.write(f'{timestamp}: no changes\n')
        return
    
    # Write the new snapshot file
    filename = f'snap_{timestamp}.txt'
    with open(os.path.join(spot_path, filename), 'w') as f:
        f.write(s1)

    # Save the image files
    img_path = os.path.join(spot_path, 'img')
    tstmp_path = os.path.join(img_path, timestamp)
    os.makedirs(tstmp_path)
    for f in os.listdir(drop_path):
        src = os.path.join(drop_path, f)
        if not os.path.isfile(src):
            continue
        dst = f'{os.path.join(tstmp_path, f)}.jpg'
        copyfile(src, dst)

    # Write out the log entry
    with open(os.path.join(spot_path, 'log.txt'), 'a') as f:
        f.write(f'{timestamp}: new snapshot written\n')

#===============================================================================
# main
#===============================================================================

if __name__ == '__main__':
    snapshot(drop_path)
