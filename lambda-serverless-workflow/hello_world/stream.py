import json


def handle_insert(record):
    newImage = record["dynamodb"]["NewImage"]
    ticker   = newImage["ticker"]["S"]
    newTickerPrice = newImage["price"]["N"]
    timestamp      = newImage["timestamp"]["N"]
    print("ticker--->", ticker)
    print("newTickerPrice--->",newTickerPrice)
    print("timestamp",timestamp)
    print("Done handling INSERT Event")
    #return ("new event info",ticker,newTickerPrice,timestamp)

def lambda_handler(event, context):
    
    try:
        print("event-->",event)
        for record in event['Records']:
            if record['eventName'] == "INSERT":
                handle_insert(record)
    except Exception as e:
        print(e)
        return "Execption!"