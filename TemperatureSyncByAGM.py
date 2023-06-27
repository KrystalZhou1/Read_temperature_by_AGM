import time
import os
import pandas as pd

try:
    import ntplib
except ImportError:
    # os.system("python -m pip install ntplib")
    os.system("pip install C:\\autoloop\\TemperatureSyncForAVFSTest\\AVFS_TempuratureLog\\bin\\ntplib-0.4.0-py2.py3-none-any.whl")
    import ntplib

try:
    import openpyxl
except ImportError:
    # os.system("python -m pip install openpyxl")
    os.system("pip install openpyxl")
    import openpyxl
    
# sync OS time
def sync_os_time():
    c = ntplib.NTPClient()
    # Website of time service center
    response = c.request('pool.ntp.org')
    ts = response.tx_time
    _date = time.strftime('%m-%d-%Y', time.localtime(ts))
    print(_date)
    _time = time.strftime('%X', time.localtime(ts))
    print(_time)
    os.system('date {} && time {}'.format(_date, _time))


# get CPU each core temperature
def get_cpu_temperature():
    new_file_path = r'C:\autoloop\TemperatureSyncForAVFSTestByAGM\AVFS_TempuratureLog\temperatureLogByAGM.xlsx'
    pm_log_path = r'C:\autoloop\TemperatureSyncForAVFSTestByAGM\AVFS_TempuratureLog\pm.csv'
    command = r'"C:\Program Files\AMD Graphics Manager\AMDGraphicsManager.exe" -pmPeriod=4000 -pmLogAll'
    if os.path.isfile(pm_log_path):
        if os.path.isfile(new_file_path):
            data = pd.read_csv(pm_log_path, index_col=0)
            data1 = pd.read_excel(new_file_path, index_col=0)
            df = pd.concat([data1, data])
            df.to_excel(new_file_path, encoding='utf-8')
            os.remove(pm_log_path)
            os.system(command)
        else:
            data = pd.read_csv(pm_log_path, index_col=0)
            data.to_excel(new_file_path, sheet_name='sheet1')
            os.remove(pm_log_path)
            os.system(command)
    else:
        os.system(command)


def main():
    #sync_os_time()
    get_cpu_temperature()


if __name__ == main():
    main()


