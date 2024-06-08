import pymysql
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np


"""
database form

drink table
date_time               drink_type  intake(ml)
YYYY-MM-DD HH:MM:SS     varchar     int

exercise table
date_time               exercise_type   duration
YYYY-MM-DD HH:MM:SS     varchar         varchar(HH:MM:SS)

sleep table
date_time               duration
YYYY-MM-DD HH:MM:SS     varchar(HH:MM:SS)

"""


def connect_to_mysql(password='liuguangsen'):
    if not password:
        print("Please enter the mysql password!")
        return
    # 连接到MySQL数据库
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=password,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def create_database(connection):
    # 创建数据库 vita_data
    with connection.cursor() as cursor:
        create_database_query = "CREATE DATABASE IF NOT EXISTS vita_data"
        cursor.execute(create_database_query)
    connection.commit()

def use_database(connection):
    # 切换到数据库 vita_data
    with connection.cursor() as cursor:
        cursor.execute("USE vita_data")
    connection.commit()

def create_table(connection):
    # 创建表格 drink_data
    with connection.cursor() as cursor:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS drink_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date_time DATETIME,
            drink_type VARCHAR(255),
            intake_ml INT
        )
        """
        cursor.execute(create_table_query)

    # 创建表格 exercise_data
        create_table_query = """
        CREATE TABLE IF NOT EXISTS exercise_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date_time DATETIME,
            exercise_type VARCHAR(255),
            duration VARCHAR(25)
        )
        """
        cursor.execute(create_table_query)

    # 创建表格 sleep_data
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sleep_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date_time DATETIME,
            duration VARCHAR(25)
        )
        """
        cursor.execute(create_table_query)


    connection.commit()

def insert_drink_data(connection, drink_type, intake_ml):
    # 获取当前的日期和时间
    now = datetime.now()
    # 获取当前的日期（年月日时分秒）
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

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

def insert_exercise_data(connection, exercise_type, duration):

    # 获取当前的日期和时间
    now = datetime.now()
    # 获取当前的日期（年月日时分秒）
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

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

def insert_sleep_data(connection, duration): #sleep_time和wake_time是格式为YYYY-mm-dd HH:MM:SS的字符串
                                                            #wake_time格式为day HH:MM:SS

    # 获取当前的日期和时间
    now = datetime.now()
    # 获取当前的日期（年月日时分秒）
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # 向表格 sleep_data 中插入数据
    with connection.cursor() as cursor:
        insert_query = """
        INSERT INTO sleep_data (date_time, duration)
        VALUES (%s, %s)
        """
        data = (date_time, duration)
        cursor.execute(insert_query, data)
    connection.commit()
    print("Data inserted successfully.")

def fetch_drink_data(connection):
    # 读取数据
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM drink_data")
        data = cursor.fetchall()
    return data #list格式

def fetch_drink_data_latest20(connection):
    # 读取数据
    with connection.cursor() as cursor:
        # 获取 drink_data 表格中最新的 20 条数据
        query = """
        SELECT * FROM drink_data
        ORDER BY id DESC
        LIMIT 20
        """
        cursor.execute(query)
        # 将数据存储在变量 data_latest20 中
        data_latest20 = cursor.fetchall()
    return data_latest20

def print_drink_data_latest20(connection):
    data_latest20=fetch_drink_data_latest20(connection)
    message=""
    for i in range(len(data_latest20)):
        row=data_latest20[i].copy()
        message=message + f"{row['id']}. {str(row['date_time'])}, {row['drink_type']}, {row['intake_ml']}"
        if i != len(data_latest20)-1:
            message += "\n"
    return message


def fetch_drink_data_week(connection):
    # 读取数据
    with connection.cursor() as cursor:
        # 获取当前时间和一星期前的时间
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        one_week_ago = today_start - timedelta(days=7)

        # 转换为字符串格式，适应MySQL的DATETIME格式
        one_week_ago_str = one_week_ago.strftime('%Y-%m-%d %H:%M:%S')

        # 查询 drink_data 表格中 date_time 为最近一星期之内的数据
        query = """
        SELECT * FROM drink_data
        WHERE date_time >= %s
        ORDER BY id DESC
        """
        cursor.execute(query, (one_week_ago_str,))

        # 将数据存储在变量 data 中
        data_week = cursor.fetchall()
    return data_week

