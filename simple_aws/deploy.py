import boto3
import json
import time
import os
import zipfile
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# CONFIGURATION
REGION = os.getenv('AWS_REGION', 'us-east-1')
PROJECT_NAME = 'SecureGuard'
TABLE_NAME = f'{PROJECT_NAME}-Threats'
FUNCTION_NAME = f'{PROJECT_NAME}-Backend'

def zip_function(filename="function.zip"):
    print("📦 Zipping Lambda function...")
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write('lambda_function.py')
    print("✅ Zipped.")
    return filename

def deploy():
    print(f"🚀 Deploying {PROJECT_NAME} simple prototype to {REGION}...")
    
    # Initialize Clients
    session = boto3.Session(region_name=REGION)
    dynamodb = session.resource('dynamodb')
    lambda_client = session.client('lambda')
    iam = session.client('iam')
    
    # 1. Create DynamoDB Table
    print(f"\n  Checking DynamoDB Table '{TABLE_NAME}'...")
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'item_id', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'item_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("   Creating table...")
        table.wait_until_exists()
        print(" Table created!")
    except Exception as e:
        if 'ResourceInUseException' in str(e):
            print(" Table already exists.")
        else:
            print(f" Error creating table: {e}")
            return

    # 2. Use Existing IAM Role (Workshop Mode)
    # The user provided a specific account, and likely needs to use the pre-created WSParticipantRole
    # Standard format: arn:aws:iam::<ACCOUNT_ID>:role/WSParticipantRole
    role_arn = 'arn:aws:iam::858134376728:role/WSParticipantRole'
    print(f"\n2️⃣  Using Existing IAM Role: {role_arn}")
    
    # We skip creating the role because in Workshop environments, we often lack permissions to create IAM roles.
    # We assume 'WSParticipantRole' already has the necessary permissions (DynamoDB access, Lambda execution).


    # 3. Deploy Lambda Function
    print(f"\n3️⃣  Deploying Lambda Function '{FUNCTION_NAME}'...")
    zip_file = zip_function()
    
    with open(zip_file, 'rb') as f:
        zipped_code = f.read()
    
    try:
        lambda_client.create_function(
            FunctionName=FUNCTION_NAME,
            Runtime='python3.11',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zipped_code},
            Environment={
                'Variables': {'TABLE_NAME': TABLE_NAME}
            },
            Timeout=15
        )
        print("✅ Function created.")
    except lambda_client.exceptions.ResourceConflictException:
        print("   Function exists, updating code...")
        lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zipped_code
        )
        print("✅ Function updated.")
    except Exception as e:
        print(f"❌ Error deploying function: {e}")
        return

    # 4. Create Function URL (Public access for simplicity)
    print(f"\n4️⃣  Creating Function URL...")
    try:
        response = lambda_client.create_function_url_config(
            FunctionName=FUNCTION_NAME,
            AuthType='NONE'
        )
        func_url = response['FunctionUrl']
    except lambda_client.exceptions.ResourceConflictException:
        response = lambda_client.get_function_url_config(FunctionName=FUNCTION_NAME)
        func_url = response['FunctionUrl']
    
    # Add permission for public access
    try:
        lambda_client.add_permission(
            FunctionName=FUNCTION_NAME,
            StatementId='FunctionURLAllowPublicAccess',
            Action='lambda:InvokeFunctionUrl',
            Principal='*',
            FunctionUrlAuthType='NONE'
        )
    except lambda_client.exceptions.ResourceConflictException:
        pass

    print(f"\n✅ SUCCESS! Deployment Complete.")
    print("="*60)
    print(f"API Endpoint: {func_url}")
    print("="*60)
    
    # Update .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    print(f"\nUpdating .env file at {env_path}...")
    
    # Create or append to .env
    env_content = ""
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
            # Filter out old keys
            lines = [l for l in lines if not l.startswith('API_GATEWAY_URL=') and not l.startswith('AWS_REGION=')]
            env_content = "".join(lines)
            if not env_content.endswith('\n'):
                env_content += '\n'
    
    with open(env_path, 'w') as f:
        f.write(env_content)
        f.write(f"AWS_REGION={REGION}\n")
        f.write(f"API_GATEWAY_URL={func_url}\n") # Using function URL as the API endpoint
    
    print("✅ .env updated with new API URL.")

if __name__ == '__main__':
    deploy()
