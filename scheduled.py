from apscheduler.schedulers.blocking import BlockingScheduler
from wylsacom import wylsacom


sched = BlockingScheduler()

cur_website = 0

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every minute.')

    # parse cur_website
    if cur_website == 0:
        print(wylsacom())
        #parsing




# @sched.scheduled_job('cron', hour=13)
# def scheduled_job():
#     print('This job is run every weekday at 1pm.')

sched.start()
