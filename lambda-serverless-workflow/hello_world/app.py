import json
from yahoo_fin.stock_info import *
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import json
import time
# import requests

tickers = ["BTC-USD"]
# tickers = ["BTC-USD","ETH-USD","ADA-USD", "DOGE-USD","VET-USD","AAL","AMC"]
table_name = 'stockprices'

def prices(tickers):
    fav_stocks = {}
    for symbol in tickers:
        price = get_live_price(symbol)
        fav_stocks[symbol] = round(price,2)
    return(fav_stocks)

def add_item(item):
    ddb_data= json.loads(json.dumps(item), parse_float=Decimal)
    dynamodb = boto3.resource('dynamodb') 
    table = dynamodb.Table(table_name)
    for key in ddb_data: 
        response = table.put_item(
            Item={
                'ticker':  key,
                'timestamp': int(round(time.time() * 1000)),
                'price': ddb_data[key]
            }
        )
    return response
        

def lambda_handler(event, context):
    """Sample pure Lambda function

  
    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

    """
    try:
        dynamodb = boto3.resource('dynamodb')
        items = prices(tickers)
        add_item(items)

    except Exception as e:
        print(e)
        return "Exception!"
    