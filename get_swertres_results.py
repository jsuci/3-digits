from datetime import datetime
from random import choice
from dotenv import find_dotenv, load_dotenv, set_key
from os import environ, read
from numpy import str_
from requests_html import HTMLSession, HTML
from pathlib import Path
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import json, pandas as pd


# environment
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)


def str_to_date(strDate):
    dateDate = datetime.strptime(strDate, "%d %a %b %Y").date()
    return dateDate

def date_to_str(dateDate):
    strDate = datetime.strftime(dateDate, "%d %a %b %Y").lower()
    return strDate

def fetch_html(entryDate, path):
    # headers
    with open("headers.json", "r") as f:
        headerList = list(json.load(f))
    header = choice(headerList)

    # file
    fp = Path(path)

    # fetch
    sess = HTMLSession()
    url = f"{environ['URL']}{entryDate.year}-{entryDate.month:02}"
    header["Host"] = "www.gidapp.com"
    r = sess.get(url, headers=header)

    # save
    print(f"downloading results {entryDate.year}-{entryDate.month}...")

    with open(fp, "w") as fo:
        fo.write(r.text)

    record_results(r.text)

    
def read_html(entryDate, path):
    # file
    fp = Path(path)

    # read
    print(f"reading results {entryDate.year}-{entryDate.month}...")
    with open(fp, "r") as fo:
        doc = fo.read()

    record_results(doc)


def record_results(htmlDoc):

    # dates
    currentDate = datetime.now().date()
    entryDate = str_to_date(environ["ENTRY_DATE"])
    
    entryYearMonth = f"{entryDate.year}-{entryDate.month}"
    currentYearMonth = f"{currentDate.year}-{currentDate.month}"

    # parse
    doc = HTML(html=htmlDoc)
    entries = doc.xpath("//div[contains(@id, 'suertres')]")

    # read
    df = pd.read_csv('pcso_3d_results.csv', dtype={'mid':str,'aft':str,'eve':str})




    # loop
    allWebDateRes = []
    for el in entries:
        webDate = date_to_str(datetime.strptime(
                el.xpath("//time/@datetime")[0], "%Y-%m-%d").date())
        webResults = list(map(lambda x: x.text, el.xpath("//tr[@class='top']/td")))

        if webDate in df.values:
            df.loc[
                df['date'] == webDate,
                ['mid', 'aft', 'eve']
            ] = [webResults[0], webResults[1], webResults[2]]

        else:
            webDateRes = {
                'date': webDate,
                'mid': webResults[0],
                'aft': webResults[1],
                'eve': webResults[2]
            }

            allWebDateRes.append(webDateRes)
        #     if entryDate < currentDate:
        #         print(webDate)
        #         df.loc[-1] = [webDate, webResults[0], webResults[1], webResults[2]]  # adding a row
        #         df.index = df.index + 1  # shifting index
        #         df.sort_index(inplace=True)
        #     else:
        #         to_append = [webDate, webResults[0], webResults[1], webResults[2]]
        #         df_length = len(df)
        #         df.loc[df_length] = to_append

    df = pd.concat([df, pd.DataFrame(allWebDateRes)])
    df.to_csv('pcso_3d_results.csv', index=False, header=True)



        # allWebDateRes.append(webDateRes)

    # export
    # exportData = pd.DataFrame(allWebDateRes)
    # if environ["HEADER"] == True:
    #     exportData.to_csv('pcso_3d_results.csv', index=False, mode='a', header=False)
    # else:
    #     exportData.to_csv('pcso_3d_results.csv', index=False, mode='a', header=True)

    

def main():
    # dates
    currentDate = datetime.now().date()
    entryDate = str_to_date(environ["ENTRY_DATE"])

    entryYearMonth = f"{entryDate.year}-{entryDate.month}"
    currentYearMonth = f"{currentDate.year}-{currentDate.month}"

    while True:
        path = Path(f"html/{entryDate.year}-{entryDate.month:02}.html")

        if path.is_file():
            read_html(entryDate, path)
        else:
            fetch_html(entryDate, path)

        if entryYearMonth == currentYearMonth:
            fetch_html(entryDate, path)
            environ["ENTRY_DATE"] = date_to_str(currentDate)
            set_key(dotenv_file, "ENTRY_DATE", environ["ENTRY_DATE"])
            break
        
        entryDate += relativedelta(months=1)
        entryYearMonth = f"{entryDate.year}-{entryDate.month}"

    # display results
    df = pd.read_csv('pcso_3d_results.csv', dtype={'mid':str,'aft':str,'eve':str})
    print(df.iloc[-1])
        

if __name__ == "__main__":
    main()
