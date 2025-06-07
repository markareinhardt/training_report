import os
import sys
import argparse
import datetime
import constants
from import_workout import import_workout
from output_report import output_report


# Set current year for arg default
current_year = datetime.datetime.now().year
parser = argparse.ArgumentParser(
                    prog='generate',
                    description='Read workout files and produce a summary report')
parser.add_argument('-y', '--year', default=str(current_year))
args = parser.parse_args()


def sort_start_time(e):
  """ Used to sort training sessions by start_time """
  return e['start_time']

""" Structure to hold all training sessions """
log = {
    "year": args.year,
    "year_total_time": 0,
    "year_total_activities": 0,
    "year_total_load": 0,
    "isoweek": list ({
        "week_total_time": 0,
        "week_total_activities": 0,
        "week_total_load": 0,
        "isoday": list ({
            "date": None,
            "day_total_time": 0,
            "day_total_activities": 0,
            "day_total_load": 0,
            "activity": []
        } for x in range(7))
    } for y in range(53))
}


def populate_log(log):
    """ Pre populate relevant fields in the log structure """
    for x in range(53):
        for y in range (7):
            try:
                log['isoweek'][x]['isoday'][y]['date'] = datetime.date.fromisocalendar(int(log['year']), x+1, y+1)
            except:
                return


def add_to_log(act):
    """ Add a single activity to the log structure """
    week_index = int(act['isoweek'])-1
    day_index = int(act['isoday'])-1
    log['isoweek'][week_index]['isoday'][day_index]['activity'].append(act)
    log['isoweek'][week_index]['isoday'][day_index]['day_total_activities']+=1
    log['isoweek'][week_index]['isoday'][day_index]['day_total_time']+=act['total_timer_time']
    log['isoweek'][week_index]['isoday'][day_index]['day_total_load']+=act['load']
    log['isoweek'][week_index]['week_total_activities']+=1
    log['isoweek'][week_index]['week_total_time']+=act['total_timer_time']
    log['isoweek'][week_index]['week_total_load']+=act['load']
    log['year_total_activities']+=1
    log['year_total_time']+=act['total_timer_time']
    log['year_total_load']+=act['load']
    # Sort day's activities
    log['isoweek'][week_index]['isoday'][day_index]['activity'].sort(key=sort_start_time)


# Pre populate log structure
populate_log(log)

# Find previous December and next January to capture ISO weeks for the processed year
prev_december = str(int(log['year'])-1)+"-12"
next_january = str(int(log['year'])+1)+"-01"

# Loop through files, and when it matches the ISO year, add to log structure
with os.scandir(constants.INPUT_FOLDER) as folder:
    for entry in folder:
        if entry.is_file():
            if entry.name.startswith(log['year']) or \
                entry.name.startswith(prev_december) or \
                entry.name.startswith(next_january):
                act = import_workout(entry)
                if act['isoyear'] == int(log['year']):
                    add_to_log(act)

# Output report from log
output_report(log)

# For cron log entry
print("Completed", datetime.datetime.now())

sys.exit(0)