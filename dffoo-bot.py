import pywinauto 
from pathlib import Path
import os
import winsound 
from mss.windows import MSS as mss
from time import sleep
import win32api, win32con
import cv2
import numpy as np

def leftClick(cx, cy):
    pywinauto.mouse.move((cx, cy))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def get_cords():
    x,y = win32api.GetCursorPos()
    print(x,y)

def make_gray_array(screen_grab):
    return cv2.cvtColor(np.array(screen_grab), cv2.COLOR_RGB2GRAY)

def search_img(img_gray, template):
    res = cv2.matchTemplate(img_gray,template,cv2.TM_SQDIFF)
    min_val = cv2.minMaxLoc(res)[0]
    if min_val < 10000000: 
        return True

def act(grab, template, cx, cy):
    if search_img(grab, template):
        leftClick(cx, cy)
        return True
    return False

def get_templates():
    raw_templates = [
        ('Confirm_Data_Download', 2782, 586),
        ('Skip_Cutscene', 3249, 94),
        ('Go_To_Support_Select', 3080, 752),
        ('Select_Support', 2609, 205),
        ('Begin_Battle', 3080, 752),
        ('Gau_Second_Skill', 3202, 555),
        ('Accept_Reward', 3168, 764),
    ]

    templates = []

    for r in raw_templates:
        template = cv2.imread(f'./templates/{r[0]}.png',0)
        cx = r[1]
        cy = r[2]
        templates.append((template, cx, cy))
    
    return templates

def get_player_name_template():
    return cv2.imread(f'./templates/Player_Name.png',0)
 
def main():
    sct = mss()
    monitor = sct.monitors[-1]

    Done = False

    wd = Path(os.getcwd())
    mp3 = str(wd / "your-turn.wav")

    Player_Name = get_player_name_template()
    templates = get_templates()

    while True:
        sct_img = sct.grab(monitor)
        gray_img = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGRA2GRAY)


        if search_img(gray_img, Player_Name) and not Done:
            winsound.PlaySound(mp3, winsound.SND_ASYNC)
            Done = True
        
        if Done:
            sleep(7)

        for ss in templates:
            if act(gray_img, *ss):
                Done = False
                sleep(1.5)
                continue

        sleep(1.5)

 
if __name__ == '__main__':
    main()
    # get_cords()
