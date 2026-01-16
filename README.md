# SecureGuard AI - Your Personal Network Security Co-Pilot

##  QUICK START

### 1. Run Local Demo
```bash
python3 demo.py
```

### 2. Deploy AWS Cloud (Simple Prototype)
If you have an AWS account (even a workshop one), you can deploy the backend in 1 minute:

```bash
# 1. Configure AWS Credentials
aws configure

# 2. Deploy Cloud Resources
python3 simple_aws/deploy.py

# 3. Run Demo again (it will auto-detect the cloud)
python3 demo.py
```


## Project Mission:

Turn cybersecurity from a, expert field gated by knowledge into a AI guided tool accessible to everyone prioritizing user autonomy and giving security back into the hands of the user 

---
### Whets unique about this project?:

We developed this project in response to growing user concerns about data security and the lack of transparency in modern cloud services seen in  issues like unprompted OneDrive syncing or loss of local file control. To address this, we built a privacy first project where all sensitive traffic analysis occurs locally on the user's network; only  threat patterns are ever processed in the cloud. The system functions as an  cyber defense tool that uses machine learning to analyze network behavior, predicting and stoping threats before they become problems for the user. 
---

##  System Architecture

### Three-Tier Architecture:

```
┌────────────────────────────────────────────────────────────┐
│                    LOCAL TIER (User's Machine)             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Network    │→ │   Traffic    │→ │  Local ML    │      │
│  │   Capture    │  │  Analyzer    │  │  Processor   │      │
│  │  (Pcap/Raw)  │  │  (Parser)    │  │  (Anomaly)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                                     ↓            │
│  ┌──────────────────────────────────────────────────┐      │
│  │        Secure Agent (Python/ Desktop App)        │      │
│  └──────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────┘
                            ↓ (Encrypted Data)
┌────────────────────────────────────────────────────────────┐
│                    AWS CLOUD TIER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  API Gateway │→ │    Lambda    │→ │  Bedrock AI  │      │
│  │   (Auth)     │  │  (Processor) │  │  (Analysis)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         ↓                ↓                    ↓            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  DynamoDB    │  │  SageMaker   │  │  S3 Threat   │      │
│  │  (User Data) │  │  (ML Model)  │  │  Intelligence│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Web Dashboard│  │  CLI Tool    │  │  Mobile App  │      │
│  │ (React)      │  │  (Optional)  │  │  (Possible)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────────────────────────────────────┘
```

---

##  Exact AWS Services & Their Roles

### Core AI/ML Services:

| Service | Purpose | Specific Use Case |
|---------|---------|-------------------|
| **Amazon Bedrock** | Primary AI/ML Engine | - Conversational interface (Claude 3.5)<br>- Threat explanation generation<br>- Remediation step generation<br>- Natural language query processing |
| **Amazon SageMaker** | Custom ML Models | - Train anomaly detection model on network patterns<br>- Build threat classification model<br>- Deploy real-time inference endpoints |
| **Amazon Rekognition** (Optional) | Visual Analysis | - Analyze network topology diagrams<br>- OCR for security certificates |

### Infrastructure Services:

| Service | Purpose | Configuration Details |
|---------|---------|----------------------|
| **AWS Lambda** | Serverless Compute | **Functions:**<br>- `ProcessTelemetry`: Process incoming network data<br>- `AnalyzeThreat`: Run ML inference<br>- `GenerateRemediation`: Create fix scripts<br>- `UpdateThreatDB`: Update threat intelligence<br>**Runtime:** Python 3.11<br>**Memory:** 1024-3008 MB<br>**Timeout:** 30-60 seconds |
| **Amazon API Gateway** | API Management | **Type:** REST API<br>**Auth:** Amazon Cognito<br>**Endpoints:**<br>- `/analyze` (POST)<br>- `/query` (POST)<br>- `/remediate` (POST)<br>- `/threats` (GET) |
| **Amazon DynamoDB** | NoSQL Database | **Tables:**<br>1. `Users` (user_id, email, settings)<br>2. `ThreatEvents` (event_id, timestamp, severity)<br>3. `NetworkBaselines` (user_id, baseline_data)<br>4. `RemediationHistory` (user_id, actions_taken)<br>**Provisioned:** On-demand |
| **Amazon S3** | Object Storage | **Buckets:**<br>- `secureguard-threat-signatures`: Threat patterns<br>- `secureguard-ml-models`: ML model artifacts<br>- `secureguard-reports`: Generated reports<br>**Encryption:** SSE-S3 |
| **Amazon Cognito** | User Authentication | **User Pool:** Email/password auth<br>**MFA:** Optional TOTP<br>**OAuth:** Future integration |
| **AWS Secrets Manager** | Credentials Management | Store API keys, database credentials |
| **Amazon CloudWatch** | Monitoring & Logs | **Metrics:**<br>- Lambda invocations<br>- API latency<br>- Threat detection rate<br>**Alarms:** Error rate > 5% |
| **AWS Systems Manager** | Parameter Store | Configuration management, feature flags |
| **Amazon EventBridge** | Event Orchestration | Trigger workflows on threat detection |
| **Amazon SNS** | Notifications | Alert users via email/SMS for critical threats |
| **Amazon VPC** | Network Security | Isolate Lambda functions, control egress |

