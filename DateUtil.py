from dateutil import parser as date_parser

def assign_date(date):
    try:
        return date_parser.parse(date)
    except TypeError:
        return date