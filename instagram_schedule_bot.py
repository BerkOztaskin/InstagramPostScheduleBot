import webbrowser as wb
import os
import pyautogui as pg
import time
import sys
from plyer import notification

NEW_POST = [1330, 120]
CHOOSE_FROM_PC = [915, 665]
FORWARD = [1275, 216]
FORWARD_2 = [1469, 215]
SHARE_POST = [1461, 213]
CANCEL_TO_DELETE = [991, 647]
OPEN_IMAGES = [1718, 999]
FOCUS = [1700,800]
DESCRIPTION = [1300,450]
FORWARD_BUTTON = [1670,180]
dir_ = os.getcwd()

WARNING_BEFORE_RUN = 60 # (SECONDS) YOU CAN CHANGE IT.
chrome_dir = 'C:\Program Files (x86)\Google\Chrome\Application' ## chrome.exe path
path_ = os.path.join(chrome_dir,'chrome.exe')


class Bot:
    def __init__(self, description, image_folder_name):
        self.description = description
        self.image_folder_name = image_folder_name

        try:
            self.notifications(f"Hello there! I will post images in the {self.image_folder_name}"
                               f" folder after {WARNING_BEFORE_RUN} sec! Please DO NOT move mouse when I am running⚠️⚠️", 30)
            self.open_browser2()
            self.upload_images()
            self.share_post()
            self.close_browser()

        except Exception:
            self.close_browser()
            print(f'ERROR OCCURED\n{sys.exc_info()}')


    def share_post(self):
        forward_button = pg.locateCenterOnScreen('images/next_button.png')
        pg.click(forward_button)
        time.sleep(2)
        forward_button2 = pg.locateCenterOnScreen('images/next_button_2.png')
        pg.click(forward_button2)
        time.sleep(0.3)
        pg.click(DESCRIPTION[0], DESCRIPTION[1])
        pg.typewrite(f'{self.description}', 0.05)
        time.sleep(2)
        share_button = pg.locateCenterOnScreen('images/share_button.png')
        pg.click(share_button)
        time.sleep(10)

    def control_images(self):
        pass
    def upload_images(self):
        new_post_button = pg.locateCenterOnScreen('images/new_post_button.png')
        pg.click(new_post_button, duration=1.0, interval=1.0, tween=pg.easeOutElastic)
        time.sleep(2)
        choose_button = pg.locateCenterOnScreen('images/select_from_computer.png')
        pg.click(choose_button, duration=2.0, interval=2.0, tween=pg.easeInBounce)
        time.sleep(2)
        pg.hotkey('WINLEFT', 'RIGHT')
        time.sleep(3)
        pg.hotkey('CTRL', 'l')
        time.sleep(0.3)
        print(os.path.join(os.getcwd(), f'data\\picture_folder\\{self.image_folder_name}'), )
        pg.typewrite(os.path.join(os.getcwd(), f'data\\picture_folder\\{self.image_folder_name}'), 0.02)
        pg.hotkey('ENTER')
        time.sleep(0.3)
        pg.click(FOCUS[0], FOCUS[1], duration=2.0, interval=3.0, tween=pg.easeInOutCirc)
        time.sleep(0.3)
        pg.hotkey('CTRL', 'a')
        time.sleep(0.3)
        pg.click(OPEN_IMAGES[0], OPEN_IMAGES[1], duration=0.5, interval=0.5, tween=pg.easeOutElastic)
        time.sleep(2)

    def open_browser2(self):
        wb.register('chrome', None, wb.BackgroundBrowser(path_))
        wb.get('chrome').open('https://www.instagram.com')
        time.sleep(1.5)
        pg.hotkey('WINLEFT', 'UP')
        pg.click(x=100, y=300, duration=2.0, interval=2.0, tween=pg.easeOutElastic)
        time.sleep(3)

    def open_browser(self):
        time.sleep(10)
        pg.hotkey('WINLEFT')
        time.sleep(2)
        pg.typewrite('chrome\n', 0.02)
        pg.hotkey('Enter')
        time.sleep(2)
        pg.hotkey('CTRL', 'l')
        pg.typewrite('https://www.instagram.com\n', 0.02)
        pg.hotkey('WINLEFT', 'UP')
        pg.click(x=100, y=400, duration=2.0, interval=2.0, tween=pg.easeOutElastic)
        time.sleep(3)

    def notifications(self, msg, duration=3):
        notification.notify(title='Instagram Post Schedule Bot',
                            message=f'{msg}'
                            , app_name='BOT'
                            , app_icon=r'C:\Users\GreyWolf\PycharmProjects\Upwork\images\bot.ico'
                            , timeout=duration)
        time.sleep(WARNING_BEFORE_RUN)

    def close_browser(self):
        pg.hotkey('CTRL','W')