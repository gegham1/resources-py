import json
import logging
import os
import uuid
from datetime import datetime

import boto3

dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])
    if 'title' not in data or 'src' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the resource.")

    timestamp = str(datetime.utcnow().timestamp())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'title': data['title'],
        'src': data['src'],
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    table.put_item(Item=item)

    response = {
        "isBase64Encoded": False,
        "headers": {},
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
