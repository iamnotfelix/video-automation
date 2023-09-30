import time
import schedule
import app
from datetime import datetime

def routine():
    app.scrapping()

def attemptRoutine():
    while(1):
        try:
            print("Routine started at {0}".format(str(datetime.now())))
            routine()
            break
        except OSError as err:
            print("Routine Failed on OS error: {0}".format(err))
            time.sleep(60)
        except Exception as err:
            print("Routine Failed on Exception: {0}".format(err))
            print("TODO: handle specific exceptions(mainly instaloader exceptions) differently.")
            break

schedule.every().day.at("19:36").do(attemptRoutine)

while True:
    schedule.run_pending()  
    time.sleep(60) # wait 1 minute