def fetch_exercise_data(connection):
    # 读取数据
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM exercise_data")
        data = cursor.fetchall()
    return data

def fetch_exercise_data_latest20(connection):
    # 读取数据
    with connection.cursor() as cursor:
        # 获取 exercise_data 表格中最新的 20 条数据
        query = """
        SELECT * FROM exercise_data
        ORDER BY id DESC
        LIMIT 20
        """
        cursor.execute(query)
        # 将数据存储在变量 data_latest20 中
        data_latest20 = cursor.fetchall()
    return data_latest20

def print_exercise_data_latest20(connection):
    data_latest20=fetch_exercise_data_latest20(connection)
    message=""
    for i in range(len(data_latest20)):
        row=data_latest20[i].copy()
        message=message + f"{row['id']}. {str(row['date_time'])}, {row['exercise_type']}, {str(row['duration'])}"
        if i!=len(data_latest20)-1:
            message+="\n"
    return message

def fetch_exercise_data_week(connection):
    # 读取数据
    with connection.cursor() as cursor:
        # 获取当前时间和一星期前的时间
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        one_week_ago = today_start - timedelta(days=7)

        # 转换为字符串格式，适应MySQL的DATETIME格式
        one_week_ago_str = one_week_ago.strftime('%Y-%m-%d %H:%M:%S')

        # 查询 exercise_data 表格中 date_time 为最近一星期之内的数据
        query = """
        SELECT * FROM exercise_data
        WHERE date_time >= %s
        ORDER BY id DESC
        """
        cursor.execute(query, (one_week_ago_str,))

        # 将数据存储在变量 data 中
        data_week = cursor.fetchall()
    return data_week

def fetch_exercise_data_today(connection):
    # 读取数据
    with connection.cursor() as cursor:
        # 获取当前时间和今天凌晨0时的时间
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # 转换为字符串格式，适应MySQL的DATETIME格式
        today_start_str = today_start.strftime('%Y-%m-%d %H:%M:%S')

        # 查询 exercise_data 表格中 date_time 为今天0时起到现在的数据
        query = """
            SELECT * FROM exercise_data
            WHERE date_time >= %s
            ORDER BY id DESC
            """
        cursor.execute(query, (today_start_str,))

        # 将数据存储在变量 data_today 中
        data_today = cursor.fetchall()
    return data_today

def fetch_sleep_data(connection):
    # 读取数据
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM sleep_data")
        data = cursor.fetchall()
    return data

def fetch_sleep_data_latest20(connection):
    # 读取数据
    with connection.cursor() as cursor:
        # 获取 sleep_data 表格中 id 最新的 20 条数据
        query = """
        SELECT * FROM sleep_data
        ORDER BY id DESC
        LIMIT 20
        """
        cursor.execute(query)
        # 将数据存储在变量 data_latest20 中
        data_latest20 = cursor.fetchall()
    return data_latest20

def fetch_sleep_data_month(connection):
    # 读取数据
    with connection.cursor() as cursor:
        # 获取当前时间和一个月(按30天计)前的时间
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        one_month_ago = today_start - timedelta(days=30)

        # 转换为字符串格式，适应MySQL的DATETIME格式
        one_month_ago_str = one_month_ago.strftime('%Y-%m-%d %H:%M:%S')

        # 查询 sleep_data 表格中 date_time 为最近一个月之内的数据
        query = """
        SELECT * FROM sleep_data
        WHERE date_time >= %s
        ORDER BY id DESC
        """
        cursor.execute(query, (one_month_ago_str,))

        # 将数据存储在变量 data 中
        data_month = cursor.fetchall()
    return data_month


def truncate_drink_data(connection):
    with connection.cursor() as cursor:
        # 清除表格 drink_data 中的数据
        truncate_table_query = "TRUNCATE TABLE drink_data"
        cursor.execute(truncate_table_query)
    # 提交更改
    connection.commit()

