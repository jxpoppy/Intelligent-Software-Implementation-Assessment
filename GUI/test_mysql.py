from mysql import *
import random
import time
connection=connect_to_mysql()
use_database(connection)
drink_type=['water','coke','beer','juice']
exercise_type=['walk','run','cycle','basketball','football','swim']
dic=dict()


def insert_drink_data_test(connection, date_time, drink_type, intake_ml):
    # 向表格 drink_data 中插入数据
    with connection.cursor() as cursor:
        insert_query = """
        INSERT INTO drink_data (date_time, drink_type, intake_ml)
        VALUES (%s, %s, %s)
        """
        data = (date_time, drink_type, intake_ml)
        cursor.execute(insert_query, data)
    connection.commit()
    print("Data inserted successfully.")

def insert_exercise_data_test(connection, date_time, exercise_type, duration):

    # 向表格 drink_data 中插入数据
    with connection.cursor() as cursor:
        insert_query = """
        INSERT INTO exercise_data (date_time, exercise_type, duration)
        VALUES (%s, %s, %s)
        """
        data = (date_time, exercise_type, duration)
        cursor.execute(insert_query, data)
    connection.commit()
    print("Data inserted successfully.")


# 获取当前的日期和时间
now = datetime.now()
# 获取当前的日期（年月日时分秒）
#nows = now.strftime("%Y-%m-%d %H:%M:%S")
"""
for i in range(70):
    date_times=now-timedelta(days=7-int(i/10))
    date_time=date_times.strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(0.1)
    type=random.choice(drink_type)
    intake=int(random.randint(1,20)*50)
    print(i)
    insert_drink_data_test(connection,date_time, type,intake)
"""

"""
for i in range(70):
    date_times=now-timedelta(days=7-int(i/10))
    date_time=date_times.strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(0.1)
    type=random.choice(exercise_type)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    random_time = f"{hour:02}:{minute:02}:{second:02}"
    # 将时间字符串转换为datetime对象并提取time部分
    time_obj = datetime.strptime(random_time, "%H:%M:%S").time()

    duration=time_obj
    print(i)
    insert_exercise_data_test(connection,date_time,type,duration)

"""

#data=fetch_drink_data_latest20(connection)
#data.reverse()
#for row in data:
#    print(row)

#truncate_drink_data(connection)
#drink_data_histogram(connection)
#drink_data_pie_chart(connection)
#exercise_data_histogram(connection)
exercise_data_pie_chart(connection)

connection.close()
