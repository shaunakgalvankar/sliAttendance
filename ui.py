import streamlit as st  
import pandas as pd
import numpy as np
import json
import json
import datetime
from matplotlib import pyplot as plt
from calculateStudentHours import studentHoursBetween
from calculatePossibleHours import PossibleHoursBetween
import datetime
import pandas as pd
from sendEmailIndividual import send_email
if 'studentID' not in st.session_state:
    st.session_state.studentID = "171821" 
# Add CSS styles for colors
st.markdown(
    """
    <style>
    .title {
        color: #FF0000;  /* Red color */
    }
    .button {
        background-color: #00FF00;  /* Green color */
        color: #FFFFFF;  /* White color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('SLI Attendance')
# Load possible hours from JSON file
with open('possibleHours.json') as f:
    possible_hours = json.load(f)

# Get the first key from possible_hours
firstDate = datetime.datetime.strptime(list(possible_hours.keys())[0], "%m/%d/%Y").date()
lastDate = datetime.datetime.strptime(list(possible_hours.keys())[-1], "%m/%d/%Y").date()

startDate = st.date_input('Start Date', value=firstDate, min_value=None, max_value=None, key=None)
today = datetime.date.today()
endDate = st.date_input('End Date', value=min(today, lastDate), min_value=None, max_value=None, key=None)
studentIDInput = st.text_input('Student ID', value=st.session_state.studentID, max_chars=None, key=None)

# Generate button
if st.button('Generate', key='generate_button'):
    # Fetch the data from startDate, endDate, and studentIDInput
    start_date = startDate.strftime("%m/%d/%Y")
    end_date = endDate.strftime("%m/%d/%Y")
    student_id = studentIDInput
    a = studentHoursBetween(student_id, start_date, end_date)
    hours, minutes, seconds = map(int, a.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    total_hours = total_seconds / 3600
    total_hours = round(total_hours, 2)

    b = PossibleHoursBetween(start_date, end_date)



    # Create a bar graph
    labels = ['Total Hours', 'Possible Hours']
    values = [total_hours, b]

    plt.barh(labels, values)  # Switched to barh for horizontal bars
    plt.xlabel('Hours')  # Switched x-axis label
    plt.ylabel('Count')  # Switched y-axis label
    plt.title('Total Hours vs Possible Hours')

    # Display the bar graph
    st.pyplot(plt)
    c = (total_hours / b) * 100
    st.write(total_hours)
    st.write(b)
    st.write(c)


# Load student data from JSON file
with open('studentData.json') as f:
    student_data = json.load(f)

# Create sidebar
st.sidebar.title('Student Data')

# Display student names in sidebar
for student, values in student_data.items():
    if st.sidebar.button(f"{student} - {values}", key=f"{student}_button"):
        # Set the value of studentID field to the clicked student name
        st.session_state.studentID = student

# Placeholder values for the pie chart
pie_data = [30, 40, 20, 10]

# Display the pie chart
# st.title('Pie Chart')
# fig, ax = plt.subplots()
# ax.pie(pie_data, labels=['A', 'B', 'C', 'D'])
# st.pyplot(fig)

# Load student responses from JSON file
with open('responses.json') as f:
    responses_data = json.load(f)

# Filter responses for the selected studentID
student_responses = responses_data.get(st.session_state.studentID, [])

# Convert responses to a DataFrame
df = pd.DataFrame(student_responses)

# Display the table
st.title('Student Responses')
st.dataframe(df, width=0)  # Set width to 0 to spread over the entire column

email_input = st.text_input('Email', value='', max_chars=None, key=None)
if st.button('Send Email', key='send_email_button'):
    # Call the function with the entered email address
    send_email(email_input, total_hours, b, start_date , end_date)
if st.button('Email All', key='email_all_button'):
    # Code to send email to all email addresses
    pass
