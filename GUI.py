import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QFrame,QSpinBox, QWidget,QPushButton, QTableWidget,QTableWidgetItem,QCheckBox, QVBoxLayout, QHBoxLayout, QAbstractItemView, QHeaderView, QLabel, QComboBox
from PyQt5.QtCore import Qt
import os
import pandas as pd
import progress
from plyer import notification

dir_ = os.getcwd()
dir_desc_ = os.path.join(dir_, 'data')
COLUMN_NUMBER = 6

class MyApp(QWidget):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setWindowTitle('Instagram Post Scheduler Bot')
        self.setWindowIcon(QtGui.QIcon('images/bot.ico'))
        self.setFixedSize(700, 500)
        self.image_folders = self.get_image_folder_name()
        self.ROW_NUMBER = len(self.image_folders)
        self.caption_folders, self.tag_folders, self.hashtag_folders = self.get_file_names()
        #print(self.get_main_file_names())
        self.dataframe = pd.DataFrame(columns=['credentials','images','captions','tags','hashtags','description'])
        self.checkbox_list = []
        self.combo_box = []
        self.row_list = []
        self.layout = QVBoxLayout()
        self.layout_ = QHBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel('Select Post schedule Interval ')

        self.interval = QSpinBox()
        self.interval.setSuffix(' Hours')
        self.layout_.addWidget(self.label)
        self.layout_.addWidget(self.interval)
        self.layout.addLayout(self.layout_)
        self.combo_box_options = ["Option 1","Option 2","Option 3"]


        self.table = QTableWidget(self.ROW_NUMBER, COLUMN_NUMBER)
        self.table.setStyleSheet('QAbstractItemView::indicator {width: 25px; height 25px;} QTableWidget::item{width:500px; height:40px;}')

        self.layout.addWidget(self.table)
        self.checkbox_list_object = self.fill_table(ROW_NUMBER=self.ROW_NUMBER,
                        image_folders=self.image_folders,
                        caption_folders=self.caption_folders,
                        tag_folders=self.tag_folders,
                        hashtag_folders=self.hashtag_folders)
        self.table.setHorizontalHeaderLabels(['Credentials','Images', 'General Post', 'Captions', 'Hashtags (#)', 'Tags (@)'])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.pb_button = QPushButton('Save Post Tasks', clicked=self.add_task)
        self.layout.addWidget(self.pb_button)




    def add_task(self):
        self.check_general()
        self.check_general()
        if self.interval.value()>0:
            #do something
            self.dataframe['interval'] = self.interval.value()
            self.hide()
            self.close()

    def fill_table(self, ROW_NUMBER, image_folders, caption_folders, tag_folders, hashtag_folders):
        for row in range(ROW_NUMBER):
            for col in range(COLUMN_NUMBER):
                if col==0:
                    combo = QComboBox()
                    self.combo_box.append(combo)
                    for t in self.combo_box_options:
                        combo.addItem(t)
                    self.table.setCellWidget(row, col, combo)
                elif col==1:
                    self.table.setItem(row, col, QTableWidgetItem(image_folders[row]))
                elif col==2:
                    widget = QWidget()
                    checkbox = QCheckBox()
                    self.checkbox_list.append(checkbox)
                    checkbox.toggled.connect(self.check_general)
                    layout = QHBoxLayout(widget)
                    layout.addWidget(checkbox)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0,0,0,0)
                    widget.setLayout(layout)
                    self.table.setCellWidget(row, col, widget)
                elif col==3:
                    self.table.setItem(row,col, QTableWidgetItem(caption_folders[row]))
                elif col==4:
                    self.table.setItem(row,col, QTableWidgetItem(tag_folders[row]))
                elif col==5:
                    self.table.setItem(row,col, QTableWidgetItem(hashtag_folders[row]))


    def check_general(self):
        for row in range(self.table.rowCount()):
            if self.checkbox_list[row].checkState():
                self.table.setItem(row, 3, QTableWidgetItem('main_caption.txt'))
                self.table.setItem(row, 4, QTableWidgetItem('main_hashtag.txt'))
                self.table.setItem(row, 5, QTableWidgetItem('main_tag.txt'))
                self.dataframe.credentials.loc[row] = self.combo_box[row].currentText()
                self.dataframe.tags.loc[row] = 'main_tag.txt'
                self.dataframe.captions.loc[row] = 'main_caption.txt'
                self.dataframe.hashtags.loc[row] = 'main_hashtag.txt'
                self.dataframe.description.loc[row] =self.get_desc(True, row)


            else:
                self.table.setItem(row, 3, QTableWidgetItem(self.caption_folders[row]))
                self.table.setItem(row, 4, QTableWidgetItem(self.tag_folders[row]))
                self.table.setItem(row, 5, QTableWidgetItem(self.hashtag_folders[row]))
                self.dataframe.credentials.loc[row] = self.combo_box[row].currentText()
                self.dataframe.tags.loc[row] = self.tag_folders[row]
                self.dataframe.captions.loc[row] = self.caption_folders[row]
                self.dataframe.hashtags.loc[row] =self.hashtag_folders[row]
                self.dataframe.description.loc[row] =self.get_desc(False, row)
        print(self.dataframe.values)
        self.dataframe.images = self.image_folders


    def get_file(self, file_name):
        content = ''

        try:
            with open(os.path.join(dir_desc_, file_name)) as f:
                content = f.read()
        except Exception:
            print(sys.exc_info())

        return content

    def get_desc(self, condition, row):
        if condition:
            main_caption = self.get_file('main_caption.txt')
            main_hashtag = self.get_file('main_hashtag.txt')
            main_tag = self.get_file('main_tag.txt')
            description = f'{main_caption}...\n{main_tag}\n{main_hashtag}'
        else:
            tag = self.get_file(os.path.join('tag_folder', self.tag_folders[row]))
            hashtag = self.get_file(os.path.join('hashtag_folder', self.hashtag_folders[row]))
            caption = self.get_file(os.path.join('caption_folder', self.caption_folders[row]))
            description = f'{caption}...\n{tag}\n{hashtag}'
        return description

    def get_main_file_names(self):
        m_filenames = next(os.walk(dir_desc_), (None, None, []))[2]
        return m_filenames

    def get_file_names(self):
        c_filenames = next(os.walk(os.path.join(dir_desc_, 'caption_folder')), (None, None, []))[2]
        t_filenames = next(os.walk(os.path.join(dir_desc_, 'tag_folder')), (None, None, []))[2]
        h_filenames = next(os.walk(os.path.join(dir_desc_, 'hashtag_folder')), (None, None, []))[2]
        return c_filenames, t_filenames, h_filenames

    def get_image_folder_name(self):
        img_folder_names = (os.listdir(os.path.join(dir_desc_, 'picture_folder')))
        #print((os.path.join(dir_desc_, 'picture_folder')))
        return img_folder_names

    def closeEvent(self, *args, **kwargs):
        super(MyApp, self).closeEvent(*args, **kwargs)
        print('hey')
        progress.Progress(self.dataframe)