def truncate_exercise_data(connection):
    with connection.cursor() as cursor:
        # 清除表格 exercise_data 中的数据
        truncate_table_query = "TRUNCATE TABLE exercise_data"
        cursor.execute(truncate_table_query)
    # 提交更改
    connection.commit()

def truncate_sleep_data(connection):
    with connection.cursor() as cursor:
        # 清除表格 sleep_data 中的数据
        truncate_table_query = "TRUNCATE TABLE sleep_data"
        cursor.execute(truncate_table_query)
    # 提交更改
    connection.commit()

def calculate_exercise_calorie_today(connection):
    #获取今日运动数据
    data_today=fetch_exercise_data_today(connection)
    # 今日无数据时返回0
    if len(data_today)==0:
        return 0
    #存储卡路里
    calorie=0
    for row in data_today:

        # 分割字符串并转换为整数
        hours, minutes, seconds = map(int, row['duration'].split(':'))
        # 将小时和分钟转换为总的分钟数
        duration_min = hours * 60 + minutes + seconds // 60  # 将秒数部分也算作分钟

        #print(row['exercise_type'],duration_min)
        if row['exercise_type']=='walk':
            # 累计卡路里数量
            calorie += 5 * duration_min
        elif row['exercise_type']=='run':
            # 累计卡路里数量
            calorie += 12 * duration_min
        elif row['exercise_type']=='cycle':
            # 累计卡路里数量
            calorie += 10 * duration_min
        elif row['exercise_type']=='basketball':
            # 累计卡路里数量
            calorie += 8 * duration_min
        elif row['exercise_type']=='football':
            # 累计卡路里数量
            calorie += 8 * duration_min
        elif row['exercise_type']=='swim':
            # 累计卡路里数量
            calorie += 10 * duration_min
    #确保输出为整数
    calorie = int(calorie)
    return calorie

def drink_data_histogram(connection):
    # 创建一个字典，用于存储每天每种饮品的摄入量总和
    daily_intake = defaultdict(lambda: defaultdict(int))
    # 获取过去一个星期饮品摄入量的数据
    data_week = fetch_drink_data_week(connection)

    # 如果没有数据，则返回0
    if len(data_week)==0:
        print("No data")
        return

    # 遍历数据，统计每天每种饮品的摄入量总和
    for row in data_week:
        date = row['date_time'].date()  # 获取日期（年月日）
        drink_type = row['drink_type']
        intake_ml = row['intake_ml']
        daily_intake[date][drink_type] += intake_ml

    # 获取最近一星期的日期范围
    start_date = min(daily_intake.keys())
    end_date = max(daily_intake.keys())

    # 创建柱状图的横坐标和纵坐标数据
    dates = []
    water_intake = []
    coke_intake = []
    beer_intake = []
    milk_intake = []

    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        water_intake.append(daily_intake[current_date]['water'])
        coke_intake.append(daily_intake[current_date]['coke'])
        beer_intake.append(daily_intake[current_date]['beer'])
        milk_intake.append(daily_intake[current_date]['milk'])
        current_date += timedelta(days=1)

    # 计算柱状图的位置
    bar_width = 0.2
    bar_positions = range(len(dates))

    # 创建 matplotlib 图形
    fig, ax = plt.subplots(figsize=(4.5, 4), dpi=100)
    ax.bar([x - 1.5 * bar_width for x in bar_positions], water_intake, label='Water', color='blue', width=bar_width)
    ax.bar([x - 0.5 * bar_width for x in bar_positions], coke_intake, label='Coke', color='red', width=bar_width)
    ax.bar([x + 0.5 * bar_width for x in bar_positions], beer_intake, label='Beer', color='green', width=bar_width)
    ax.bar([x + 1.5 * bar_width for x in bar_positions], milk_intake, label='Milk', color='orange', width=bar_width)

    # 设置图形属性
    ax.set_xlabel('Date')
    ax.set_ylabel('Intake (ml)')
    ax.set_title('Weekly Drink Intake')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(dates, rotation=45)
    ax.legend()
    plt.tight_layout()

    return fig


