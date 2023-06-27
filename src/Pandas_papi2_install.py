#import keyMouse
import time,os
# import win32gui

def check_Papi():
    try:
        import papi2
        return True
    except:
        return False

def check_kysy():
    if os.path.isfile(r'C:\AMD\Kysy4\Python\KysyEnvironment.py'):
        return True
    else:
        return False

def window_enum_handler(hwnd,resultList):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

def get_app_list(handles=[]):
    mlst=[]
    win32gui.EnumWindows(window_enum_handler,handles)
    for handle in handles:
        mlst.append(handle)
    return mlst

def kysy_install():
    while not check_kysy():
        print("install kysy")
        os.system(r'Setup.exe /S /v/qn')
        time.sleep(20)

def pandas_install():
    print("pandas installing")
    os.system("pip install pandas-1.3.5-cp37-cp37m-win_amd64.whl")
    print("pandas done")

def papi2_install():
    papiVer=''
    print("install papi2")
    for i in os.listdir():
        if 'papi2' in i:
            papiVer=i
    if not check_Papi():
        os.system("pip install "+papiVer)
    print("papi2 is installed done")
    time.sleep(5)
    print("papi2 finished")

if __name__ == '__main__':
    #kysy_install()
    pandas_install()
    time.sleep(2)
    papi2_install()
