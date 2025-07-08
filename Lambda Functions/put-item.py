import json
import os
import boto3

# Create DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['SAMPLE_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Validate HTTP method
    if event.get("httpMethod") != "POST":
        raise Exception(f"postMethod only accepts POST method, you tried: {event.get('httpMethod')} method.")

    print("Received event:", json.dumps(event))

    # Parse the request body
    try:
        body = json.loads(event.get("body", "{}"))
        item = {
            "id": body["id"],
            "name": body["name"],
            "email": body["email"],
            "message": body["message"]
        }
    except (json.JSONDecodeError, KeyError) as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Invalid request body: {str(e)}"})
        }

    # Put item into DynamoDB
    try:
        response = table.put_item(Item=item)
        print("Success - item added or updated:", response)
    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    # Response
    return {
        "statusCode": 200,
        "body": json.dumps(item),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Content-Type": "application/json",
            "Access-Control-Allow-Methods": "*"
        }
    }