def exercise_data_histogram(connection):
    # 创建一个字典，用于存储每天每种运动的时长总和
    daily_exercise = defaultdict(lambda: defaultdict(int))
    # 获取过去一个星期运动数据
    data_week = fetch_exercise_data_week(connection)

    # 如果没有数据，则返回0
    if len(data_week) == 0:
        print("No data")
        return

    # 遍历数据，统计每天每种运动的时长总和
    for row in data_week:
        date = row['date_time'].date()  # 获取日期（年月日）
        exercise_type = row['exercise_type']
        # 将时间字符串转换为datetime对象
        time_obj = datetime.strptime(row['duration'], "%H:%M:%S")
        # 计算总分钟数，忽略秒数
        total_minutes = time_obj.hour * 60 + time_obj.minute
        duration_min = total_minutes
        daily_exercise[date][exercise_type] += duration_min

    # 获取最近一星期的日期范围
    start_date = min(daily_exercise.keys())
    end_date = max(daily_exercise.keys())

    # 创建柱状图的横坐标和纵坐标数据
    dates = []
    walk_duration = []
    run_duration = []
    cycle_duration = []
    basketball_duration = []
    football_duration = []
    swim_duration = []

    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        walk_duration.append(daily_exercise[current_date]['walk'])
        run_duration.append(daily_exercise[current_date]['run'])
        cycle_duration.append(daily_exercise[current_date]['cycle'])
        basketball_duration.append(daily_exercise[current_date]['basketball'])
        football_duration.append(daily_exercise[current_date]['football'])
        swim_duration.append(daily_exercise[current_date]['swim'])
        current_date += timedelta(days=1)

    # 计算柱状图的位置
    bar_width = 0.2
    bar_positions = range(len(dates))

    # 创建 matplotlib 图形，尺寸为 500x500 像素
    fig, ax = plt.subplots(figsize=(4.5, 4), dpi=100)  # 设置 dpi 为 100 以达到 500x500 像素

    ax.bar([x - 2.5 * bar_width for x in bar_positions], walk_duration, label='Walk', color='blue', width=bar_width)
    ax.bar([x - 1.5 * bar_width for x in bar_positions], run_duration, label='Run', color='red', width=bar_width)
    ax.bar([x - 0.5 * bar_width for x in bar_positions], cycle_duration, label='Cycle', color='green', width=bar_width)
    ax.bar([x + 0.5 * bar_width for x in bar_positions], basketball_duration, label='Basketball', color='orange', width=bar_width)
    ax.bar([x + 1.5 * bar_width for x in bar_positions], football_duration, label='Football', color='purple', width=bar_width)
    ax.bar([x + 2.5 * bar_width for x in bar_positions], swim_duration, label='Swim', color='cyan', width=bar_width)

    # 设置图形属性
    ax.set_xlabel('Date')
    ax.set_ylabel('Duration (min)')
    ax.set_title('Weekly Exercise Duration')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(dates, rotation=45)
    ax.legend()
    plt.tight_layout()

    return fig



def drink_data_pie_chart(connection):
    # 创建一个字典，用于存储每种饮品的摄入量总和
    total_intake = defaultdict(int)
    # 获取过去一个星期饮品摄入量的数据
    data_week = fetch_drink_data_week(connection)

    # 如果没有数据，则返回0
    if len(data_week) == 0:
        print("No data")
        return

    # 遍历数据，统计每种饮品的摄入量总和
    for row in data_week:
        drink_type = row['drink_type']
        intake_ml = row['intake_ml']
        total_intake[drink_type] += intake_ml

    # 计算总摄入量
    total = sum(total_intake.values())

    # 计算每种饮品的摄入量占比
    percentages = {drink_type: (intake_ml / total) * 100 for drink_type, intake_ml in total_intake.items()}

    # 构建标签
    labels = [f"{drink_type} \n({total_intake[drink_type]} ml)" for drink_type in total_intake.keys()]
    sizes = percentages.values()

    # 创建 matplotlib 图形，尺寸为 500x500 像素
    fig, ax = plt.subplots(figsize=(4.5, 4), dpi=100)  # 设置 dpi 为 100 以达到 500x500 像素

    # 绘制饼图
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Drink Intake Percentage per week', pad=20)  # 调整标题的距离
    ax.axis('equal')  # 保持饼图为圆形

    # 调整图的子图布局，将饼图下移一些距离
    fig.subplots_adjust(bottom=0.1)

    return fig

