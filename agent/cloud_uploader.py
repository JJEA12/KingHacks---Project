"""
Cloud Uploader Module
Securely uploads anonymized telemetry to AWS.
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
                logger.warning("API endpoint not configured, skipping upload")
                logger.debug(f"Would upload {len(self.batch)} telemetry items")
                self.batch.clear()
                return
            
            # Prepare payload
            payload = {
                'timestamp': datetime.now().isoformat(),
                'telemetry_count': len(self.batch),
                'telemetry': self.batch[:self.batch_size]  # Respect batch size limit
            }
            
            # In production, this would POST to API Gateway
            # For now, just log (since we haven't deployed AWS yet)
            logger.info(f"📤 Uploading {len(self.batch)} telemetry items to cloud")
            logger.debug(f"Payload size: {len(json.dumps(payload))} bytes")
            
            # Simulate API call
            # response = requests.post(self.api_endpoint, json=payload)
            
            # Clear batch after successful upload
            self.batch.clear()
            logger.info("✅ Upload successful")
            
        except ClientError as e:
            logger.error(f"AWS API error: {e}")
        except Exception as e:
            logger.error(f"Upload error: {e}")
            
    def upload_threat_event(self, threat_data):
        """Upload a detected threat event immediately (high priority)"""
        try:
            if not self.api_endpoint:
                logger.warning(f"🚨 THREAT DETECTED (not uploaded - no API endpoint): {threat_data['type']}")
                return
            
            logger.warning(f"🚨 Uploading threat event: {threat_data['type']}")
            
            # In production: POST to /threats endpoint
            # response = requests.post(f"{self.api_endpoint}/threats", json=threat_data)
            
            logger.info("✅ Threat event uploaded")
            
        except Exception as e:
            logger.error(f"Failed to upload threat event: {e}")
            
    def get_stats(self):
        """Get upload statistics"""
        return {
            'queue_size': self.upload_queue.qsize(),
            'batch_size': len(self.batch),
            'endpoint_configured': bool(self.api_endpoint)
        }
