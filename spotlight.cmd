rem spotlight.cmd
@echo off

rem Check the Spotlight service assets' directory for new files
py spotlight.py >> spotlight.log 2>&1 
