import time
import instagram_schedule_bot as bot
import os
import sys
from plyer import notification

dir_ = os.getcwd()
dir_desc_ = os.path.join(dir_, 'data')

class Progress:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.tasks()

    def tasks(self):
        self.notifications('Hello There! I am alive ! 🤖 ')
        for row in range(self.dataframe.shape[0]):
            tasks_list = list(self.dataframe.loc[row])
            #time.sleep(60)
            #print(tasks_list)
            #print(f'{tasks_list[0]} will share.')
            #print(f'{tasks_list[4]}')

            bot.Bot(tasks_list[4], tasks_list[0])
            time.sleep(int(tasks_list[0][-1])*60*60)

    def notifications(self, msg, duration=30):
        notification.notify(title='Instagram Post Schedule Bot',
                            message=f'{msg}'
                            , app_name='BOT'
                            , app_icon=r'C:\Users\GreyWolf\PycharmProjects\Upwork\images\bot.ico'
                            , timeout=duration)
