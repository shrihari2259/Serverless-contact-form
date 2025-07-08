import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Create DynamoDB resource and table
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['SAMPLE_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Check HTTP method
    if event.get("httpMethod") != "GET":
        raise Exception(f"getAllItems only accepts GET method, you tried: {event.get('httpMethod')}")

    print("Received event:", json.dumps(event))

    try:
        # Scan table to get all items (up to 1MB)
        response = table.scan()
        items = response.get('Items', [])
    except Exception as e:
        print("Error scanning table:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    result = {
        "statusCode": 200,
        "body": json.dumps(items)
    }

    print(f"Response from: {event.get('path')} statusCode: {result['statusCode']} body: {result['body']}")
    return result
