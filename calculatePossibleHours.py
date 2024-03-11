import json
from datetime import datetime, timedelta

def PossibleHoursBetween(startDate, endDate):
    # Load the data from possibleHours.json
    with open('possibleHours.json') as file:
        data = json.load(file)

    # Convert the start and end dates to datetime objects
    start_date = datetime.strptime(startDate, '%m/%d/%Y')  # Updated format
    end_date = datetime.strptime(endDate, '%m/%d/%Y')  # Updated format

    # Calculate the total hours between the start and end dates
    total_hours = 0
    previous_tuesday = None
    for date in data:
        date_obj = datetime.strptime(date, '%m/%d/%Y')  # Updated format
        if start_date <= date_obj <= end_date:
            # Check if the date is a Tuesday or Thursday
            if date_obj.weekday() == 1:
                total_hours += 1.5
                previous_tuesday = date_obj
            elif date_obj.weekday() == 3:
                # Check if the previous Tuesday is within the same week
                if previous_tuesday and date_obj - previous_tuesday <= timedelta(days=6):
                    continue
                total_hours += 1.5
            # Check if the date is a Saturday
            elif date_obj.weekday() == 5:
                total_hours += 4.5

    return total_hours

print(PossibleHoursBetween("09/08/2023", "09/15/2023"))  # Output: 7.5