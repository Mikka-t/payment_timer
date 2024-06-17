import time
import sys
from datetime import datetime
import pyfiglet

# schedule
timer_schedule = {
    "Monday": [["9:00", "12:00"], ["13:00", "18:00"]],
    "Tuesday": [["9:00", "12:00"], ["13:00", "18:00"]],
    "Wednesday": [["13:00", "18:00"]],
    "Thursday": [],
    "Friday": [],
    "Saturday": [],
    "Sunday": []
}

def get_current_count(schedule, current_time, payment):
    total_seconds = 0
    for period in schedule:
        start_time = datetime.strptime(period[0], "%H:%M").time()
        end_time = datetime.strptime(period[1], "%H:%M").time()
        if start_time <= current_time.time() <= end_time:
            total_seconds += (current_time - datetime.combine(current_time.date(), start_time)).seconds
        elif current_time.time() > end_time:
            total_seconds += (datetime.combine(current_time.date(), end_time) - datetime.combine(current_time.date(), start_time)).seconds
    return total_seconds * (payment / 3600)

def is_within_schedule(schedule, current_time):
    for period in schedule:
        start_time = datetime.strptime(period[0], "%H:%M").time()
        end_time = datetime.strptime(period[1], "%H:%M").time()
        if start_time <= current_time.time() <= end_time:
            return True
    return False

def timer(payment, time_slice):
    current_time = datetime.now()
    weekday = current_time.strftime("%A")
    if weekday in timer_schedule:
        count = get_current_count(timer_schedule[weekday], current_time, payment)
    else:
        count = 0

    interval = time_slice * 3600 / payment # time of 0.01 yen

    try:
        while True:         
            sys.stdout.write("\033[H\033[J")   
            ascii_art = pyfiglet.figlet_format(f"{count:.2f}")
            sys.stdout.write(f"\r{ascii_art}")
            sys.stdout.flush()
            current_time = datetime.now()
            if is_within_schedule(timer_schedule[weekday], current_time):
                time.sleep(interval)
                count += time_slice
            else:
                time.sleep(1) # when its not working time
    except KeyboardInterrupt:
        print("\n timer stopped.")

if __name__ == "__main__":
    payment = 1064 # yen per hour
    time_slice = 0.01 # seconds
    timer(payment, time_slice)
