# timetrackics

    usage: timetrackics.py [-h] [--category CATEGORY] [--location LOCATION] [--description DESCRIPTION] [--date DATE] [--header HEADER] [--debug DEBUG] [--sum SUM] filename

    positional arguments:
      filename              location of icalendar file

    optional arguments:
      -h, --help            show this help message and exit
     --category CATEGORY   filter events by category
     --location LOCATION   filter events by location
     --description DESCRIPTION
                           filter events for something whats in description
     --date DATE           only add events where date starts with this, e.g. 2003-11
     --header HEADER       set to something enables heading row
     --debug DEBUG         set to something enables debug mode
     --sum SUM             prints sum hour's at the end
