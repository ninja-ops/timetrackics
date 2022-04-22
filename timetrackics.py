import os.path, sys, argparse
from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("filename", help="location of icalendar file")
  parser.add_argument("--category", help="filter events by category", default="")
  parser.add_argument("--location", help="filter events by location", default="")
  parser.add_argument("--description", help="filter events for something whats in description", default="")
  parser.add_argument("--date", help="only add events where date starts with this, e.g. 2003-11", default="")
  parser.add_argument("--header", help="set to something enables heading row", default="1")
  parser.add_argument("--debug", help="set to something enables debug mode", default="")
  parser.add_argument("--sum", help="prints sum hour's at the end", default="")
  parser.add_argument("--group-by", help="group by e.g. 'day'", default="")

  args = parser.parse_args()
  if os.path.isfile(args.filename) == False:
    print("file '" + args.filename + "' does not exists")
    sys.exit(2)

  lines = []
  days = {}

  g = open(args.filename,'rb')
  gcal = Calendar.from_ical(g.read())

  sum_hours = 0

  for component in gcal.walk():
    if component.name == "VEVENT":
      add = True

      dtstart = component.get('dtstart').dt
      time_dtstart = datetime.fromisoformat(str(dtstart))

      dtend = component.get('dtend').dt
      time_dtend = datetime.fromisoformat(str(dtend))
      time_diff = time_dtend - time_dtstart
      time_hours = time_diff.total_seconds()/60/60

      categories = component.get('categories')
      summary = component.get('summary')
      location = component.get('location')
      description = component.get('description')

      if categories != None and args.category != "":
        if categories.to_ical().decode() != args.category:
          add = False
      else:
        if args.category != "":
          add = False

      if categories != None:
        categories_string = categories.to_ical().decode()
      else:
        categories_string = ""

      if location != None and args.location != "":
        if location != args.location:
          add = False
      else:
        if args.location != "":
          add = False

      if location == None:
        location = ""

      if description != None and args.description != "":
        if description.find(args.description) == -1:
          add = False
      else:
        if args.description != "":
          add = False

      if args.date != "":
        if str(dtstart).find(args.date) != 0:
          add = False

      if args.debug != "":
        print("DEBUG DTSTART\t\t:", dtstart)
        print("DEBUG DTEND\t\t:", dtend)
        print("DEBUG SUMMARY\t\t:", summary)
        print("DEBUG LOCATION\t\t:", location)
        print("DEBUG DESCRIPTION \t:", str(description).replace("\n", " "))
        print("DEBUG HOURS\t\t:", time_hours)


      if add == True:
        sum_hours = sum_hours + time_hours
        if args.debug != "":
          print("DEBUG ?\t\t\t! add to csv-string")
          print("")
        line = str(dtstart) + "\t" + str(dtend) + "\t" + str(time_hours) + "\t" + location + "\t" + categories_string + "\t" + summary + "\t" + str(description).replace("\n", " ")
        day = str(dtstart)[0:10];
        if day not in days:
          days[day] = {}
          days[day]['summary'] = []
          days[day]['hours'] = 0
        days[day]['summary'].append(str(summary))
        days[day]['hours'] = days[day]['hours'] + time_hours
        lines.append(line)
      else:
        if args.debug != "":
          print("DEBUG ?\t\t\t! dont add to csv-string")
          print("")

  g.close()

  if args.debug != "":
    print("DEBUG ", lines)
    print("DEBUG", days)
    print()



  lines.sort(reverse=False)
  if args.group_by == "":
    if args.header != "":
      print("start\tend\thours\tlocation\tcategory\tsummary\tdescription")
    for line in lines:
      print(line)

  if args.group_by == "day":
    if args.header != "":
      print("day\thours\tsummary")
    for item in sorted(days):
      line = item + "\t";
      line = line + str(days[item]['hours']) + "\t";
      line = line + ', '.join(days[item]['summary']);
      print(line)

  if args.sum != "":
    print()
    print("Total\t",sum_hours)
    print()

main()