### Optional Advanced Services:

| Service | Purpose | When to Use |
|---------|---------|-------------|
| **Amazon GuardDuty** | AWS-native Threat Detection | Cross-reference local findings with AWS intelligence |
| **AWS Security Hub** | Centralized Security View | Aggregate findings across services |
| **Amazon Macie** | Data Privacy | Detect sensitive data in network traffic logs |
| **AWS IoT Core** | IoT Device Security | If expanding to IoT device monitoring |

---

## Roadmap

### AWS Backend 

Use **AWS CDK** (Python or TypeScript)

```typescript
// Example CDK Stack Structure
const app = new cdk.App();

const networkStack = new NetworkStack(app, 'SecureGuardNetwork', {
  vpcCidr: '10.0.0.0/16'
});

const dataStack = new DataStack(app, 'SecureGuardData', {
  threatTableName: 'ThreatEvents',
  userTableName: 'Users'
});

const computeStack = new ComputeStack(app, 'SecureGuardCompute', {
  vpc: networkStack.vpc,
  tables: dataStack.tables
});

const aiStack = new AIStack(app, 'SecureGuardAI', {
  bedrockModel: 'anthropic. claude-3-5-sonnet-20241022-v2: 0',
  sagemakerEndpoint: 'threat-classifier'
});
```

#### Lambda Functions: 

1. **ProcessTelemetry** (`process_telemetry.py`)
   ```python
   import boto3
   import json
   
   bedrock = boto3.client('bedrock-runtime')
   dynamodb = boto3.resource('dynamodb')
   
   def handler(event, context):
       # 1. Validate incoming data
       # 2. Store in DynamoDB
       # 3. Trigger analysis if anomaly detected
       # 4. Return acknowledgment
   ```

2. **AnalyzeThreat** (`analyze_threat.py`)
   ```python
   def handler(event, context):
       # 1. Retrieve telemetry from DynamoDB
       # 2. Call SageMaker endpoint for classification
       # 3. Enrich with Bedrock context
       # 4. Store analysis results
   ```

3. **GenerateRemediation** (`generate_remediation.py`)
   ```python
   def handler(event, context):
       # 1. Get threat details
       # 2. Call Bedrock with prompt: 
       #    "Generate step-by-step remediation for [threat_type]
       #     on [os_type] with [network_config]"
       # 3. Format as executable script
       # 4. Return to user
   ```

#### Deployment Script:
```bash
#!/bin/bash
# deploy.sh

# Install dependencies
pip install -r requirements. txt

# Bootstrap CDK
cdk bootstrap aws://ACCOUNT-ID/REGION

# Deploy stacks
cdk deploy SecureGuardNetwork --require-approval never
cdk deploy SecureGuardData --require-approval never
cdk deploy SecureGuardCompute --require-approval never
cdk deploy SecureGuardAI --require-approval never

# Output API endpoint
aws cloudformation describe-stacks \
  --stack-name SecureGuardCompute \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
  --output text
```

---

###  ML Model Training 

#### Dataset: 
- **Public Dataset:** [CICIDS2017](https://www.unb.ca/cic/datasets/ids-2017.html) or [KDD Cup 99](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)
- **Features:** Packet size, protocol, port, timing, byte distribution

#### Training Pipeline (SageMaker):

```python
import sagemaker
from sagemaker.sklearn import SKLearn

# Define training script
sklearn_estimator = SKLearn(
    entry_point='train. py',
    framework_version='1.2-1',
    instance_type='ml.m5.xlarge',
    role=sagemaker_role,
    hyperparameters={
        'algorithm': 'random_forest',
        'n_estimators': 100,
        'max_depth': 20
    }
)

# Train model
sklearn_estimator.fit({'train': 's3://bucket/train-data'})

# Deploy endpoint
predictor = sklearn_estimator.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium',
    endpoint_name='threat-classifier'
)
```

#### Model Outputs:
- **Classification:** Benign, Port Scan, DDoS, Malware, Data Exfiltration
- **Confidence Score:** 0.0 - 1.0
- **Feature Importance:** Which traffic characteristics triggered the alert

---

### : Bedrock AI Integration 

#### Conversational Interface: 

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def chat_with_ai(user_query, threat_context):
    prompt = f"""You are a cybersecurity expert assistant. 
    
    Network Context: {threat_context}
    User Question: {user_query}
    
    Provide a clear, actionable response.  If this is a threat, explain: 
    1. What is happening
    2. Why it's dangerous
    3. Exact steps to resolve it
    
    Be concise but thorough."""
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content":  prompt}
            ]
        })
    )
    
    return json.loads(response['body'].read())
