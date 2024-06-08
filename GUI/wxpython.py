#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import time
import threading
import datetime
import mysql
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FC


connection = mysql.connect_to_mysql('liuguangsen')
mysql.create_database(connection)
mysql.use_database(connection)
mysql.create_table(connection)

class HoverImageButton(wx.Button):
    def __init__(self, parent, bitmap, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER):
        super(HoverImageButton, self).__init__(parent, id, "", pos, size, style)
        self.bitmap = bitmap
        self.bitmap_hover = bitmap.Scale(bitmap.GetWidth() * 1.2, bitmap.GetHeight() * 1.2,
                                         wx.IMAGE_QUALITY_HIGH)  # 放大后的图片
        self.is_hovered = False
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

    def OnMouseEnter(self, event):
        self.is_hovered = True
        self.Refresh()

    def OnMouseLeave(self, event):
        self.is_hovered = False
        self.Refresh()

    def DoDraw(self, dc):
        if self.is_hovered:
            bitmap = self.bitmap_hover
        else:
            bitmap = self.bitmap

            # 绘制图片到按钮上
        dc.DrawBitmap(bitmap, 0, 0, True)

    def Refresh(self, eraseBackground=True, rect=None):
        dc = wx.BufferedPaintDC(self)
        self.DoDraw(dc)


def pic_button(parent, pic_path,pos=(0,0),size=(0,0)):
    # 加载图片为wx.Image对象
    image = wx.Image(pic_path, wx.BITMAP_TYPE_ANY)
    # 计算图片的原始宽高比
    width, height = image.GetSize()
    aspect_ratio = width / float(height)
    # 根据目标尺寸和宽高比计算缩放后的尺寸
    if size[0] / aspect_ratio < size[1]:
        # 如果宽度是限制因素
        new_width = size[0]
        new_height = int(new_width / aspect_ratio)
    else:
        # 如果高度是限制因素
        new_height = size[1]
        new_width = int(new_height * aspect_ratio)
        # 缩放图片
    image = image.Rescale(new_width, new_height, wx.IMAGE_QUALITY_HIGH)
    # 将缩放后的图片转换为位图
    bitmap = wx.Bitmap(image)
    # 创建位图按钮
    button = wx.BitmapButton(parent, wx.ID_ANY, bitmap, pos=pos, size=size)
    return button


class BackgroundPanel(wx.Panel):
    def __init__(self, parent, image_path, **kwargs):
        super(BackgroundPanel, self).__init__(parent, **kwargs)
        self.image_path = image_path
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self._bitmap = None

    def OnSize(self, event):
        self.LoadBitmap()

    def LoadBitmap(self):
        # 加载图片
        image = wx.Image(self.image_path, wx.BITMAP_TYPE_ANY)
        # 直接转换为位图
        self._bitmap = image.ConvertToBitmap()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        if self._bitmap:
            # 获取面板和图片的尺寸
            panel_width, panel_height = self.GetSize()
            bitmap_width, bitmap_height = self._bitmap.GetWidth(), self._bitmap.GetHeight()
            dc.DrawBitmap(self._bitmap, 0, 0)



def insert_image(window, image_path, size=(100, 100), position=(10, 10)):
    image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
    image = image.Scale(size[0], size[1], wx.IMAGE_QUALITY_HIGH)
    bitmap = image.ConvertToBitmap()
    static_bitmap = wx.StaticBitmap(window, wx.ID_ANY, bitmap, position)
    return static_bitmap




