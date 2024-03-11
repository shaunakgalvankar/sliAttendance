import datetime
import json

def studentHoursBetween(studentID, start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").date()
    end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").date()

    with open('responses.json') as file:
        data = json.load(file)

    if studentID not in data:
        return "Student ID not found in data."

    student_data = data[studentID]
    check_in_out_pairs = []
    check_in_time = None

    # Format for parsing the date and time from the string
    date_format = "%m/%d/%Y %H:%M:%S"
    total_seconds = 0

    for entry in student_data:
        timestamp_str, action, dayOfWeek = entry
        timestamp = datetime.datetime.strptime(timestamp_str, date_format)
        if start_date <= timestamp.date() <= end_date:
            if action == "CHECK IN":
                check_in_time = timestamp
            elif action == "CHECK OUT" and check_in_time is not None:
                duration = timestamp - check_in_time
                if dayOfWeek in ["Monday","Tuesday","Wednesday", "Thursday","Friday"]:
                    duration = min(duration, datetime.timedelta(hours=1.5))
                if dayOfWeek in ["Saturday"]:
                    duration = min(duration, datetime.timedelta(hours=4.5))
                total_seconds += duration.total_seconds()
                check_in_time = None  # Reset check-in time after pairing with a check-out

    total_hours, remainder_seconds = divmod(total_seconds, 3600)
    total_minutes, total_seconds = divmod(remainder_seconds, 60)

    # Return the total time as a formatted string (HH:MM:SS)
    return f"{int(total_hours):02}:{int(total_minutes):02}:{int(total_seconds):02}"


