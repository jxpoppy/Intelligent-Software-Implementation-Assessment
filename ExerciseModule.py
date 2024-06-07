from datetime import datetime
import os
import json

class ExerciseModule:
    def __init__(self):
        self.history = dict()  # record
        self.exercise_records = []

    def export_json_record(self): #从json中导出运动数据
        file_name = "history.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                history = file.read()
                self.history = json.loads(history)
            file.close()

    def import_json_record(self, date, time, exercise_type, duration_minutes):  # date和time为字符串格式YYYY-MM-DD HH:MM:SS
        record = {
            "date": date,
            "time": time,
            "exercise type": exercise_type,
            "duration minutes": duration_minutes,
        }
        self.export_json_record()
        if 'exercise' not in self.history:  # 如果没有运动量记录，则创建记录运动量的列表
            self.history['exercise'] = []
        self.history["exercise"].append(record)
        file_name = "history.json"
        file = open(file_name, 'w')
        history_json = json.dumps(self.history, sort_keys=True, indent=4, separators=(",", ":"))
        file.write(history_json)
        file.close()

    def empty_history(self): #清空记录，无法复原
        self.export_json_record()
        if 'exercise' not in self.history:
            return
        self.history["exercise"]=[]
        file_name = "history.json"
        file = open(file_name, 'w')
        history_json = json.dumps(self.history, sort_keys=True, indent=4, separators=(",", ":"))
        file.write(history_json)
        file.close()
