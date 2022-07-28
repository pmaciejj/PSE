
import os
import wget
import glob
import datetime
import pandas as pd

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

main_path = os.path.realpath(__file__)
main_path = os.path.dirname(main_path)

data_path  = os.path.join(main_path,"pse_dane")
if not os.path.isdir(data_path):
    os.mkdir(data_path)

period_from = "2017-01"
period_to = "2022-06"

# generacja oze - wiatr i fotowoltaika
## https://www.pse.pl//getcsv/-/export/csv/PL_GEN_WIATR/data_od/20220101/data_do/20220108
oze_url = r"https://www.pse.pl//getcsv/-/export/csv/PL_GEN_WIATR/data_od/start_date_paceholder/data_do/end_date_placeholder"

# wielkosci podstawowe
## https://www.pse.pl/getcsv/-/export/csv/PL_WYK_KSE/data_od/20220701/data_do/20220712
wp_url = r"https://www.pse.pl/getcsv/-/export/csv/PL_WYK_KSE/data_od/start_date_paceholder/data_do/end_date_placeholder"

# dobieranie danych
periods_list = periods_gen(period_from,period_to)
for period in periods_list:

    start_date = period[0]
    end_date = period[1]

    period_oze_url = oze_url.replace("start_date_paceholder",start_date).replace("end_date_placeholder",end_date)
    period_wp_url = wp_url.replace("start_date_paceholder",start_date).replace("end_date_placeholder",end_date)

    period_oze_file =  os.path.join(data_path,"OZE_" + start_date + "_" + end_date + ".csv")
    period_wp_file =os.path.join(data_path,"WP_" + start_date + "_" + end_date + ".csv")

    if not os.path.isfile(period_oze_file):
        wget.download(period_oze_url,period_oze_file)
    if not os.path.isfile(period_wp_file):
       wget.download(period_wp_url,period_wp_file)


# tworzenie jednego zbiorczego pliku OZE.csv
if os.path.isfile(data_path + "/OZE.csv"):
    os.remove(data_path + "/OZE.csv")

for i,f in enumerate(glob.glob(data_path + "/OZE*.csv")):

    if i == 0:
        df = pd.read_csv(f,encoding_errors="ignore",sep=";")
    else:
        oze = pd.read_csv(f,encoding_errors="ignore",sep=";")
        df = pd.concat([df,oze])

df.to_csv(data_path + "/OZE.csv",index_label=False,index=False,sep = ";")

# tworzenie jednego zbiorczego pliku WP.csv
if os.path.isfile(data_path + "/WP.csv"):
    os.remove(data_path + "/WP.csv")

cols_to_del = ["Generacja IRZ","Generacja PI"]

for i,f in enumerate(glob.glob(data_path + "/WP*.csv")):

    wp = pd.read_csv(f,encoding_errors="ignore",sep=";")

    cols_to_del = ["Generacja IRZ","Generacja PI"]
    cols = wp.columns.to_list()
    for c in cols_to_del:
        if c in cols:
            wp.drop(columns=c,inplace=True)

    if i == 0:
        df = wp.copy()

    else:
        df = pd.concat([df,wp])

df.to_csv(data_path + "/WP.csv",index_label=False,index=False,sep=";")