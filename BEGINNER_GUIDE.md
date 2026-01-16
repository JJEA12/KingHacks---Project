#  Beginner's Guide to using SecureGuard AI
#### Files:
- **main.py** - Entry point, starts everything
- **network_capture.py** - Captures network packets (like recording traffic)
- **anomaly_detector.py** - Detects suspicious patterns (the AI brain)
- **cloud_uploader.py** - Sends anonymized data to AWS (privacy-first!)
- **gui.py** - Simple interface to interact with the agent

#### workings:
```
Your Network → Capture Packets → Detect Threats → Alert You → Upload to Cloud
```
#### Test it now!

1. **Install dependencies:**
   cd agent
   pip install -r requirements.txt

2. **Run in CLI mode**
   python main.py --cli
   ```

3. **See statistics:**
   Type `stats` and press Enter

4. **See alerts:**
   Type `alerts` and press Enter

## Understanding the Code
**1. Threading (network_capture.py)**
```python
# Why? So we can capture packets while doing other things
self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
```
Think of it like multitasking - walking and chewing gum at the same time!

**2. Queue (packet_queue)**
```python
self.packet_queue = Queue(maxsize=10000)
```
A queue is like a line at a store - first in, first out. Keeps packets organized.

**3. Hash Functions (privacy)**
```python
hashlib.sha256(ip_address.encode()).hexdigest()[:16]
```
Hashing turns "192.168.1.1" into "a3f5b2c9" - can't reverse it back. Privacy!

**4. Machine Learning (Isolation Forest)**
```python
IsolationForest(contamination=0.1)
```



## Troubleshooting

### "Permission denied" when capturing packets
# Linux/Mac: Run with sudo
sudo python main.py --cli

# Windows: Run terminal as Administrator

### "Module not found" errors
cd agent

# Reinstall dependencies
pip install -r requirements.txt


### "AWS credentials not found"
 We'll set these up in Step 2

## Project Structure

```
KingHacks---Project/
├── agent/                  # ✅ DONE - Local Python app
│   ├── main.py
│   ├── network_capture.py
│   ├── anomaly_detector.py
│   ├── cloud_uploader.py
│   ├── gui.py
│   ├── requirements.txt
│   └── config.yaml
├── infrastructure/         # 🔄 TODO - AWS CDK code
├── lambda-functions/       # 🔄 TODO - Cloud functions
├── dashboard/              # 🔄 TODO - React website
├── ml-models/              # 🔄 TODO - ML training scripts
└── README.md
```