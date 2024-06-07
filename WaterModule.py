from datetime import datetime
import os
import json
import matplotlib.pyplot as plt

class WaterMoudle:
    def __init__(self):
        self.history = dict() #record
        self.water_data=0
        self.milk_data=0
        self.beer_data=0
        self.coke_data=0

    def export_json_record(self): #从json中导出饮水量
        file_name = "history.json"
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                history = file.read()
                self.history=json.loads(history)
            file.close()

    def import_json_record(self,date,time,drink_type,consumption): #date和time为字符串格式YYYY-MM-DD HH:MM:SS
        record={                                                    #向json存入饮水量
            "date":date,
            "time":time,
            "drink type":drink_type,
            "consumption":consumption,
        }
        self.export_json_record()
        if 'water consumption' not in self.history: #如果没有饮水量记录，则创建记录饮水量的列表
            self.history['water consumption']=[]
        self.history["water consumption"].append(record)
        file_name="history.json"
        file = open(file_name,'w')
        history_json=json.dumps(self.history,sort_keys=True,indent=4,separators=(",",":"))
        file.write(history_json)
        file.close()

    def empty_history(self): #清空记录，无法复原
        self.export_json_record()
        if 'water consumption' not in self.history:
            return
        self.history["water consumption"]=[]
        file_name = "history.json"
        file = open(file_name, 'w')
        history_json = json.dumps(self.history, sort_keys=True, indent=4, separators=(",", ":"))
        file.write(history_json)
        file.close()


