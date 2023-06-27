@echo off


tzutil /s "China Standard Time"
net time \\ouray /set /y

cd C:\autoloop\TemperatureSyncForAVFSTest\AVFS_TempuratureLog

start cmd /k python TemperatureSyncByAGM.py