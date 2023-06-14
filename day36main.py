import requests
import os
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY= os.environ.get("NEWS_API_KEY")
NEWS_API_KEY=os.environ.get("NEWS_API_KEY")
account_sid=os.environ.get("ACCOUNT_SID")
auth_token=os.environ.get("AUTH_TOKEN")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


stock_para={
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":STOCK_NAME,
    "apikey":API_KEY,
    "outputsize":"compact"
}
stock_data=requests.get(STOCK_ENDPOINT,params=stock_para)
data=stock_data.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]

#print(data_list)

yeseterday_data=data_list[0]
yesterday_price=yeseterday_data["4. close"]
#print(yesterday_price)


day_before_yeseterday_data=data_list[1]
day_before_yesterday_price=day_before_yeseterday_data["4. close"]
#print(day_before_yesterday_price)



differnce=abs(float(day_before_yesterday_price)-float(yesterday_price))

#print(differnce)


diff_percent=(differnce/float(yesterday_price))*100
#print(diff_percent)

if diff_percent>2:
    news_para={
        "apiKey":NEWS_API_KEY,
        "qInTitle":COMPANY_NAME,

    }
    news_response=requests.get(NEWS_ENDPOINT,params=news_para)
    articles=news_response.json()["articles"]
    three_articles=articles[:3]
    #print(three_articles)


    edit_msg=[f"Headline : {article['title']}.\nBrief: {article['description']}" for article in three_articles]

client = Client(account_sid, auth_token)
for article in edit_msg:
    message = client.messages \
                    .create(
                        body=article,
                        from_='+14302335453',
                        to='ENTER YOUR NUMBER'
                    )

#print(message.status)