def get_images_count():
    flag = True
    img_folder_names = (os.listdir(os.path.join(dir_desc_, 'picture_folder')))
    for i in img_folder_names:
        if len(os.listdir(os.path.join(os.path.join(dir_desc_, 'picture_folder'),i)))<=10:
            pass
        else:flag = False
    return flag

def get_file_names():
    c_filenames = next(os.walk(os.path.join(dir_desc_, 'caption_folder')), (None, None, []))[2]
    t_filenames = next(os.walk(os.path.join(dir_desc_, 'tag_folder')), (None, None, []))[2]
    h_filenames = next(os.walk(os.path.join(dir_desc_, 'hashtag_folder')), (None, None, []))[2]
    img_folder_names = (os.listdir(os.path.join(dir_desc_, 'picture_folder')))
    if (len(c_filenames) == len(t_filenames)
            and len(c_filenames) == len(h_filenames)
            and len(c_filenames) == len(img_folder_names)):
        return True
    else:
        return False

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyleSheet('''
    QtWidget{
        font-size: 17px;
    }''')
    if (get_file_names() and get_images_count()):
        myApp = MyApp()
        myApp.show()
    elif not get_file_names():

        notification.notify(title='Instagram Post Schedule Bot',
                                message='Relevant folders count does not match. Please Control them and try again!'
                                , app_name='BOT'
                                , app_icon=r'C:\Users\GreyWolf\PycharmProjects\Upwork\images\bot.ico'
                                , timeout=20)
        sys.exit()
    elif not get_images_count():
        notification.notify(title='Instagram Post Schedule Bot',
                            message='There are more than 10 images in one of your files. I can not share that many pictures on Instagram.'
                            , app_name='BOT'
                            , app_icon=r'C:\Users\GreyWolf\PycharmProjects\Upwork\images\bot.ico'
                            , timeout=20)
        sys.exit()
    else:
        notification.notify(title='Instagram Post Schedule Bot',
                            message='Ooops! There is a problem.'
                            , app_name='BOT'
                            , app_icon=r'C:\Users\GreyWolf\PycharmProjects\Upwork\images\bot.ico'
                            , timeout=20)
        sys.exit()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

