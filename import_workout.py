import constants
import zipfile, json
from datetime import datetime

def import_workout(file):
    activity = {
        "start_time": None,
        "isoyear": None,
        "isoweek": None,
        "isoday": None,
        "sport": "Unknown",
        "wkt_name": None,
        "total_timer_time": 0,
        "avg_heart_rate": 0,
        "load": 0
    }

    if file.name.endswith(constants.FILE_EXTENSION):
        json_file_name = file.name.rpartition(".")[0]+".metadata.json"
        with zipfile.ZipFile(constants.INPUT_FOLDER+"/"+file.name, 'r') as zip:
            with zip.open(json_file_name) as json_file:
                data = json.load(json_file)
                if "startTime" in data:
                    if "time" in data["startTime"]:
                        activity["start_time"] = datetime.fromisoformat(data["startTime"]["time"])
                        activity["isoyear"] = activity["start_time"].astimezone().isocalendar().year
                        activity["isoweek"] = activity["start_time"].astimezone().isocalendar().week
                        activity["isoday"] = activity["start_time"].astimezone().isocalendar().weekday
                        activity["sport"] = data["activityType"]["internalName"]
                        if "title" in data:
                            activity["wkt_name"] = data["title"]
                        activity["total_timer_time"] = data["duration"]
                        activity["avg_heart_rate"] = data["avgHeartrate"]
                        activity["load"] = data["calories"]
                    else:
                        print("Error - no time entry in startTime")
                else:
                    print("Error - no startTime entry")

    return(activity)