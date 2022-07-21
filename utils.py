import datetime

def periods_gen(period_from:str,period_to:str) ->list:

    date_from = period_from + "-01"
    date_to = period_to + "-01"

    date_from = datetime.datetime.strptime(date_from,"%Y-%m-%d")
    date_to = datetime.datetime.strptime(date_to,"%Y-%m-%d")

    periods = []

    while date_from <= date_to:

        period_start = datetime.datetime.strftime(date_from,"%Y%m%d")
        period_end = date_from + datetime.timedelta(days=40)
        period_end = period_end - datetime.timedelta(days=period_end.day)

        date_from = period_end + datetime.timedelta(days=1)

        period_end = datetime.datetime.strftime(period_end,"%Y%m%d")
        periods.append([period_start,period_end])
    
    return periods


