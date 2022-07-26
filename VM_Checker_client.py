# VM 이용시간 확인 클라이언트 프로그램
# VM 시작프로그램에 등록

import tkinter.messagebox as msgbox
from tkinter import *
import platform
from datetime import datetime
from datetime import timedelta
from time import sleep

schedule_timer = 5
cfg_file = "config.cfg"
# config 파일 구성
# 서버IP|사용시작시간|사용시간|제한시간|VM이름
his_file = "history.txt"

def initial_setup():
    # 최초 실행
    # 설정파일 읽고, 업데이트
    cfg_f = open(cfg_file, "r+")
    cfg_data = cfg_f.readline()
    cfg_f.close()

    cfg_split = cfg_data.split("|")
    global server_ip, starttime, limittime, nodename, usetime
    # 서버 IP 주소 셋팅
    server_ip = cfg_split[0]
    usetime = timedelta(seconds=0)
    # 최초 실행시간 셋팅
    if cfg_split[2] == "0":
        starttime = datetime.now()
        cfg_split[1] = str(starttime)

        # 윈도우 VM 이름 가져오기
        nodename = platform.node()
        cfg_split[4] = nodename

        # 사용 제한시간 가져오기
        # 사용 제한 시간 셋팅(서버에서 통신해서 가져와야함)
        # [참고] 사용시간이 연장되는 경우 수시 통신을 통해 갱신해야함
        limittime = timedelta(hours=100)
        cfg_split[3] = limittime.total_seconds()

        # 설정 파일 업데이트
        cfg_wdata = cfg_split[0] + "|" + cfg_split[1] + "|" + "0" + "|" + str(cfg_split[3]) + "|" + cfg_split[4]
        print(cfg_wdata)

        cfg_f = open(cfg_file, "w")
        cfg_f.write(cfg_wdata)
        cfg_f.close()
    else:
        usetime = timedelta(seconds=float(cfg_split[2]))



def time_alert(name):
    # 시간에 따른 경고 팝업창 출력
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def sectohms(sec):
    # 초(Seconds)를 시간:분:초 방식으로 변환
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    hms = ("%d:%02d:%02d" % (h, m, s))
    return hms

def usage_timer(usetime):
    # 현재까지 사용시간 확인
    # config.cfg 파일에 사용시간 갱신

    while(1):
        lasttime = datetime.now()
        usetime2 = lasttime - starttime
        inttime = timedelta(seconds=schedule_timer)
        usetime_bak = timedelta(seconds=0)
        usetime_bak = usetime
        #usetime = usetime_bak + inttime
        usetime = usetime + inttime
        print("사용시간", usetime)
        remaintime = limittime-usetime
        #remaintime2는 삭제할 예정(최초 실행시간 기준으로 사용시간을 확인하여 실제 사용시간과 다름(비교목적)
        remaintime2 = limittime - usetime2
        # print("Use Time : ", usetime, "Remain Time : ", remaintime)

        # history 파일 쓰기 및 서버 전송 데이터 형식
        # VM 이름|사용시간|잔여시간
        usetime_sec = usetime.total_seconds()
        usetime_hms = sectohms(usetime_sec)
        remaintime_hms = sectohms(remaintime.total_seconds())
        remaintime_hms2 = sectohms(remaintime2.total_seconds())

        his_data = nodename + "|" + str(starttime) + "|" +  str(usetime_hms) + "|" + str(remaintime_hms) + "|" + str(remaintime_hms2) +"\n"
        print(his_data)
        # history 파일에 사용 기록 저장
        his_f = open(his_file, "a")
        his_f.write(his_data)
        his_f.close()

        # config.cfg에 사용시간 갱신
        cfg_f = open(cfg_file, "r+")
        cfg_data = cfg_f.readline()
        cfg_f.close()
        cfg_split = cfg_data.split("|")
        cfg_split[2] = str(usetime_sec)
        cfg_wdata = cfg_split[0] + "|" + cfg_split[1] + "|" + cfg_split[2] + "|" + str(cfg_split[3]) + "|" + cfg_split[4]
        cfg_f = open(cfg_file, "w")
        cfg_f.write(cfg_wdata)
        cfg_f.close()

        print(timedelta(seconds=float(str(usetime.total_seconds()))))
        # 서버로 사용시간 전송

        # 실행 주기 설정
        sleep(schedule_timer)

if __name__ == '__main__':
#    root = Tk()
#    root.title("test")
#    root.geometry("640x480")
#dPtks    msgbox.showinfo("test", "test information")

    initial_setup()
    usage_timer(usetime)