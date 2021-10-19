from datetime import date, datetime
from urllib.request import Request, urlopen
from icalendar import Calendar

#"SchoolCalendarUri": "https://www.gmaelem.org/calendar/calendar_242.ics",
#"AthleticCalendarUri": "https://www.gmaelem.org/calendar/page_534.ics",
#"MenuCalendarUri": "https://www.gmaelem.org/calendar/calendar_298.ics"

# This should return a list of strings
def GetItemsForDate(request_date, caption, calendar_uri, logger):
    
    request_date = FixDate(request_date)
    
    logger.info("GetItemsForDate: request_date == {0}.".format(request_date))


    cal = GetCalendar(calendar_uri, logger)
    
    events = cal.walk('vevent')
    count = len(events)
    logger.info("GetItemsForDate: {0} events in Calendar.".format(count))

    items = []

    for event in events:
        start_date = event["DTSTART"].dt
        start_date = FixDate(start_date)
        logger.info("GetItemsForDate: start_date == {0}.".format(start_date))
        if start_date == request_date:
            summary = event["SUMMARY"]
            items.append(summary)

    count = len(items)
    logger.info("GetItemsForDate: {0} matching items.".format(count))

    return(items)

def GetCalendar(uri, logger):
    
    fname = uri
    user_agent = "Mozilla/5.0 AppleWebKit/537.36 Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    request = Request(fname)
    request.add_header("User-Agent", user_agent)
    
    response = urlopen(request)
    body = response.read()
    
    logger.info(body)

    cal = Calendar.from_ical(body)

    return(cal)

def FixDate(date_in):
    if type(date_in) == str:
        date_in = datetime.strptime(date_in, "%Y-%m-%d")
    y = date_in.year
    m = date_in.month
    d = date_in.day
    date_out = date(y, m, d)

    return(date_out)


