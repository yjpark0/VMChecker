import tkinter.messagebox as msgbox
from tkinter import *
import platform
import time
from datetime import datetime
from datetime import timedelta
from time import sleep
from time import strftime


#myhost = os.uname()[1]
#os.uname()은 현재 OS에서 다음의 5개 정보(sysname, nodename, release, version, machine)를 받아 이를 튜플로 return합니다.

def initial_setup():
    # 설정파일 읽고, 업데이트
    cfg_file = open("config.cfg", "r+")
    for x in range(3):
        cfg_data = cfg_file.readline()
    cfg_file.close()

    cfg_split = cfg_data.split("|")
    global server_ip, starttime, limittime
    # 서버 IP 주소 셋팅
    server_ip = cfg_split[0]
    # 최초 실행시간 셋팅
    starttime = datetime.now()
    cfg_split[1] = str(starttime)
    # 사용 제한 시간 셋팅(서버에서 통신해서 가져와야함)
    # [참고] 사용시간이 연장되는 경우 수시 통신을 통해 갱신해야함

    # 윈도우 VM 이름 가져오기
    nodename = platform.node()
    cfg_split[4] = nodename

    # 사용 제한시간 가져오기
    limittime = timedelta(hours=100)
    print(limittime)

    print(cfg_split)



def cfg_mgn():
    # 설정파일 읽고, 업데이트
    cfg_file = open("config.cfg", "r+")
    cfg_data = cfg_file.readline()
    cfg_file.close()



def time_alert(name):
    # 시간에 따른 경고 팝업창 출력
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def usage_timer2():
    # 현재까지 사용시간 확인
    # config.cfg 파일에 사용시간 갱신

    while(1):
        lasttime = datetime.now()

        usetime = lasttime - starttime
        print("Use Time : ", usetime, "Remain Time : ", limittime-usetime)

        sleep(5)

def usage_timer():
    starttime = time.time()
    lasttime = starttime
    lapnum = 1
    value = ""

    print("Press ENTER for each lap.\nType Q and press ENTER to stop.")
    print(starttime)
    starttime_str = time.localtime(starttime)
    print(starttime_str)
    while value.lower() != "q":
        # Input for the ENTER key press
        value = input()

        # The current lap-time
        laptime = round((time.time() - lasttime), 2)

        # Total time elapsed since the timer started
        totaltime = round((time.time() - starttime), 2)

        # Printing the lap number, lap-time, and total time
        print("Lap No. " + str(lapnum))
        print("Total Time: " + str(totaltime))
        print("Lap Time: " + str(laptime))

        print("*" * 20)

        # Updating the previous total time and lap number
        lasttime = time.time()
        lapnum += 1

    print("Exercise complete!")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
#    root = Tk()
#    root.title("test")
#    root.geometry("640x480")
#    msgbox.showinfo("test", "test information")
#    print_hi('PyCharm')

    initial_setup()
    usage_timer2()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