class MainFrame(wx.Frame):
    def __init__(self,parent,title):
        super(MainFrame,self).__init__(parent,title="VITA",size=(1300,1000))
        self.Centre()
        bg_panel = BackgroundPanel(self, "1.png")

        btn1 = wx.Button(bg_panel, -1, 'Drink water', pos=(110, 200),size=(100, 70))
        btn1.Bind(wx.EVT_BUTTON, lambda event:self.on_open_sub_frame_water('Drink water'))
        btn1.SetBackgroundColour(wx.Colour(255, 255, 255))

        image_path1 = "6.png"  # 替换为你的图片路径
        insert_image(bg_panel, image_path1, size=(90, 70), position=(20, 200))

        btn2 = wx.Button(bg_panel, -1, 'Exercise', pos=(110, 400), size=(100, 70))
        btn2.Bind(wx.EVT_BUTTON, lambda event:self.on_open_sub_frame_sports('Exercise'))
        btn2.SetBackgroundColour(wx.Colour(255, 255, 255))

        image_path2 = "7.png"  # 替换为你的图片路径
        insert_image(bg_panel, image_path2, size=(90, 70), position=(20, 400))

        btn3 = wx.Button(bg_panel, -1, 'Sleep', pos=(110, 600), size=(100, 70))
        btn3.Bind(wx.EVT_BUTTON, lambda event:self.on_open_sub_frame_sleep('Sleep'))
        btn3.SetBackgroundColour(wx.Colour(255, 255, 255))

        image_path3 = "8.png"  # 替换为你的图片路径
        insert_image(bg_panel, image_path3, size=(90, 70), position=(20, 600))

        btn4 = wx.Button(bg_panel, -1, 'personal centre', pos=(110, 800), size=(100, 70))
        btn4.Bind(wx.EVT_BUTTON, lambda event:self.on_open_sub_frame_personal_centre('personal centre'))
        btn4.SetBackgroundColour(wx.Colour(255, 255, 255))

        image_path4 = "9.png"  # 替换为你的图片路径
        insert_image(bg_panel, image_path4, size=(90, 70), position=(20, 800))

        btn_exit = wx.Button(bg_panel, -1, 'Exit', pos=(1100, 800), size=(100, 70))
        btn_exit.Bind(wx.EVT_BUTTON, self.on_exit)
        btn_exit.SetBackgroundColour(wx.Colour(255, 255, 255))


        self.figure = plt.figure()
        self.canvas = FC(bg_panel, -1, self.figure)
        mysql.drink_data_histogram(connection)
        self.canvas.SetSize(500,500)
        self.canvas.Move(200,200)










    def on_close(self,event):
        # 关闭子窗口
        self.Close()
        self.Show()

    def on_exit(self, event):
        self.Close()






















    def on_open_sub_frame_water(self, title):
        sub_frame = wx.Frame(self, title=title, size=(1300, 1000))
        sub_panel = BackgroundPanel(sub_frame, "10.png")
        sub_sub_panel = BackgroundPanel(sub_panel, "14.png")
        sub_sub_panel.SetSize((450, 700))  # 宽度200像素，高度100像素
        sub_sub_panel.SetPosition((850, 70))  # x坐标50像素，y坐标50像素


        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        static_text1 = wx.StaticText(sub_panel,
                                     label='Please select the drink you want to record by clicking on the icon below:',
                                     pos=(150, 25))
        static_text1.SetBackgroundColour(wx.Colour(180, 230, 240))
        static_text1.SetFont(font)

        btn_coke = pic_button(sub_panel, "2.png", pos=(200, 65), size=(100, 140))
        btn_coke.SetBackgroundColour(wx.Colour(180, 230, 240))
        btn_coke.Bind(wx.EVT_BUTTON, self.coke_button_click)

        font2 = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        static_text2 = wx.StaticText(sub_panel, label='coke', pos=(170, 225))
        static_text2.SetBackgroundColour(wx.Colour(215, 250, 255))
        static_text2.SetFont(font)

        btn_water = pic_button(sub_panel, "3.png", pos=(350, 65), size=(100, 140))
        btn_water.SetBackgroundColour(wx.Colour(180, 230, 240))
        btn_water.Bind(wx.EVT_BUTTON, self.water_button_click)

        static_text3 = wx.StaticText(sub_panel, label='water', pos=(380, 225))
        static_text3.SetBackgroundColour(wx.Colour(215, 250, 255))
        static_text3.SetFont(font)

        btn_beer = pic_button(sub_panel, "4.png", pos=(500, 65), size=(100, 140))
        btn_beer.SetBackgroundColour(wx.Colour(180, 230, 240))
        btn_beer.Bind(wx.EVT_BUTTON, self.beer_button_click)

        static_text4 = wx.StaticText(sub_panel, label='Beer', pos=(530, 225))
        static_text4.SetBackgroundColour(wx.Colour(215, 250, 255))
        static_text4.SetFont(font)

        btn_milk = pic_button(sub_panel, "5.png", pos=(650, 65), size=(100, 140))
        btn_milk.SetBackgroundColour(wx.Colour(180, 230, 240))
        btn_milk.Bind(wx.EVT_BUTTON, self.milk_button_click)

        static_text5 = wx.StaticText(sub_panel, label='Milk', pos=(680, 225))
        static_text5.SetBackgroundColour(wx.Colour(215, 250, 255))
        static_text5.SetFont(font)

        self.static_text = wx.StaticText(sub_panel, label="Please select the drink you want to record!", pos=(200, 300))
        self.static_text.SetFont(font)
        self.static_text.SetBackgroundColour(wx.Colour(215, 250, 255))

        self.static_text2 = wx.StaticText(sub_panel, label=" ", pos=(200, 450))
        self.static_text2.SetFont(font)
        self.static_text2.SetBackgroundColour(wx.Colour(255, 255, 255))

        # 创建输入框并禁用
        self.input_box = wx.TextCtrl(sub_panel, pos=(300, 375), style=wx.TE_PROCESS_ENTER | wx.TE_LEFT)
        self.input_box.Disable()

        self.btn_submit = wx.Button(sub_panel, label='Record', pos=(500, 350),size=(100, 70))
        self.btn_submit.Disable()
        self.btn_submit.Bind(wx.EVT_BUTTON, self.record_click)
        self.btn_submit.SetBackgroundColour(wx.Colour(255, 255, 255))

        static_text6 = wx.StaticText(sub_panel, label='History', pos=(1000, 25))
        static_text6.SetBackgroundColour(wx.Colour(180, 230, 240))
        static_text6.SetFont(font2)

        self.static_text8 = wx.StaticText(sub_panel, label="There are no records now!", pos=(900, 70))
        self.static_text8.SetFont(font)

        data_latest20 = mysql.print_drink_data_latest20(connection)
        self.static_text8.SetLabel(data_latest20)




        static_text7 = wx.StaticText(sub_panel, label='Water reminder', pos=(360, 500))
        static_text7.SetBackgroundColour(wx.Colour(255, 255, 255))
        static_text7.SetFont(font2)

        font3 = wx.Font(32, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.static_text3 = wx.StaticText(sub_panel, label="HOUR", pos=(320, 550))
        self.static_text3.SetFont(font)
        self.static_text3.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.static_text4 = wx.StaticText(sub_panel, label="MINUTE", pos=(520, 550))
        self.static_text4.SetFont(font)
        self.static_text4.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.timer_label = wx.StaticText(sub_panel, label="00:00", pos=(400, 700))
        self.timer_label.SetFont(font3)
        self.start_button = wx.Button(sub_panel, label="Start", pos=(300, 800),size=(100, 70))
        self.start_button.Bind(wx.EVT_BUTTON, self.start_countdown)
        self.start_button.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.reload_button = wx.Button(sub_panel, label="Reset", pos=(500, 800),size=(100, 70))
        self.reload_button.Bind(wx.EVT_BUTTON, self.reload)
        self.reload_button.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.hour_choice = wx.Choice(sub_panel, choices=[str(i) for i in range(24)], pos=(300, 600),size=(100, 70))
        self.hour_choice.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.minute_choice = wx.Choice(sub_panel, choices=[str(i) for i in range(60)], pos=(500, 600),size=(100, 70))
        self.minute_choice.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.timer_running = False

        btn_close = wx.Button(sub_panel, wx.ID_ANY, 'Back', pos=(950, 800), size=(100, 70))
        btn_close.Bind(wx.EVT_BUTTON, lambda event: (sub_frame.Close(), self.Show()))
        btn_close.SetBackgroundColour(wx.Colour(255, 255, 255))
        btn_exit = wx.Button(sub_panel, -1, 'Exit', pos=(1100, 800), size=(100, 70))
        btn_exit.Bind(wx.EVT_BUTTON, self.on_exit)
        btn_exit.SetBackgroundColour(wx.Colour(255, 255, 255))
        sub_frame.Centre()
        sub_frame.Show()

    def coke_button_click(self, event):
        # 在点击按钮后更新静态文本
        self.static_text.SetLabel("Please enter how many milliliters of coke you drink:")
        self.input_box.Enable()
        self.btn_submit.Enable()

    def water_button_click(self, event):
        # 在点击按钮后更新静态文本
        self.static_text.SetLabel("Please enter how many milliliters of water you drink:")
        self.input_box.Enable()
        self.btn_submit.Enable()

    def beer_button_click(self, event):
        # 在点击按钮后更新静态文本
        self.static_text.SetLabel("Please enter how many milliliters of beer you drink:")
        self.input_box.Enable()
        self.btn_submit.Enable()

    def milk_button_click(self, event):
        # 在点击按钮后更新静态文本
        self.static_text.SetLabel("Please enter how many milliliters of milk you drink:")
        self.input_box.Enable()
        self.btn_submit.Enable()

    def record_click(self, event):
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        input_text = self.input_box.GetValue()
        current_text = self.static_text.GetLabel()
        drink_type = ""
        if current_text == "Please enter how many milliliters of coke you drink:":
            drink_type = "coke"
        elif current_text == "Please enter how many milliliters of water you drink:":
            drink_type = "water"
        elif current_text == "Please enter how many milliliters of beer you drink:":
            drink_type = "beer"
        elif current_text == "Please enter how many milliliters of milk you drink:":
            drink_type = "milk"

        try:
            input_value = int(input_text)
            if input_value < 0 or input_value > 2000:
                self.static_text2.SetLabel("Please enter a valid intake amount (0-2000 milliliters)!")
            else:
                self.static_text2.SetLabel("Record successfully!")
                print("日期时间：", date_time)
                print("用户输入的内容：", input_text)
                print("饮料类型：", drink_type)
                mysql.insert_drink_data(connection,drink_type,input_text)
        except ValueError:
            self.static_text2.SetLabel("Please enter a valid integer value for intake amount!")
        data_latest20 = mysql.print_drink_data_latest20(connection)
        self.static_text8.SetLabel(data_latest20)





    def start_countdown(self, event):
        hours = int(self.hour_choice.GetString(self.hour_choice.GetSelection()))
        minutes = int(self.minute_choice.GetString(self.minute_choice.GetSelection()))
        total_seconds = hours * 3600 + minutes * 60
        self.start_button.Disable()
        self.reload_button.Enable()
        self.timer_running = True
        t = threading.Thread(target=self.countdown, args=(total_seconds,))
        t.start()


    def reload(self, event):
        self.start_button.Enable()
        self.reload_button.Disable()
        self.timer_running = False
        self.timer_label.SetLabel("00:00")


    def countdown(self, total_seconds):
        for i in range(total_seconds, -1, -1):
            if not self.timer_running:
                break
            minutes, seconds = divmod(i, 60)
            timeformat = '{:02d}:{:02d}'.format(minutes, seconds)
            wx.CallAfter(self.update_timer, timeformat)
            time.sleep(1)
        if self.timer_running:
            wx.CallAfter(self.show_alert_water)

    def update_timer(self, timeformat):
        self.timer_label.SetLabel(timeformat)

    def show_alert_water(self):
        wx.MessageBox("Time's up！", "Remind")


    def start_timer3(self, event2):
        if not self.timer_running2:
            if self.last_stop_time2 > 0:
                self.start_time2 = time.time() - self.elapsed_time2
            else:
                self.start_time2 = time.time()
            self.timer_running2 = True
            self.timer_thread2 = threading.Thread(target=self.update_timer2)
            self.timer_thread2.daemon = True
            self.timer_thread2.start()
            self.static_text4.SetLabel("You can time you sleep now!")






    def finish_timer3(self, event2):
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        if self.timer_running2:
            self.stop_timer2(event2)
        if self.format_time2(self.elapsed_time2) == 0 :
            self.static_text4.SetLabel("Too quick to record!")
        else:
            self.static_text4.SetLabel("Record successfully! Click start to record more!")
            print("日期时间：", date_time)
            print("睡眠时长：", self.format_time2(self.elapsed_time2))
        self.elapsed_time2 = 0
        self.start_time2 = 0
        self.last_stop_time2 = 0
        self.timer_label2.SetLabel("00:00:00")







    def on_open_sub_frame_sleep(self, title):
        sub_frame = wx.Frame(self, title=title, size=(1300, 1000))
        sub_panel = BackgroundPanel(sub_frame, "11.png")
        font2 = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        static_text8 = wx.StaticText(sub_panel, label='Sports reminder', pos=(330, 300))
        static_text8.SetBackgroundColour(wx.Colour(230, 250, 230))
        static_text8.SetFont(font2)

        font3 = wx.Font(32, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.timer_label = wx.StaticText(sub_panel, label="00:00", pos=(400, 500))
        self.timer_label.SetFont(font3)
        self.start_button = wx.Button(sub_panel, label="Start", pos=(300, 600), size=(100, 70))
        self.start_button.Bind(wx.EVT_BUTTON, self.start_countdown)
        self.start_button.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.reload_button = wx.Button(sub_panel, label="Reset", pos=(500, 600), size=(100, 70))
        self.reload_button.Bind(wx.EVT_BUTTON, self.reload)
        self.reload_button.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.hour_choice = wx.Choice(sub_panel, choices=[str(i) for i in range(24)], pos=(300, 400), size=(100, 70))
        self.hour_choice.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.minute_choice = wx.Choice(sub_panel, choices=[str(i) for i in range(60)], pos=(500, 400), size=(100, 70))
        self.minute_choice.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.timer_running = False


        self.static_text4 = wx.StaticText(sub_panel, label="You can time you sleep now!",
                                          pos=(650, 300))
        self.static_text4.SetFont(font2)
        self.static_text4.SetBackgroundColour(wx.Colour(230, 250, 230))
        self.timer_label2 = wx.StaticText(sub_panel, label="00:00:00", pos=(750, 500))
        self.timer_label2.SetFont(font3)
        self.start_button2 = wx.Button(sub_panel, label="Start", pos=(700, 400), size=(100, 70))
        self.start_button2.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.stop_button2 = wx.Button(sub_panel, label="Stop", pos=(900, 400), size=(100, 70))
        self.stop_button2.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.continue_button2 = wx.Button(sub_panel, label="Continue", pos=(700, 600), size=(100, 70))
        self.continue_button2.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.finish_button2 = wx.Button(sub_panel, label="Finish", pos=(900, 600), size=(100, 70))
        self.finish_button2.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.start_button2.Bind(wx.EVT_BUTTON, self.start_timer3)
        self.stop_button2.Bind(wx.EVT_BUTTON, self.stop_timer2)
        self.continue_button2.Bind(wx.EVT_BUTTON, self.continue_timer2)
        self.finish_button2.Bind(wx.EVT_BUTTON, self.finish_timer3)

        self.timer_running2 = False
        self.elapsed_time2 = 0
        self.start_time2 = 0
        self.last_stop_time2 = 0
        self.timer_thread2 = None









        btn_close = wx.Button(sub_panel, wx.ID_ANY, 'Back', pos=(950, 800), size=(100, 70))
        btn_close.Bind(wx.EVT_BUTTON, lambda event: (sub_frame.Close(), self.Show()))
        btn_close.SetBackgroundColour(wx.Colour(255, 255, 255))
        btn_exit = wx.Button(sub_panel, -1, 'Exit', pos=(1100, 800), size=(100, 70))
        btn_exit.Bind(wx.EVT_BUTTON, self.on_exit)
        btn_exit.SetBackgroundColour(wx.Colour(255, 255, 255))
        sub_frame.Centre()
        sub_frame.Show()





    def start_timer2(self, event2):
        if not self.timer_running2:
            if self.last_stop_time2 > 0:
                self.start_time2 = time.time() - self.elapsed_time2
            else:
                self.start_time2 = time.time()
            self.timer_running2 = True
            self.timer_thread2 = threading.Thread(target=self.update_timer2)
            self.timer_thread2.daemon = True
            self.timer_thread2.start()

    def stop_timer2(self, event2):
        if self.timer_running2:
            self.timer_running2 = False
            self.last_stop_time2 = time.time()

    def continue_timer2(self, event2):
        if not self.timer_running2:
            self.start_timer2(event2)


    def finish_timer2(self, event2):
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        if self.timer_running2:
            self.stop_timer2(event2)

        current_text = self.static_text3.GetLabel()
        sport_type = ""

        if current_text == "It's time to start timing your walks!":
            sport_type = "walk"
        elif current_text == "It's time to start timing your run!":
            sport_type = "run"
        elif current_text == "It's time to start timing your cycling!":
            sport_type = "cycle"
        elif current_text == "It's time to start timing your playing basketball!":
            sport_type = "basketball"
        elif current_text == "It's time to start timing your playing football!":
            sport_type = "football"
        elif current_text == "It's time to start timing your swimming!":
            sport_type = "swim"

        if self.format_time2(self.elapsed_time2) == 0 :
            self.static_text3.SetLabel("Too quick to record!")
        else:
            self.static_text3.SetLabel("Record successfully! Select sport to to unlock  buttons!")
            print("日期时间：", date_time)
            print("运动时长：", self.format_time2(self.elapsed_time2))
            print("运动类型：", sport_type)

        mysql.insert_exercise_data(connection,sport_type,self.format_time2(self.elapsed_time2))

        self.elapsed_time2 = 0
        self.start_time2 = 0
        self.last_stop_time2 = 0
        self.timer_label2.SetLabel("00:00:00")
        self.start_button2.Disable()
        self.stop_button2.Disable()
        self.continue_button2.Disable()
        self.finish_button2.Disable()




    def update_timer2(self):
        while self.timer_running2:
            self.elapsed_time2 = time.time() - self.start_time2
            self.timer_label2.SetLabel(self.format_time2(self.elapsed_time2))
            time.sleep(1)

    def format_time2(self, elapsed2):
        hours2 = int(elapsed2 / 3600)
        minutes2 = int((elapsed2 % 3600) / 60)
        seconds2 = int(elapsed2 % 60)
        return f"{hours2:02d}:{minutes2:02d}:{seconds2:02d}"


    def walk_button_click(self, event):
        # 在点击按钮后更新静态文本
        self.static_text3.SetLabel("It's time to start timing your walks!")
        self.start_button2.Enable()
        self.stop_button2.Enable()
        self.finish_button2.Enable()
        self.continue_button2.Enable()

    def run_button_click(self, event):
        # 在点击按钮后更新静态文本
        self.static_text3.SetLabel("It's time to start timing your run!")
        self.start_button2.Enable()
        self.stop_button2.Enable()
        self.finish_button2.Enable()
        self.continue_button2.Enable()

    def cycle_button_click(self, event):
        # 在点击按钮后更新静态文本
        self.static_text3.SetLabel("It's time to start timing your cycling!")
        self.start_button2.Enable()
        self.stop_button2.Enable()
        self.finish_button2.Enable()
        self.continue_button2.Enable()

    def bask_button_click(self, event):
        # 在点击按钮后更新静态文本
        self.static_text3.SetLabel("It's time to start timing your playing basketball!")
        self.start_button2.Enable()
        self.stop_button2.Enable()
        self.finish_button2.Enable()
        self.continue_button2.Enable()

    def foot_button_click(self, event):
        # 在点击按钮后更新静态文本
        self.static_text3.SetLabel("It's time to start timing your playing football!")
        self.start_button2.Enable()
        self.stop_button2.Enable()
        self.finish_button2.Enable()
        self.continue_button2.Enable()

    def swim_button_click(self, event):
        # 在点击按钮后更新静态文本
        self.static_text3.SetLabel("It's time to start timing your swimming!")
        self.start_button2.Enable()
        self.stop_button2.Enable()
        self.finish_button2.Enable()
        self.continue_button2.Enable()


    def on_open_sub_frame_sports(self, title):
        sub_frame = wx.Frame(self, title=title, size=(1300, 1000))
        sub_panel = BackgroundPanel(sub_frame, "12.png")

        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        static_text1 = wx.StaticText(sub_panel,
                                     label='Please select the sport you want to record by clicking on the icon below:',
                                     pos=(150, 25))
        static_text1.SetBackgroundColour(wx.Colour(240, 240, 130))
        static_text1.SetFont(font)

        btn_walk = pic_button(sub_panel, "15.png", pos=(200, 65), size=(100, 140))
        btn_walk.SetBackgroundColour(wx.Colour(240, 240, 130))
        btn_walk.Bind(wx.EVT_BUTTON, self.walk_button_click)

        font2 = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        static_text2 = wx.StaticText(sub_panel, label='Walk', pos=(230, 225))
        static_text2.SetBackgroundColour(wx.Colour(250, 250, 180))
        static_text2.SetFont(font)

        btn_run = pic_button(sub_panel, "16.png", pos=(350, 65), size=(100, 140))
        btn_run.SetBackgroundColour(wx.Colour(240, 240, 130))
        btn_run.Bind(wx.EVT_BUTTON, self.run_button_click)

        static_text3 = wx.StaticText(sub_panel, label='Run', pos=(380, 225))
        static_text3.SetBackgroundColour(wx.Colour(250, 250, 180))
        static_text3.SetFont(font)

        btn_cycle = pic_button(sub_panel, "17.png", pos=(500, 65), size=(100, 140))
        btn_cycle.SetBackgroundColour(wx.Colour(240, 240, 130))
        btn_cycle.Bind(wx.EVT_BUTTON, self.cycle_button_click)

        static_text4 = wx.StaticText(sub_panel, label='Cycle', pos=(530, 225))
        static_text4.SetBackgroundColour(wx.Colour(250, 250, 180))
        static_text4.SetFont(font)

        btn_bask = pic_button(sub_panel, "18.png", pos=(650, 65), size=(100, 140))
        btn_bask.SetBackgroundColour(wx.Colour(240, 240, 130))
        btn_bask.Bind(wx.EVT_BUTTON, self.bask_button_click)

        static_text5 = wx.StaticText(sub_panel, label='Basketball', pos=(650, 225))
        static_text5.SetBackgroundColour(wx.Colour(250, 250, 180))
        static_text5.SetFont(font)

        btn_foot = pic_button(sub_panel, "19.png", pos=(800, 65), size=(100, 140))
        btn_foot.SetBackgroundColour(wx.Colour(240, 240, 130))
        btn_foot.Bind(wx.EVT_BUTTON, self.foot_button_click)


        static_text6 = wx.StaticText(sub_panel, label='Football', pos=(810, 225))
        static_text6.SetBackgroundColour(wx.Colour(250, 250, 180))
        static_text6.SetFont(font)

        btn_swim = pic_button(sub_panel, "20.png", pos=(950, 65), size=(100, 140))
        btn_swim.SetBackgroundColour(wx.Colour(240, 240, 130))
        btn_swim.Bind(wx.EVT_BUTTON, self.swim_button_click)

        static_text7 = wx.StaticText(sub_panel, label='Swim', pos=(980, 225))
        static_text7.SetBackgroundColour(wx.Colour(250, 250, 180))
        static_text7.SetFont(font)

        static_text8 = wx.StaticText(sub_panel, label='Sports reminder', pos=(160, 300))
        static_text8.SetBackgroundColour(wx.Colour(250, 250, 180))
        static_text8.SetFont(font2)

        font3 = wx.Font(32, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.timer_label = wx.StaticText(sub_panel, label="00:00", pos=(200, 500))
        self.timer_label.SetFont(font3)

        self.start_button = wx.Button(sub_panel, label="Start", pos=(100, 600), size=(100, 70))
        self.start_button.Bind(wx.EVT_BUTTON, self.start_countdown)
        self.start_button.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.reload_button = wx.Button(sub_panel, label="Reset", pos=(300, 600), size=(100, 70))
        self.reload_button.Bind(wx.EVT_BUTTON, self.reload)
        self.reload_button.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.hour_choice = wx.Choice(sub_panel, choices=[str(i) for i in range(24)], pos=(100, 400), size=(100, 70))
        self.hour_choice.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.minute_choice = wx.Choice(sub_panel, choices=[str(i) for i in range(60)], pos=(300, 400), size=(100, 70))
        self.minute_choice.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.timer_running1 = False



        self.static_text3 = wx.StaticText(sub_panel, label="Please select the sport you want to record!", pos=(450, 300))
        self.static_text3.SetFont(font)
        self.static_text3.SetBackgroundColour(wx.Colour(250, 250, 180))
        self.timer_label2 = wx.StaticText(sub_panel, label="00:00:00", pos=(550, 500))
        self.timer_label2.SetFont(font3)
        self.start_button2 = wx.Button(sub_panel, label="Start", pos=(500, 400),size=(100, 70))
        self.start_button2.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.start_button2.Disable()
        self.stop_button2 = wx.Button(sub_panel, label="Stop", pos=(700, 400),size=(100, 70))
        self.stop_button2.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.stop_button2.Disable()
        self.continue_button2 = wx.Button(sub_panel, label="Continue", pos=(500, 600),size=(100, 70))
        self.continue_button2.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.continue_button2.Disable()
        self.finish_button2 = wx.Button(sub_panel, label="Finish", pos=(700, 600),size=(100, 70))
        self.finish_button2.Disable()
        self.finish_button2.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.start_button2.Bind(wx.EVT_BUTTON, self.start_timer2)
        self.stop_button2.Bind(wx.EVT_BUTTON, self.stop_timer2)
        self.continue_button2.Bind(wx.EVT_BUTTON, self.continue_timer2)
        self.finish_button2.Bind(wx.EVT_BUTTON, self.finish_timer2)

        self.timer_running2 = False
        self.elapsed_time2 = 0
        self.start_time2 = 0
        self.last_stop_time2 = 0
        self.timer_thread2 = None

        static_text9 = wx.StaticText(sub_panel, label='Calories burned today', pos=(900, 400))
        static_text9.SetBackgroundColour(wx.Colour(250, 250, 180))
        static_text9.SetFont(font2)









        btn_close = wx.Button(sub_panel, wx.ID_ANY, 'Back', pos=(950, 800), size=(100, 70))
        btn_close.Bind(wx.EVT_BUTTON, lambda event: (sub_frame.Close(), self.Show()))
        btn_close.SetBackgroundColour(wx.Colour(255, 255, 255))
        btn_exit = wx.Button(sub_panel, -1, 'Exit', pos=(1100, 800), size=(100, 70))
        btn_exit.Bind(wx.EVT_BUTTON, self.on_exit)
        btn_exit.SetBackgroundColour(wx.Colour(255, 255, 255))
        sub_frame.Centre()
        sub_frame.Show()














    def on_open_sub_frame_personal_centre(self, title):
        sub_frame = wx.Frame(self, title=title, size=(1300, 1000))
        sub_panel = BackgroundPanel(sub_frame, "13.png")
        btn_close = wx.Button(sub_panel, wx.ID_ANY, 'Back', pos=(950, 800), size=(100, 70))
        btn_close.Bind(wx.EVT_BUTTON, lambda event: (sub_frame.Close(), self.Show()))
        btn_close.SetBackgroundColour(wx.Colour(255, 255, 255))
        btn_exit = wx.Button(sub_panel, -1, 'Exit', pos=(1100, 800), size=(100, 70))
        btn_exit.Bind(wx.EVT_BUTTON, self.on_exit)
        btn_exit.SetBackgroundColour(wx.Colour(255, 255, 255))
        sub_frame.Centre()
        sub_frame.Show()







if __name__ == '__main__':
    vita = wx.App()
    frame = MainFrame(None,title="vita")
    frame.Show()
    vita.MainLoop()
