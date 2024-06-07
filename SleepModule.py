from datetime import datetime
import os
import json

class SleepModule():
    def __init__(self):
        self.history = dict()  # record
        self.exercise_records = []

    def export_json_record(self): #从json中导出睡眠数据
        file_name = "history.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                history = file.read()
                self.history = json.loads(history)
            file.close()

    def import_json_record(self, sleep_time, wake_time):  # date和time为字符串格式YYYY-mm-DD HH:MM:SS
        # 使用datetime.strptime()方法将字符串解析为datetime对象
        time1 = datetime.strptime(sleep_time, '%Y-%m-%d %H:%M:%S')
        time2 = datetime.strptime(wake_time, '%Y-%m-%d %H:%M:%S')
        sleep_duration = time2 - time1
        record = {
            "sleep time": sleep_time,
            "wake time": wake_time,
            "sleep duration":str(sleep_duration)
        }
        self.export_json_record()
        if 'sleep' not in self.history:  # 如果没有睡眠记录，则创建记录睡眠的列表
            self.history['sleep'] = []
        self.history["sleep"].append(record)
        file_name = "history.json"
        file = open(file_name, 'w')
        history_json = json.dumps(self.history, sort_keys=True, indent=4, separators=(",", ":"))
        file.write(history_json)
        file.close()

    def empty_history(self): #清空记录，无法复原
        self.export_json_record()
        if 'sleep' not in self.history:
            return
        self.history["sleep"]=[]
        file_name = "history.json"
        file = open(file_name, 'w')
        history_json = json.dumps(self.history, sort_keys=True, indent=4, separators=(",", ":"))
        file.write(history_json)
        file.close()