def exercise_data_pie_chart(connection):
    # 创建一个字典，用于存储每种运动的持续时间总和
    total_duration = defaultdict(int)
    # 获取过去一个星期运动持续时间的数据
    data_week = fetch_exercise_data_week(connection)

    # 如果没有数据，则返回0
    if len(data_week) == 0:
        print("No data")
        return

    # 遍历数据，统计每种运动的持续时间总和
    for row in data_week:
        exercise_type = row['exercise_type']

        # 分割字符串并转换为整数
        hours, minutes, seconds = map(int, row['duration'].split(':'))
        # 将小时和分钟转换为总的分钟数
        total_minutes = hours * 60 + minutes + seconds // 60  # 将秒数部分也算作分钟

        duration_min = int(total_minutes)
        total_duration[exercise_type] += duration_min

    # 计算总摄入量
    total = sum(total_duration.values())

    # 计算每种饮品的摄入量占比
    percentages = {exercise_type: (duration_min / total) * 100 for exercise_type, duration_min in total_duration.items()}

    # 构建标签
    labels = [f"{exercise_type} \n({total_duration[exercise_type]} mins)" for exercise_type in total_duration.keys()]
    sizes = percentages.values()

    # 创建 matplotlib 图形，尺寸为 500x500 像素
    fig, ax = plt.subplots(figsize=(4.5, 4), dpi=100)  # 设置 dpi 为 100 以达到 500x500 像素

    # 绘制饼图
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Exercise Duration Percentage per week', pad=20)  # 调整标题的距离
    ax.axis('equal')  # 保持饼图为圆形

    # 调整图的子图布局，将饼图下移一些距离
    fig.subplots_adjust(bottom=0.1)

    return fig

def sleep_data_line_chart(connection):
    # 创建一个字典，用于存储每种运动的持续时间总和
    total_duration = defaultdict(int)
    # 获取过去一个星期运动持续时间的数据
    data_week = fetch_sleep_data_month(connection)
    #data_week = fetch_exercise_data_week(connection)

    # 如果没有数据，则返回0
    if len(data_week) == 0:
        print("No data")
        return

    # 将数据转换为日期和时长的列表
    dates = []
    durations = []

    for row in data_week:
        date = row['date_time'].date()
        duration_parts = row['duration'].split(':')
        duration_hours = float(duration_parts[0]) + float(duration_parts[1]) / 60
        dates.append(date)
        durations.append(duration_hours)

    # 按日期进行分组并计算每天的睡眠总时长
    daily_sleep_duration = {}
    for date, duration in zip(dates, durations):
        if date in daily_sleep_duration:
            daily_sleep_duration[date] += duration
        else:
            daily_sleep_duration[date] = duration

    # 将字典按日期排序
    sorted_dates = sorted(daily_sleep_duration.keys())
    sorted_durations = [round(daily_sleep_duration[date], 1) for date in sorted_dates]

    # 创建折线图
    fig, ax = plt.subplots(figsize=(11, 4),dpi = 100)
    ax.plot(sorted_dates, sorted_durations, marker='o', linestyle='-')

    # 设置图形属性
    ax.set_title('Sleep Duration Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sleep Duration (Hours)')
    ax.grid(True)

    return fig



if __name__=='__main__' and True:

    connection = connect_to_mysql()
    create_database(connection)
    use_database(connection)
    create_table(connection)
    #insert_drink_data(connection,'water',100)
    #insert_drink_data(connection,'coke',150)

    #data=fetch_drink_data(connection)
    #data=fetch_drink_data_week(connection)
    #data=fetch_drink_data_latest20(connection)
    #print("Data from drink_data table:")
    #for row in data:
    #    print(row)
    #print(data)
    #print(type(data))

    #truncate_drink_data(connection)
    sleep_data_line_chart(connection)
    connection.close()
