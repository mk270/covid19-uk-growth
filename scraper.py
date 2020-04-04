import requests
import lxml.html
import re
import datetime

URL = 'https://gov.uk/guidance/coronavirus-covid-19-information-for-the-public'

pattern = r'^As of 9am on (.*2020),.* ([0-9,]+) were confirmed( as)? positi'

def get_date_and_count():
    req = requests.get(URL)
    root = lxml.html.fromstring(req.text)
    headings = root.xpath("//h2[@id = '%s']" % 'number-of-cases-and-deaths')
    matching_h2 = headings[0]
    siblings = [ elt for elt in matching_h2.itersiblings() ]
    tgt = siblings[0]
    # probably could have done that all with xpath

    text = tgt.text

    regexp = re.compile(pattern)
    results = regexp.match(text)
    # print(text, results)
    whole, date, count = tuple([ results.group(i) for i in range(0, 3) ])

    day = datetime.datetime.strptime(date, '%d %B %Y')
    count = count.replace(",", "")
    return day, int(count)
