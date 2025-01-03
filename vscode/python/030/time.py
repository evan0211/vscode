import time
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def job1():
    print(f'工作１啟動: 目前時間{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

def job2():
    print(f'工作２啟動: 目前時間{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    
def job3():
    print(f'工作３啟動: 目前時間{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

def job4():
    print(f'工作４啟動: 目前時間{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

# 指定時區（一定要指定，否則會失敗）
scheduler = BlockingScheduler(timezone="Asia/Shanghai")

# 每１分鐘執行job1函式
scheduler.add_job(job1, 'interval', minutes=1)

# 每５秒執行job2函式
scheduler.add_job(job2, 'interval', seconds=5)

# 每１秒執行job3函式
scheduler.add_job(job3, 'interval', seconds=1)

# 每週二到日的下午6點30分執行job4函式
scheduler.add_job(job4, 'cron', day_of_week='1-6', hour=18, minute=30)

scheduler.start()

print('Schedule started ...')  # 這行不會被執行
