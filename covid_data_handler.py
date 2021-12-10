"""A module containing the required functions for the continuous assessment"""

import csv
import json
import requests
import sched
import time

from uk_covid19 import Cov19API


def parse_csv_data(csv_filename: str) -> list:
    """A function thats takes in the name of a csv file and returns a list of strings for the rows in the file"""

    rows = []  # a list containing the strings for the rows

    with open("{}".format(csv_filename)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")  # opens the file and reads the data as an iterable
        for row in csv_reader:
            rows.append(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}")  # the data is appended
            # to the list and separated by whitespace
    return rows


def process_covid_csv_data(covid_csv_data: list) -> tuple[int, int, int]:
    """"A function that takes in a list of strings separated by whitespace and returns some of the data"""

    last_7_days_cases, total_deaths, current_hospital_cases = 0, "", ""

    started_reading = False  # a boolean value to check whether the function has started reading data into the
    # variables above
    cumulative_cases = 0

    deaths_column = 5
    hospital_cases_column = 4  # two variables holding the columns of the data we want

    for i in range(3, 10):
        case = ""
        for character in covid_csv_data[i][::-1]:
            if character != " ":
                case += character
            else:
                case = case[::-1]
                cumulative_cases += int(case)
                break  # a count-controlled loop which loops through rows 4 to 11 tallying the total of the end column
    last_7_days_cases = cumulative_cases

    for character in covid_csv_data[1]:
        if character == " ":
            deaths_column -= 1
        elif deaths_column == 1:
            current_hospital_cases += character
        if deaths_column == 0:
            break  # a count controlled loop which starts reading when it hits the 5th column then breaks when it
            # hits the next column

    for i in range(1, len(covid_csv_data)):
        for character in covid_csv_data[i]:
            if character == " " and hospital_cases_column == 1 and not started_reading:
                hospital_cases_column = 5
                break
            elif character == " ":
                hospital_cases_column -= 1
            elif hospital_cases_column == 1:
                started_reading = True
                total_deaths += character
            if hospital_cases_column == 0:
                return last_7_days_cases, int(current_hospital_cases), int(total_deaths)  # a count controlled loop
                # which reads until it hits the 6th column then stops when it hits the next
    return last_7_days_cases, int(current_hospital_cases), int(total_deaths)


def covid_API_request(location: str = "Exeter", location_type: str = "ltla") -> dict:
    """A function which returns up to date data as a dictionary from an API using the uk-covid19 module"""

    location = location
    ltype = location_type

    area = [
        "areaType={}".format(ltype),
        "areaName={}".format(location)
    ]  # area is used as a filter to select nly data from the locatiokn we want

    categories = {
        "date": "date",
        "hospitalCases": "hospitalCases",
        "cumDeaths60DaysByDeathDate": "cumDeaths60DaysByDeathDate",
        "cumCasesBySpecimenDateRate": "cumCasesBySpecimenDateRate"
    }  # categories is used to select what data we want

    api = Cov19API(filters=area, structure=categories)
    data = api.get_json()  # returns the data as a json
    return data


def schedule_covid_updates(update_interval: int, update_name: str) -> int:
    """A function which schedules an update every given interval"""

    s = sched.scheduler(timefunc=time.monotonic, delayfunc=time.sleep)
    s.enter(update_interval, 1, covid_API_request())
    s.run()  # schedules a new covid api request in the given interval

    return 0


if __name__ == "__main__":
    covid_API_request()
