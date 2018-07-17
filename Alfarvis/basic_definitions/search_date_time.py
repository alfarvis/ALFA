#!/usr/bin/env python

known_months = dict({'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5,
    'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10,
    'november': 11, 'december': 12, 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
    'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12})


def searchDateTime(keyword_list):
    days = []
    months = []
    years = []
    hours = []
    minutes = []
    N = len(keyword_list)
    for i, keyword in enumerate(keyword_list):
        if ':' in keyword:
            splits = keyword.split(':')
            if len(splits) >= 2:
                hours.append(int(splits[0]))
                minutes.append(int(splits[1]))
                continue
        elif keyword in ['am', 'pm', "o'clock", "oclock"]:
            if i >= 0 and keyword_list[i - 1].isdigit():
                hours.append(int(keyword_list[i - 1]))
                if keyword == 'pm' and hours[-1] != 12:
                    hours[-1] = hours[-1] + 12
                if keyword == 'am' and hours[-1] == 12:
                    hours[-1] = hours[-1] - 12
                minutes.append(0)
        # Search for date
        if '/' in keyword:
            date_splits = keyword.split('/')
        elif '-' in keyword:
            date_splits = keyword.split('-')
        elif keyword in known_months:
            months.append(known_months[keyword])
            if i >= 1 and keyword_list[i - 1].isdigit():
                days.append(int(keyword_list[i - 1]))
                if i < N - 1 and keyword_list[i + 1].isdigit():
                    years.append(int(keyword_list[i + 1]))
            elif i < N - 1 and keyword_list[i + 1].isdigit():
                days.append(int(keyword_list[i + 1]))
                if i < N - 2 and keyword_list[i + 2].isdigit():
                    years.append(int(keyword_list[i + 2]))

        else:
            date_splits = None
        if date_splits is not None and len(date_splits) >= 3:
            months.append(int(date_splits[0]))
            days.append(int(date_splits[1]))
            years.append(int(date_splits[2]))
            continue

    return days, months, years, hours, minutes
