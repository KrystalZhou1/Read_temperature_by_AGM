import time
import csv
import datetime
import os

try:
    import ntplib
except ImportError:
    os.system("python -m pip install ntplib")
    import ntplib

try:
    from papi2 import *
except ImportError:
    print('PAPI2 is not installed on this system, trying to install PAPI2')
    os.system('setup.bat')
    # os.system('mkdir C:\\Users\\Administrator\\Desktop\\papi2')
    # os.system('copy \\\\valfs\\shareall\\E\\EddyWang\\1.0.4\\setup\\bin C:\\Users\\Administrator\\Desktop\\papi2')
    # os.system('mkdir C:\\Users\\Administrator\\Desktop\\papi2')
    # os.system('copy \\\\valfs\\shareall\\E\\EddyWang\\1.0.4\\setup\\bin C:\\Users\\Administrator\\Desktop\\papi2')
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\certifi-2022.12.7-py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\charset_normalizer-3.0.1-cp37-cp37m-win_amd64.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\dohq_artifactory-0.8.4-py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\enum_tools-0.9.0.post1-py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\idna-3.4-py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\keyboard-0.13.5-py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\numpy-1.21.6-cp37-cp37m-win_amd64.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\pandas-1.3.5-cp37-cp37m-win_amd64.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\Pygments-2.14.0-py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\PyJWT-2.6.0-py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\pyparsing-3.0.9-py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\python_dateutil-2.8.2-py2.py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\pytz-2022.7.1-py2.py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\requests-2.28.2-py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\six-1.16.0-py2.py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\typing_extensions-4.4.0-py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\urllib3-1.26.14-py2.py3-none-any.whl")
    # os.system("python -m pip install C:\\Users\\Administrator\\Desktop\\papi2\\papi2-0.11.14.0-py3-none-any.whl")
    from papi2 import *

import papi2.wrappers.toollib


# write data to csv file
def write_data(core_temp):
    with open('CPUTemperature.csv', 'a', encoding='utf-8') as file_obj:
        # crate writer object
        writer = csv.writer(file_obj)
        writer.writerow(core_temp)
        file_obj.close()

# get CPU name
papi = PAPI2.using_toollib()
dev = papi.get_cpu()
print(f"CPU_name:{dev.asic_name}")
# get CPU enabled core number
enabled_core_num = dev.mp1fw.read_fw_state("SystemScoreboard_EnabledCores")
print(f"EnabledCores:{enabled_core_num}")
# write basic CPU info to csv file
CPU_info = [('CPU_name:', dev.asic_name), ('EnabledCores:', enabled_core_num)]
for i in CPU_info:
    write_data(i)
# add header in the CSV
header = ['Time', 'Core', 'Temperature']
write_data(header)

# sync OS time
def sync_OS_time():
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
    # get enabled core
    enabled_core_ccd = []
    for j in range(0, 8):
        enabled_core_ccd.append(dev.mp1fw.read_fw_state("SystemScoreboard_CoreEn_{}".format(j)))
    # print(enabled_core_ccd)
    for i in range(0, 8):
        if enabled_core_ccd[i] == 1:
            print(dev.mp1fw.read_fw_state(f'Data_Core_{i}_Temperature'))
            list = [datetime.datetime.now(), i, dev.mp1fw.read_fw_state(f'Data_Core_{i}_Temperature')]
            write_data(list)

def main():
    sync_OS_time()
    while True:
        get_cpu_temperature()
        time.sleep(120)

if __name__ == main():
    main()


