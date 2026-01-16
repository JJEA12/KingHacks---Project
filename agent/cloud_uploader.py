"""
Cloud Uploader Module
uploads anonymized data to AWS.
"""

import os
import json
import time
import threading
from datetime import datetime
from queue import Queue
from loguru import logger
import boto3
from botocore.exceptions import ClientError


class CloudUploader:
    """Handles secure upload of telemetry data to AWS"""
    
    def __init__(self, config):
        self.config = config
        self.upload_queue = Queue()
        self.is_running = False
        self.upload_thread = None
        
        # Initialize AWS clients
        self.region = config.get('region', 'us-east-1')
        self.api_endpoint = os.getenv('API_GATEWAY_URL', config.get('api_endpoint', ''))
        
        # Batch settings
        self.batch_size = config.get('batch_size', 100)
        self.upload_interval = config.get('upload_interval_seconds', 60)
        self.batch = []
        
        # Initialize boto3 clients if credentials available
        try:
            self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
            self.api_client = boto3.client('apigateway', region_name=self.region)
            logger.info(f"AWS clients initialized for region: {self.region}")
        except Exception as e:
            logger.warning(f"AWS clients not initialized: {e}")
            self.dynamodb = None
            self.api_client = None
            
    def start(self):
        """Start background upload thread"""
        if self.is_running:
            return
            
        self.is_running = True
        self.upload_thread = threading.Thread(target=self._upload_loop, daemon=True)
        self.upload_thread.start()
        logger.info("Cloud uploader started")
        
    def stop(self):
        """Stop upload thread and flush remaining data"""
        self.is_running = False
        if self.batch:
            self._upload_batch()
        if self.upload_thread:
            self.upload_thread.join(timeout=5)
        logger.info("Cloud uploader stopped")
        
    def queue_telemetry(self, data):
        """Add telemetry data to upload queue"""
        self.upload_queue.put(data)
        
    def _upload_loop(self):
        """Background loop for batching and uploading"""
        last_upload = time.time()
        
        while self.is_running:
            try:
                # Get data from queue
                try:
                    data = self.upload_queue.get(timeout=1)
                    self.batch.append(data)
                except:
                    pass  # Queue empty, continue
                
                # Upload if batch is full or interval elapsed
                current_time = time.time()
                if len(self.batch) >= self.batch_size or \
                   (self.batch and (current_time - last_upload) >= self.upload_interval):
                    self._upload_batch()
                    last_upload = current_time
                    
            except Exception as e:
                logger.error(f"Upload loop error: {e}")
                
    def _upload_batch(self):
        """Upload current batch to cloud"""
        if not self.batch:
            return
            
        try:
            # Check if API endpoint is configured
            if not self.api_endpoint:
                # FREE TIER / DEMO MODE: Write to local JSON file to update Dashboard
                # This file acts as our "Cloud Database" for the demo
                db_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard_data.json')
                
                # Create default structure if not exists
                if not os.path.exists(db_path):
                    with open(db_path, 'w') as f:
                        json.dump({'threats': [], 'stats': {'packets': 0}}, f)

                # Prepare payload (Simulating what we WOULD send to AWS Lambda)
                payload = {
                    'timestamp': datetime.now().isoformat(),
                    'telemetry_count': len(self.batch),
                    'telemetry': self.batch[:self.batch_size]
                }
                
                # Read current DB
                try:
                    with open(db_path, 'r') as f:
                        db = json.load(f)
                except:
                    db = {'threats': [], 'stats': {'packets': 0}}
                
                # Update Stats "In the Cloud"
                db['stats']['packets'] = db.get('stats', {}).get('packets', 0) + len(self.batch)
                
                # Save just the threats to the "Cloud DB"
                for item in self.batch:
                    if item.get('is_threat') or item.get('anomaly_score', 0) > 0.5:
                         # Cap list size to 20 for simple display
                        db['threats'].insert(0, item)
                        db['threats'] = db['threats'][:20]

                # Write back
                with open(db_path, 'w') as f:
                    json.dump(db, f, indent=2)

                logger.info(f"[AWS SIMULATION] Uploaded {len(self.batch)} items to Simulated Cloud DB (dashboard_data.json)")
                self.batch.clear()
                return

            # Real upload logic (if configured later)
            # ...

            
            # Prepare payload
            payload = {
                'timestamp': datetime.now().isoformat(),
                'telemetry_count': len(self.batch),
                'telemetry': self.batch[:self.batch_size]  # Respect batch size limit
            }
            
            # Send to API Gateway or Lambda Function URL
            import requests
            
            # If using Lambda Function URL, use it directly. If using API Gateway, append endpoint.
            url = self.api_endpoint
            if url and 'lambda-url' not in url and not url.endswith('/analyze'):
                 url = f"{url}/analyze"

            if url:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=30,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    logger.info(f"Successfully uploaded {len(self.batch)} telemetry items")
                    self.batch.clear()
                else:
                    logger.error(f"Upload failed: {response.status_code} - {response.text}")
            else:
                logger.info(f"[SIMULATION] Would upload {len(self.batch)} items (No URL configured)")
                self.batch.clear()
            
        except ClientError as e:
            logger.error(f"AWS API error: {e}")
        except Exception as e:
            logger.error(f"Upload error: {e}")
            
    def upload_threat_event(self, threat_data):
        """Upload a detected threat event immediately (high priority)"""
        try:
            # Prepare payload
            payload = threat_data
            timestamp = datetime.now().isoformat()
            
            if not self.api_endpoint:
                # FREE TIER: Save to local "Cloud DB"
                logger.warning(f"[AWS SIMULATION] THREAT DETECTED: {threat_data['type']} - Uploading to Cloud DB...")
                
                db_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard_data.json')
                
                # Load DB
                try:
                    with open(db_path, 'r') as f:
                        db = json.load(f)
                except:
                    db = {'threats': [], 'stats': {'packets': 0}}
                
                # Add threat
                threat_data['timestamp'] = timestamp
                db['threats'].insert(0, threat_data) # Add to top
                db['threats'] = db['threats'][:30]   # Keep last 30
                
                # Save DB
                with open(db_path, 'w') as f:
                    json.dump(db, f, indent=2)
                    
                return
            
            logger.warning(f"Uploading threat event: {threat_data['type']}")
            
            # Prepare threat payload properly wrapped
            payload = {
                'timestamp': datetime.now().isoformat(),
                'is_threat': True,
                'telemetry': [threat_data]
            }

            url = self.api_endpoint
            if 'lambda-url' not in url and not url.endswith('/threats'):
                 url = f"{url}/threats" # Or just use the main endpoint if it's a Function URL
            
            # For Function URL simple backend, we use the same endpoint for everything
            if 'lambda-url' in self.api_endpoint:
                url = self.api_endpoint

            import requests
            requests.post(url, json=payload, timeout=10)
            
            logger.info("Threat event uploaded")
            
        except Exception as e:
            logger.error(f"Failed to upload threat event: {e}")
            
    def get_stats(self):
        """Get upload statistics"""
        return {
            'queue_size': self.upload_queue.qsize(),
            'batch_size': len(self.batch),
            'endpoint_configured': bool(self.api_endpoint)
        }
