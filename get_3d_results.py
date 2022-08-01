from datetime import datetime
from dotenv import find_dotenv, load_dotenv, set_key
from os import environ, getenv
from dateutil.relativedelta import relativedelta
from random import choice
import json, pandas as pd
from requests_html import HTMLSession, HTML

DOTENV_FILE = find_dotenv()
load_dotenv(DOTENV_FILE)

def fetch_results(entryDate):
    # construct headers and url
    with open("headers.json", "r") as f:
        headerList = list(json.load(f))
    headerChoice = choice(headerList)
    headerChoice["Host"] = "www.gidapp.com"
    url = f"http://128.199.93.100/lottery/philippines/pcso/suertres/month/{entryDate}"

    # fetch resources
    print(f'fetching results {entryDate}.')
    sess = HTMLSession()
    r = sess.get(url, headers=headerChoice)

    # return htmlStr
    return r.text



def save_results(htmlStr):
    # parse htmlObj
    doc = HTML(html=htmlStr)
    entries = doc.xpath("//div[contains(@id, 'suertres')]")

    # read existing results
    df = pd.read_csv('pcso_3d_results.csv', dtype={'mid':str,'aft':str,'eve':str})



    # loop through all entries
    allWebDateRes = []
    for el in entries:
        webDateObj = datetime.strptime(el.xpath("//time/@datetime")[0], "%Y-%m-%d").date()
        webDateStr = datetime.strftime(webDateObj, "%d %a %b %Y").lower()
        webResults = list(map(lambda x: x.text, el.xpath("//tr[@class='top']/td")))


        if webDateStr in df['date'].values:
            df.loc[
                df['date'] == webDateStr,
                ['mid', 'aft', 'eve']
            ] = [webResults[0], webResults[1], webResults[2]]

        else:
            webDateRes = {
                'date': webDateStr,
                'mid': webResults[0],
                'aft': webResults[1],
                'eve': webResults[2]
            }


            allWebDateRes.append(webDateRes)



    # save to existing entries
    print(f"saving results.")
    df = pd.concat([df, pd.DataFrame(allWebDateRes)])
    df.to_csv('pcso_3d_results.csv', index=False, header=True)

    print(df.iloc[-1])
    print('\n\n')


def update_results():
    # read existing results
    df = pd.read_csv('pcso_3d_results.csv', dtype={'mid':str,'aft':str,'eve':str})

    # attach current date to end of results
    currentDateObj = datetime.now().date()
    currentDateStr = datetime.strftime(currentDateObj, "%d %a %b %Y").lower()
    if currentDateStr not in df.values:
        df.loc[len(df.index)] = [currentDateStr, '-', '-', '-']

    # update last entry date
    environ["LAST_ENTRY_DATE"] = df["date"].iloc[-1]
    set_key(DOTENV_FILE, "LAST_ENTRY_DATE", environ["LAST_ENTRY_DATE"])



def date_list():
    # get current date
    currentDateObj = datetime.now().date()

    # get entry date in dateObj format
    lastEntryDate = environ["LAST_ENTRY_DATE"]
    lastEntryDateObj = datetime.strptime(lastEntryDate, "%d %a %b %Y").date()
    
    # generate list of entrydate in dateObj format
    entryDates = []
    lastEntryYearMonth = f"{lastEntryDateObj.year}-{lastEntryDateObj.month:02}"
    currentYearMonth = f"{currentDateObj.year}-{currentDateObj.month:02}"

    entryDates.append(lastEntryYearMonth)
    
    while lastEntryYearMonth != currentYearMonth:

        lastEntryDateObj += relativedelta(months=1)
        lastEntryYearMonth = f"{lastEntryDateObj.year}-{lastEntryDateObj.month:02}"

        entryDates.append(lastEntryYearMonth)

    return entryDates



def main():
    for everyDate in date_list():
        htmlStr = fetch_results(everyDate)
        save_results(htmlStr)
    
    update_results()


if __name__ == "__main__":
    main()