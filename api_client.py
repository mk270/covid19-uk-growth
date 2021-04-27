#!/usr/bin/env python3

import datetime
import logging
import argparse
import requests
import json

endpoint = "https://api.coronavirus.data.gov.uk/v1/data"
# secret docs at https://coronavirus.data.gov.uk/developers-guide


class DateNotFound(Exception):
    pass


def get_data(today):
    structure = json.dumps({
        "date": "date",
        "newCases": "newCasesByPublishDate",
        "cumCases": "cumCasesByPublishDate",
        "cumTests": "cumTestsByPublishDate"
    })
    filters = "areaType=overview"

    url = f"{endpoint}?filters={filters}&structure={structure}"
    result = requests.get(url)
    assert result.status_code == 200, (result.status_code, result.reason)
    data = result.json()["data"]

    logging.info(json.dumps(data, indent=2))

    for i in data:
        if i["date"] == today:
            return (i["newCases"], i["cumCases"], i["cumTests"])
    raise DateNotFound

def lookup_cases_and_tested(days_ago):
    today = datetime.datetime.now()
    offset = datetime.timedelta(days_ago)
    then = (today - offset).strftime("%Y-%m-%d")
    new_cases, cum_cases, cum_tests = get_data(then)
    return (then, cum_cases, cum_tests)
