from flask import Flask, render_template, request, redirect, url_for
import calendar
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the current month and year
    now = datetime.now()
    month = now.month
    year = now.year

    # Check for user input to change the month/year
    if request.method == 'POST':
        month = int(request.form.get('month', month))
        year = int(request.form.get('year', year))

    # Create a calendar for the given month and year
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    cal_data = cal.formatmonth(year, month)
    
    # Make each date clickable
    cal_data = cal_data.replace('>%d<' % datetime.now().day, '><a href="/date/{}/{}/{}">%d</a><' % (year, month, datetime.now().day))

    return render_template('index.html', calendar_data=cal_data, month=month, year=year)

@app.route('/date/<int:year>/<int:month>/<int:day>')
def display_date_file(year, month, day):
    # Format date as yyymmdd
    file_date = datetime(year, month, day).strftime('%y%m%d')
    file_name = f'cal_{file_date}.cal'

    # Check if the file exists, create it if not
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            file.write(f'File for {year}-{month}-{day}\n')
    
    # Display the file content
    with open(file_name, 'r') as file:
        content = file.read()

    return f"<h1>File: {file_name}</h1><pre>{content}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
