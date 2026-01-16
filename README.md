# SecureGuard AI - Your Personal Network Security Co-Pilot

##  QUICK START (New Machine Setup)

### Step 1: Install Python 3.12+

**Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install python3 python3-pip git
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3 python3-pip git
```

**macOS:**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.12 git
```

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2.  Check "Add Python to PATH" during installation
3. Install Git from [git-scm.com](https://git-scm.com/download/win)

### Step 2: Clone & Install Dependencies

**Linux/macOS:**
```bash
# Clone the repository
git clone https://github.com/JJEA12/KingHacks---Project.git
cd KingHacks---Project

# Install Python dependencies
pip3 install -r agent/requirements.txt
pip3 install streamlit pandas plotly
```

**Windows (PowerShell/CMD):**
```powershell
# Clone the repository
git clone https://github.com/JJEA12/KingHacks---Project.git
cd KingHacks---Project

# Install Python dependencies
pip install -r agent/requirements.txt
pip install streamlit pandas plotly
```

### Step 3: Run the Security Agent (Backend)
This simulates network traffic and detects threats using local ML:

**Linux/macOS:**
```bash
python3 demo.py
```

**Windows:**
```powershell
python demo.py
```

**What you'll see:** Terminal output showing simulated network packets and detected threats (Port Scans, DDoS attempts).

### Step 4: Launch the Visual Dashboard (Frontend)
Open a **new terminal/command prompt** and run:

**Linux/macOS:**
```bash
streamlit run agent/dashboard.py
```

**Windows:**
```powershell
streamlit run agent/dashboard.py
```

**What you'll see:** A web browser will open automatically showing:
- 🛡️ Real-time threat timeline visualization
- 📊 Attack distribution charts
- 📈 Live security metrics
- 🔴 Color-coded threat severity indicators

The dashboard automatically reads threat data from the agent and updates every 2 seconds.

> **💡 Tip:** On Windows, if the browser doesn't open automatically, manually visit `http://localhost:8501`

> **💡 Tip:** On Windows, if the browser doesn't open automatically, manually visit `http://localhost:8501`

---

###  What This Demo Shows

This prototype demonstrates the **full SecureGuard AI architecture** without requiring AWS:

1. **Local ML Agent** (`demo.py`) - Simulates the network sensor that would run on a user's machine
2. **Cloud Database** (`dashboard_data.json`) - Simulates AWS DynamoDB storage
3. **Visual Interface** (`streamlit dashboard`) - Simulates the cloud-hosted web dashboard

**In production:** The agent would capture real network traffic, the cloud database would be AWS DynamoDB, and the dashboard would be hosted on AWS with Bedrock AI providing natural language explanations.

---

## Project Mission:

Turn cybersecurity from a, expert field gated by knowledge into a AI guided tool accessible to everyone prioritizing user autonomy and giving security back into the hands of the user 

---
### Whets unique about this project?:

We developed this project in response to growing user concerns about data security and the lack of transparency in modern cloud services seen in  issues like unprompted OneDrive syncing or loss of local file control. To address this, we built a privacy first project where all sensitive traffic analysis occurs locally on the user's network; only  threat patterns are ever processed in the cloud. The system functions as an  cyber defense tool that uses machine learning to analyze network behavior, predicting and stoping threats before they become problems for the user. 
---

##  System Architecture

### Current Demo Architecture:

```
┌────────────────────────────────────────────────────────────┐
│                    LOCAL MACHINE                           │
│                                                            │
│  ┌──────────────────────────────────────────────────┐      │
│  │         Network Traffic Simulator (demo.py)      │      │
│  │  - Generates fake network packets                │      │
│  │  - Simulates normal & malicious traffic          │      │
│  └──────────────────────────────────────────────────┘      │
│                         ↓                                  │
│  ┌──────────────────────────────────────────────────┐      │
│  │      ML Anomaly Detector (anomaly_detector.py)   │      │
│  │  - Isolation Forest algorithm                    │      │
│  │  - Detects: Port Scans, DDoS, Unusual Ports      │      │
│  └──────────────────────────────────────────────────┘      │
│                         ↓                                  │
│  ┌──────────────────────────────────────────────────┐      │
│  │    "Cloud" Uploader (cloud_uploader.py)          │      │
│  │  - Writes to dashboard_data.json (Simulates AWS) │      │
│  └──────────────────────────────────────────────────┘      │
│                         ↓                                  │
│  ┌──────────────────────────────────────────────────┐      │
│  │       Visual Dashboard (dashboard.py)            │      │
│  │  - Streamlit web interface                       │      │
│  │  - Timeline visualization                        │      │
│  │  - Real-time threat updates                      │      │
│  └──────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────┘
```

### Production Architecture (With AWS):

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
│  │        Secure Agent (Python Desktop App)         │      │
│  └──────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────┘
                            ↓ (Encrypted HTTPS)
┌────────────────────────────────────────────────────────────┐
│                    AWS CLOUD TIER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Lambda Function│→ │  DynamoDB    │  │  Bedrock AI  │      │
│  │  (Processor) │  │  (Storage)   │  │  (Analysis)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                          │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ Web Dashboard│  │  Mobile App  │                        │
│  │ (Streamlit)  │  │  (Future)    │                        │
│  └──────────────┘  └──────────────┘                        │
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

| Service | Purpose | Implementation Status |
|---------|---------|----------------------|
| **AWS Lambda** | Serverless threat processing |  Code ready in `simple_aws/` |
| **DynamoDB** | Threat event storage |  Schema defined |
| **Bedrock AI** | Natural language explanations |  Requires account access |
| **SageMaker** | Custom ML model training |  Future enhancement |
| **API Gateway** | Secure agent-to-cloud communication |  Lambda Function URL alternative ready |

---

##  System Architecture 

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

---

##  Project Files

```
KingHacks---Project/
├── agent/
│   ├── main.py              # Main agent entry point
│   ├── demo.py              # Simulation mode (no admin required)
│   ├── anomaly_detector.py  # ML-based threat detection
│   ├── cloud_uploader.py    # Cloud communication (AWS simulation)
│   ├── network_capture.py   # Real packet capture (requires sudo)
│   ├── dashboard.py         # Streamlit visual dashboard
│   ├── config.yaml          # Configuration settings
│   └── requirements.txt     # Python dependencies
├── simple_aws/
│   ├── deploy.py            # AWS deployment automation
│   └── lambda_function.py   # Lambda backend code
├── dashboard.html           # Static HTML dashboard (alternative)
├── dashboard_data.json      # Simulated cloud database
└── README.md                # This file
```

---

##  Troubleshooting

**Q: Dashboard shows "No threats detected"**
- Make sure `demo.py` is running in another terminal
- Check that `dashboard_data.json` exists in the project root

**Q: Import errors when running demo.py**
- **Linux/macOS:** Run `pip3 install -r agent/requirements.txt`
- **Windows:** Run `pip install -r agent/requirements.txt`
- Then install additional packages: `pip install streamlit pandas plotly` (use `pip3` on Linux/macOS)

**Q: Permission denied errors**
- Use `demo.py` instead of `main.py` (demo doesn't need admin privileges)
- **Linux:** You may need to use `python3` instead of `python`
- **Windows:** Run PowerShell/CMD as Administrator if issues persist

**Q: Dashboard won't open in browser**
- Manually visit: `http://localhost:8501`
- Or check the terminal for the correct port
- **Windows Firewall:** You may need to allow Python through the firewall

**Q: "python/python3 not found"**
- **Linux/macOS:** Use `python3` explicitly
- **Windows:** Make sure you checked "Add Python to PATH" during installation
  - If not, reinstall Python or add it to PATH manually

**Q: Module 'scapy' requires elevated privileges**
- This only affects `main.py` (real packet capture)
- Use `demo.py` instead for the simulation mode (no admin needed)

---

##  License

MIT License - See [LICENSE](LICENSE) for details

---

##  Contributors

Built for KingHacks 2026 by [@JJEA12](https://github.com/JJEA12)

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


