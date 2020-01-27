import random
from datetime import date


def raw_date_generator(min_year, max_year):
    min_date = date(min_year, 1, 1)
    max_date = date(max_year, 12, 31)
    return min_date + (max_date - min_date) * random.random()


def str_date_generator(raw_date, format_list=None):
    if format_list is None:
        format_list = ['%b %d %Y', '%d %b %Y', '%Y %b %d', '%B %d %Y', '%d %B %Y', '%Y %B %d',
                       '%b %dth %Y', '%B %dth %Y', '%dth %b %Y', '%dth %B %Y',
                       '%b %dth, %Y', '%B %dth, %Y', '%dth %b, %Y', '%dth %B, %Y',
                       '%b-%d-%Y', '%d-%b-%Y', '%Y-%b-%d', '%m-%B-%Y', '%d-%B-%Y', '%Y-%B-%d',
                       '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%m-%d-%Y', '%d-%m-%Y', '%Y-%m-%d']
    return raw_date.strftime(format_list[random.randint(0, len(format_list) - 1)])


def date_generator(num, min_year=1800, max_year=2100, format_list=None):
    return [str_date_generator(raw_date_generator(min_year, max_year), format_list) for i in range(num)]


if __name__ == "__main__":
    print(date_generator(500))
