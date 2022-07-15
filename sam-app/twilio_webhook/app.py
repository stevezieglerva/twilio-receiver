import json

# import requests


def lambda_handler(event, context):

    print(json.dumps(event, indent=3, default=str))

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
