import json
import boto3
import os
import time
from decimal import Decimal

# Helper class to convert Python objects to DynamoDB format
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'SecureGuard-Threats')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    try:
        # Handle cases where the body might be a string or already a dict
        body = event.get('body', '{}')
        if isinstance(body, str):
            payload = json.loads(body)
        else:
            payload = body
            
        # Basic validation
        if not payload:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Empty payload'})
            }

        timestamp = payload.get('timestamp', str(time.time()))
        telemetry_items = payload.get('telemetry', [])
        saved_count = 0
        
        # Process items - in this simple version, we only save "threats" 
        # or items with high anomaly scores to save DB costs
        for item in telemetry_items:
            # Check if it's a threat or just telemetry
            is_threat = False
            if item.get('is_threat'):
                is_threat = True
            elif item.get('anomaly_score', 0) > 0.7:  # Example threshold
                is_threat = True
            
            # If it's interesting, save it
            if is_threat or True: # For prototype, let's save everything to see it working
                # Add partition key and sort key if missing
                if 'item_id' not in item:
                     item['item_id'] = f"{timestamp}-{os.urandom(4).hex()}"
                
                # DynamoDB needs all numbers to be Decimals or Strings, but boto3 handles floats often.
                # Simplest is to wrap put_item.
                
                # Structure for DynamoDB
                db_item = {
                    'item_id': item['item_id'],     # Partition Key
                    'timestamp': timestamp,         # Sort Key
                    'data': item
                }
                
                table.put_item(Item=db_item)
                saved_count += 1

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data received', 
                'saved_items': saved_count
            })
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
