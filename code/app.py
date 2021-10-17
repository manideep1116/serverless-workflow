import json
from yahoo_fin.stock_info import *
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import time
import os
# import requests

tickers = ["BTC-USD","ETH-USD","ADA-USD","DOGE-USD","VET-USD","AAL","AMC","DAL"]
table_name = os.environ['table_name']

def prices(tickers):
    """function to get prices from yahoo finance

    Returns
    ------
    list of prices

    """
    fav_stocks = {}
    for symbol in tickers:
        price = get_live_price(symbol)
        fav_stocks[symbol] = round(price,2)
    return(fav_stocks)

def add_item(item):
    """function to generate items for table

    Returns
    ------
    New row with attributes

    """
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
    """Lambda function to add prices to table

    Returns
    ------
    Adds items to the table

    """
    try:
        dynamodb = boto3.resource('dynamodb')
        items = prices(tickers)
        add_item(items)

    except Exception:
        return None
    