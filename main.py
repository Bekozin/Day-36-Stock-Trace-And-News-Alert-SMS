import requests
import datetime
import os
from twilio.rest import Client

Previous_Date_Raw = datetime.datetime.today() - datetime.timedelta(days=1)
date = str(Previous_Date_Raw).split(" ")
Previous_Date = date[0]

The_Day_Before_Raw = datetime.datetime.today() - datetime.timedelta(days=2)
date = str(The_Day_Before_Raw).split(" ")
The_Day_Before = date[0]

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")

STOCK_REWUEST_LINK = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=9QIJPEJTJRRLYYUS"

response = requests.get(STOCK_REWUEST_LINK)
previous_day = (response.json()['Time Series (Daily)'][Previous_Date]['4. close'])
the_day_before = (response.json()['Time Series (Daily)'][The_Day_Before]['4. close'])

Close_Price_the_day_before = float(the_day_before)
Close_Price_previous_day = float(previous_day)

Positive_difference = abs(Close_Price_the_day_before - Close_Price_previous_day)


def check_the_warning(pay, payda):
    warning_cross = float(pay) * 100 / float(payda)

    if warning_cross >= 5:
        print(f"%{warning_cross}")
        print("Sıçanzi fakirleştin")

    else:
        print(f"%{warning_cross}")
        print("No Problem")


check_the_warning(Positive_difference, Close_Price_the_day_before)

new_parameters = {
    "apiKey": os.environ.get("NEWS_API_KEY"),
    "qInTitle": COMPANY_NAME
}

new_response = requests.get(NEWS_ENDPOINT, params=new_parameters)
articles = new_response.json()["articles"]
three_articles_needed = articles[:3]


formatted_articles = [f"Headline {article['title']}. \nBrief: {article['description']}" for article in
                      three_articles_needed]
print(formatted_articles)


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_='Twilio number linked to account',
        to='+905306751864'
    )

print(message.sid)