```

#### Remediation Generation:

```python
def generate_remediation_script(threat_type, os_type):
    prompt = f"""Generate a safe, executable script to remediate this threat:
    
    Threat: {threat_type}
    Operating System: {os_type}
    
    Requirements:
    - Include explanatory comments
    - Add safety checks
    - Provide rollback steps
    - Use standard tools (iptables, netsh, etc.)
    
    Output only the script, properly formatted."""
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )
    
    return parse_script(response)
```

---

###  Web Dashboard 

#### Tech Stack:
- **Frontend:** React 18 + TypeScript
- **UI Library:** AWS Amplify UI Components
- **Charts:** Recharts or D3.js
- **State:** React Query + Zustand
- **Hosting:** AWS Amplify Hosting

#### Key Features: 

1. **Real-Time Dashboard**
   ```tsx
   // Network health score (0-100)
   // Active threats timeline
   // Traffic volume charts
   // Top protocols/ports
   ```

2. **Threat Details View**
   ```tsx
   // Threat severity (Critical/High/Medium/Low)
   // Affected devices
   // Attack timeline
   // AI explanation
   // Remediation options
   ```

3. **User infomation Chat Interface**
   ```tsx
   // Chat widget 
   // auto generates questions for the user
   // What  
   ```

#### Deployment:
```bash
# Initialize Amplify
amplify init

# Add hosting
amplify add hosting

# Configure API
amplify add api

# Deploy
amplify push
amplify publish
```

---

##  Security & Privacy Considerations

### Privacy-First Design: 

1. **Local Processing:**
   - All raw packet data stays on user's machine
   - Only encrypted data sent to cloud: 
     - Traffic volume statistics
     - Protocol distributions

2. **Data Encryption:**
   - In-transit: TLS 1.3 for all API calls
   - At-rest: S3/DynamoDB encryption enabled
   - Client-side:  Encrypt sensitive configs with user password

3. **Compliance:**
   - GDPR:  User data deletion on request
   - CCPA: Data export functionality
   - No PII collection without consent

### Security Measures:

```python
# Example:  Data sanitization before cloud upload
def sanitize_telemetry(raw_packet):
    return {
        'timestamp': packet. timestamp,
        'protocol': packet.protocol,
        'src_port': packet.src_port,
        'dst_port': packet. dst_port,
        'packet_size': packet.size,
        'flags': packet.flags,
        # NO IPs, NO payloads, NO identifiable data
        'src_ip_hash': hashlib.sha256(packet.src_ip).hexdigest()[: 8],
        'dst_ip_hash': hashlib.sha256(packet.dst_ip).hexdigest()[:8]
    }
```

---

##  Scalability Architecture

### Scaling Strategies:

| Component | Current (POC) | Scale to 10K Users | Scale to 100K Users |
|-----------|---------------|-------------------|---------------------|
| **Lambda** | On-demand | Provisioned concurrency (50) | Auto-scaling (500-5000) |
| **DynamoDB** | On-demand | Provisioned (1000 WCU/RCU) | Global Tables + DAX caching |
| **SageMaker** | Single endpoint | Multi-model endpoint | Auto-scaling endpoints + batch transform |
| **S3** | Standard | Intelligent-Tiering | CloudFront CDN for threat signatures |
| **API Gateway** | Regional | Edge-optimized | Multi-region active-active |
| **Bedrock** | On-demand | Reserved capacity | Multi-region failover |
---

---

##  Deliverables Checklist

- [ ] Desktop agent (Windows/Mac/Linux)
- [ ] AWS infrastructure (CDK code)
- [ ] ML model (trained + deployed)
- [ ] Web dashboard (deployed on Amplify)
- [ ] API documentation (Swagger/OpenAPI)
- [ ] GitHub repository with README
- [ ] Demo video (2-3 minutes)
- [ ] Presentation slides
- [ ] Architecture diagram (draw.io or Lucidchart)

---

##  Quick Start Commands

```bash
# Clone repository
git clone https://github.com/JJEA12/KingHacks---Project
cd KingHacks---Project

# Backend deployment
cd infrastructure
npm install
cdk deploy --all

# Frontend deployment
cd ../dashboard
npm install
npm run build
amplify publish

# Desktop agent
cd ../agent
pip install -r requirements.txt
python main.py

# ML model training
cd ../ml-models
python train.py --dataset cicids2017 --output s3://bucket/models
python deploy.py --endpoint threat-classifier
```


##  Resources & References

### AWS Documentation:
- [Amazon Bedrock Developer Guide](https://docs.aws.amazon.com/bedrock/)
- [SageMaker Examples](https://github.com/aws/amazon-sagemaker-examples)
- [CDK Patterns](https://cdkpatterns.com/)

### Datasets:
- [CICIDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)
- [NSL-KDD](https://www.unb.ca/cic/datasets/nsl. html)

### Libraries:
- [Scapy](https://scapy.net/) - Packet manipulation
- [Zeek](https://zeek.org/) - Network analysis framework


