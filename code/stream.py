import json
import boto3
from boto3.dynamodb.conditions import Key
import os

table_name   =  os.environ['table_name']

SENDER       = os.environ['sender']

RECIPIENT    = os.environ['recipient']

AWS_REGION   = os.environ['region']

percent_change = os.environ['percent_change']


def ses_email(message):
    """function to generate email message

    Returns
    ------
    Emails the user form Amazon SES

    """
    ses = boto3.client('ses',region_name=AWS_REGION)
    CHARSET = "UTF-8"
    SUBJECT = "Serverless-Workflow for Stocks and Crypto Volatility"
    BODY    = """
Hello, 

Here's an update on your favourite Stock/Crypto price movements.

%s
	
Regards,
Manideep
            """%message
    try:

        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except Exception as e:
        print(e)


def query_prices(id):
    """function to query prices from the table

    Returns
    ------
    list of all the prices in the table for a specific ticker

    """
 
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(table_name)
    response = table.query(
        KeyConditionExpression=Key('ticker').eq(id),
        ScanIndexForward= False
    )
    values = response['Items']
    return values  

def find_Volatility(values):
    """function to compare the prices

    Returns
    ------
    Percentage of Volatility

    """
    item_values = values[:2]
    ticker = item_values[0]['ticker']
    volatile_values = []
    for item in item_values:
        value = float(item['price'])
        volatile_values.append(value)

    if len(volatile_values) ==1:
        pass
    else:
        if volatile_values[0]>volatile_values[1]:
            increase = volatile_values[0] - volatile_values[1]
            increase_percent = int((increase/volatile_values[1])*100)
            if increase_percent > percent_change:
                message = ("There is volatility in the market. The price of "+ ticker +" has rised by "+str(increase_percent)+"%" + " with current price " +str(volatile_values[0]))
                ses_email(message)
        elif volatile_values[0] == volatile_values[1]:
            pass
        else:
            decrease = volatile_values[1] - volatile_values[0]
            decrease_percent = int((decrease/volatile_values[1])*100)
            if decrease_percent > percent_change:
                message = ("There is volatility in the market. The price of "+ ticker +" has dropped by "+str(decrease_percent)+"%" + " with current price " +str(volatile_values[0]))
                ses_email(message)


def handle_insert(record):
    """trigger when the event type is INSERT
   
    Returns
    ------
    Volatility

    """
    newImage = record["dynamodb"]["NewImage"]
    ticker   = newImage["ticker"]["S"]
    newTickerPrice = newImage["price"]["N"]
    timestamp      = newImage["timestamp"]["N"]
    values = query_prices(ticker)
    return find_Volatility(values)



def lambda_handler(event, context):
    """Lambda function to find the Volatility

    Returns
    ------
    Volatility in percents

    """
    
    try:
        print("event-->",event)
        for record in event['Records']:
            print("record--->",record)
            if record['eventName'] == "INSERT":
                handle_insert(record)
                
    except Exception as e:
        print(e)
        return "Exception!"

# event = {'Records': [{'eventID': '1659f5ab548b4c50eea09477f61b8c20', 'eventName': 'INSERT', 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'us-east-1', 'dynamodb': {'ApproximateCreationDateTime': 1634164478.0, 'Keys': {'ticker': {'S': 'AMC'}, 'timestamp': {'N': '1634164477920'}}, 'NewImage': {'ticker': {'S': 'AMC'}, 'price': {'N': '110'}, 'timestamp': {'N': '1634164477920'}}, 'SequenceNumber': '800000000019080192835', 'SizeBytes': 59, 'StreamViewType': 'NEW_AND_OLD_IMAGES'}, 'eventSourceARN': 'arn:aws:dynamodb:us-east-1:962368282980:table/stockprices/stream/2021-10-13T22:31:24.749'}]}

