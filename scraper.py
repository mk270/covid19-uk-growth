import requests
import lxml.html
import re
import time
import datetime
import logging

URL = 'https://gov.uk/guidance/coronavirus-covid-19-information-for-the-public'

patterns = {
    "date": r'^As of 9 ?am( on)? ([0-9]+) ([A-Z][a-z]+),',
    "tested": r'.*there have been ([0-9,]+) tests',
    "positive": r'.* ([0-9,]+) (people )?(have )?tested positive.*'
}

max_matches = 3 + 1 # number of groups in regexp above, plus one for whole

def get_report():
    req = requests.get(URL)
    root = lxml.html.fromstring(req.text)
    headings = root.xpath("//h3[@id = '%s']" % 'positive-cases')
    matching_h2 = headings[0]
    siblings = [ elt for elt in matching_h2.itersiblings() ]
    return siblings

def extract_results(elts):
    def extract():
        for name, pattern in patterns.items():
            regexp = re.compile(pattern)
            results = None
            for elt in elts:
                text = elt.text
                logging.info(text)
                if text is None:
                    continue
                results = regexp.match(text)
                if results is None:
                    continue
                break
            logging.info(name)
            logging.info(results)
            yield name, results

    groups = dict([ (name, results) for name, results in extract() ])

    day = int(groups["date"].group(2))
    month_name = groups["date"].group(3)

    month = time.strptime(month_name, '%B').tm_mon
    year = datetime.datetime.now().year
    date = datetime.datetime(year, month, day)

    tested = int(groups["tested"].groups(1)[0].replace(",", ""))
    count = int(groups["positive"].groups(1)[0].replace(",", ""))

    assert count != 0

    return date, count, tested

def get_date_and_count():
    elts = get_report()
    day, count, tested = extract_results(elts)
    return day, count, tested
