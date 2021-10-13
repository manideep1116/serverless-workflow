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

def create_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.create_table(
        TableName= table_name,
        KeySchema=[
            {
                'AttributeName': 'ticker',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'timestamp',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ticker',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )

    print("Table status:", table.table_status)

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

def query_prices(id):
 
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('ticker').eq(id),
        ScanIndexForward= False
    )
    print('response-->', response)
    for item in response['Items']:
        print(item)
    return response['Items']


def lambda_handler(event, context):
    """Sample pure Lambda function

  
    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

    """

    dynamodb = boto3.resource('dynamodb')    
    table_names = [table.name for table in dynamodb.tables.all()]

    if table_name not in table_names:
        create_table(table_name)
    items = prices(tickers)
    add_item(items)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Here are the values of stock values" + str(prices(tickers))  ,
            # "location": ip.text.replace("\n", "")
        }),
    }