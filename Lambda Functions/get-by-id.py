import json
import os
import boto3

# Create DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['SAMPLE_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Validate HTTP method
    if event.get("httpMethod") != "GET":
        raise Exception(f"getMethod only accepts GET method, you tried: {event.get('httpMethod')}")

    print("Received event:", json.dumps(event))

    # Extract ID from pathParameters
    path_params = event.get("pathParameters") or {}
    item_id = path_params.get("id")

    if not item_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing ID in path parameters"})
        }

    try:
        # Fetch item by ID
        response = table.get_item(Key={"id": item_id})
        item = response.get("Item")
    except Exception as e:
        print("Error getting item:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    result = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    print(f"Response from: {event.get('path')} statusCode: {result['statusCode']} body: {result['body']}")
    return result
