from datetime import date
import CalendarUtil

schoolCalendarUri = "https://www.gmaelem.org/calendar/calendar_242.ics"
athleticCalendarUri = "https://www.gmaelem.org/calendar/page_534.ics"
menuCalendarUri = "https://www.gmaelem.org/calendar/calendar_298.ics"

request_date = date(2020, 10, 21)
caption = "Calendar"
items = CalendarUtil.GetItemsForDate(request_date, caption, schoolCalendarUri)

response = ""

count = len(items)

if count == 0:
    response = "I didn't find any items on the {0} on {1}. You can say another day to search again.".format(caption.lower(),request_date)
else:

    intro = ""

    if count == 1:
        intro = "I found one item on"
    else:
        intro = "I found {0} items on".format(count)

    index = 0
    eventText = ""
    for item in items:
        index = index + 1
        eventText = eventText + "{0}. {1}.\n".format(index, item)

    response = "{0} the {1} on {2}.\n\n{3}\nYou can say another day to search again.".format(intro, caption.lower(), request_date, eventText)

print(response)


