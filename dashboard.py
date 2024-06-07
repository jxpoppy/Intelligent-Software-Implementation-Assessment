import wx
import matplotlib.pyplot as plt
from datetime import datetime
import mysql.connector

class VitaApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, title="Vita Health Management Software")
        self.SetTopWindow(frame)
        frame.Show()
        return True

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Adding a simple menu
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # Dashboard Panel
        self.dashboard_panel = wx.Panel(panel)
        dashboard_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.water_btn = wx.Button(self.dashboard_panel, label="Water")
        self.sleep_btn = wx.Button(self.dashboard_panel, label="Sleep")
        self.exercise_btn = wx.Button(self.dashboard_panel, label="Exercise")
        self.profile_btn = wx.Button(self.dashboard_panel, label="Profile")

        dashboard_sizer.Add(self.water_btn, 1, wx.EXPAND|wx.ALL, 5)
        dashboard_sizer.Add(self.sleep_btn, 1, wx.EXPAND|wx.ALL, 5)
        dashboard_sizer.Add(self.exercise_btn, 1, wx.EXPAND|wx.ALL, 5)
        dashboard_sizer.Add(self.profile_btn, 1, wx.EXPAND|wx.ALL, 5)

        self.dashboard_panel.SetSizer(dashboard_sizer)

        vbox.Add(self.dashboard_panel, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_BUTTON, self.OnWater, self.water_btn)
        self.Bind(wx.EVT_BUTTON, self.OnSleep, self.sleep_btn)
        self.Bind(wx.EVT_BUTTON, self.OnExercise, self.exercise_btn)
        self.Bind(wx.EVT_BUTTON, self.OnProfile, self.profile_btn)

    def OnQuit(self, event):
        self.Close()

    def OnWater(self, event):
        wx.MessageBox('Water Module', 'Info', wx.OK | wx.ICON_INFORMATION)

    def OnSleep(self, event):
        wx.MessageBox('Sleep Module', 'Info', wx.OK | wx.ICON_INFORMATION)

    def OnExercise(self, event):
        wx.MessageBox('Exercise Module', 'Info', wx.OK | wx.ICON_INFORMATION)

    def OnProfile(self, event):
        wx.MessageBox('Profile Module', 'Info', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = VitaApp()
    app.MainLoop()


class WaterModule(wx.Frame):
    def __init__(self, parent):
        super(WaterModule, self).__init__(parent, title="Water Consumption", size=(600, 400))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.water_input = wx.TextCtrl(panel)
        self.log_button = wx.Button(panel, label="Log Water Intake")
        self.show_stats_button = wx.Button(panel, label="Show Statistics")

        vbox.Add(self.water_input, 0, wx.EXPAND|wx.ALL, 5)
        vbox.Add(self.log_button, 0, wx.EXPAND|wx.ALL, 5)
        vbox.Add(self.show_stats_button, 0, wx.EXPAND|wx.ALL, 5)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.OnLogWater, self.log_button)
        self.Bind(wx.EVT_BUTTON, self.OnShowStats, self.show_stats_button)

    def OnLogWater(self, event):
        amount = self.water_input.GetValue()
        if amount.isdigit():
            with open("water_log.txt", "a") as file:
                file.write(f"{datetime.now()}, {amount}\n")
            wx.MessageBox(f"{amount} ml of water logged!", "Success", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Please enter a valid number", "Error", wx.OK | wx.ICON_ERROR)

    def OnShowStats(self, event):
        dates = []
        amounts = []
        with open("water_log.txt", "r") as file:
            for line in file:
                date_str, amount = line.split(", ")
                dates.append(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f"))
                amounts.append(int(amount))

        plt.figure(figsize=(10, 5))
        plt.plot(dates, amounts, marker='o')
        plt.title("Water Consumption Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount (ml)")
        plt.show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = WaterModule(None)
    frame.Show()
    app.MainLoop()



def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="vita"
    )
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS water_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date_time DATETIME,
        amount INT
    )
    """)
    connection.commit()
    connection.close()

def log_water_to_db(amount):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO water_log (date_time, amount) VALUES (NOW(), %s)", (amount,))
    connection.commit()
    connection.close()

def fetch_water_data():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT date_time, amount FROM water_log WHERE user_id = %s", (user_id,))
    result = cursor.fetchall()
    connection.close()
    return result

create_table()

class WaterModule(wx.Frame):
    def __init__(self, parent):
        super(WaterModule, self).__init__(parent, title="Water Consumption", size=(600, 400))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.water_input = wx.TextCtrl(panel)
        self.log_button = wx.Button(panel, label="Log Water Intake")
        self.show_stats_button = wx.Button(panel, label="Show Statistics")

        vbox.Add(self.water_input, 0, wx.EXPAND|wx.ALL, 5)
        vbox.Add(self.log_button, 0, wx.EXPAND|wx.ALL, 5)
        vbox.Add(self.show_stats_button, 0, wx.EXPAND|wx.ALL, 5)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.OnLogWater, self.log_button)
        self.Bind(wx.EVT_BUTTON, self.OnShowStats, self.show_stats_button)

    def OnLogWater(self, event):
        amount = self.water_input.GetValue()
        if amount.isdigit():
            log_water_to_db(int(amount))
            wx.MessageBox(f"{amount} ml of water logged!", "Success", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Please enter a valid number", "Error", wx.OK | wx.ICON_ERROR)

    def OnShowStats(self, event):
        data = fetch_water_data()
        dates, amounts = zip(*data) if data else ([], [])

        plt.figure(figsize=(10, 5))
        plt.plot(dates, amounts, marker='o')
        plt.title("Water Consumption Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount (ml)")
        plt.show()

if __name__ == '__main__':
    app = wx.App(False)
    user_id = 1  # Example user ID
    frame = WaterModule(None, user_id)
    frame.Show()
    app.MainLoop()
