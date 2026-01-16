"""
Anomaly Detection Module
Detects suspicious network activity using machine learning.
"""

import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from loguru import logger
from sklearn.ensemble import IsolationForest
import numpy as np


class AnomalyDetector:
    """Detects network anomalies using ML algorithms"""
    
    def __init__(self, config):
        self.config = config
        self.is_running = False
        self.detection_thread = None
        
        # Baseline tracking
        self.baseline_duration = timedelta(hours=config.get('baseline_duration_hours', 24))
        self.packet_history = deque(maxlen=10000)
        self.baseline_established = False
        
        # Anomaly detection models
        self.models = {}
        if 'isolation_forest' in config.get('algorithms', []):
            self.models['isolation_forest'] = IsolationForest(
                contamination=0.1,
                random_state=42
            )
        
        # Threat detection patterns
        self.threat_patterns = {
            'port_scan': self._detect_port_scan,
            'ddos': self._detect_ddos,
            'unusual_port': self._detect_unusual_port
        }
        
        # Connection tracking
        self.connections = defaultdict(lambda: {'count': 0, 'ports': set(), 'last_seen': None})
        self.alerts = []
        
    def start(self):
        """Start anomaly detection in background"""
        if self.is_running:
            return
            
        self.is_running = True
        self.detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.detection_thread.start()
        logger.info("Anomaly detector started")
        
    def stop(self):
        """Stop anomaly detection"""
        self.is_running = False
        if self.detection_thread:
            self.detection_thread.join(timeout=5)
        logger.info("Anomaly detector stopped")
        
    def analyze_packet(self, packet_data):
        """Analyze a single packet for anomalies"""
        if not packet_data:
            return None
            
        # Add to history
        self.packet_history.append({
            **packet_data,
            'analyzed_at': datetime.now()
        })
        
        # Update connection tracking
        if 'src_ip_hash' in packet_data and 'dst_port' in packet_data:
            src = packet_data['src_ip_hash']
            self.connections[src]['count'] += 1
            self.connections[src]['ports'].add(packet_data['dst_port'])
            self.connections[src]['last_seen'] = datetime.now()
        
        # Run threat detection patterns
        threats = []
        for threat_name, detector_func in self.threat_patterns.items():
            if detector_func(packet_data):
                threat = {
                    'type': threat_name,
                    'timestamp': datetime.now().isoformat(),
                    'packet': packet_data,
                    'severity': self._get_severity(threat_name)
                }
                threats.append(threat)
                logger.warning(f"🚨 Threat detected: {threat_name}")
                
        return threats if threats else None
        
    def _detection_loop(self):
        """Background loop for batch analysis"""
        while self.is_running:
            try:
                # Clean up old connections
                self._cleanup_old_connections()
                
                # Check for patterns over time
                self._check_temporal_patterns()
                
                time.sleep(5)  # Check every 5 seconds
            except Exception as e:
                logger.error(f"Detection loop error: {e}")
                
    def _detect_port_scan(self, packet_data):
        """Detect potential port scanning activity"""
        if 'src_ip_hash' not in packet_data:
            return False
            
        src = packet_data['src_ip_hash']
        conn = self.connections[src]
        
        # Port scan: many different ports from same source in short time
        if len(conn['ports']) > 20:  # More than 20 different ports
            return True
        return False
        
    def _detect_ddos(self, packet_data):
        """Detect potential DDoS activity"""
        # Count packets to same destination in last minute
        recent_packets = [
            p for p in self.packet_history
            if datetime.now() - p['analyzed_at'] < timedelta(minutes=1)
        ]
        
        if 'dst_ip_hash' in packet_data:
            dst = packet_data['dst_ip_hash']
            dst_count = sum(1 for p in recent_packets if p.get('dst_ip_hash') == dst)
            
            # More than 1000 packets to same destination in 1 minute
            if dst_count > 1000:
                return True
        return False
        
    def _detect_unusual_port(self, packet_data):
        """Detect connections to unusual ports"""
        if 'dst_port' not in packet_data:
            return False
            
        # List of unusual/suspicious ports
        suspicious_ports = {
            31337, 12345, 54321,  # Common backdoor ports
            6666, 6667, 6668, 6669,  # IRC (can be used for botnets)
            1234, 4321, 5555  # Common malware ports
        }
        
        return packet_data['dst_port'] in suspicious_ports
        
    def _cleanup_old_connections(self):
        """Remove old connection tracking data"""
        cutoff = datetime.now() - timedelta(minutes=5)
        to_remove = [
            ip for ip, data in self.connections.items()
            if data['last_seen'] and data['last_seen'] < cutoff
        ]
        for ip in to_remove:
            del self.connections[ip]
            
    def _check_temporal_patterns(self):
        """Check for patterns over time (batch analysis)"""
        # This would be where ML model inference happens
        # For now, just logging
        if len(self.packet_history) > 100:
            logger.debug(f"Analyzing {len(self.packet_history)} packets for patterns")
            
    def _get_severity(self, threat_type):
        """Get severity level for threat type"""
        severity_map = {
            'port_scan': 'MEDIUM',
            'ddos': 'CRITICAL',
            'unusual_port': 'HIGH'
        }
        return severity_map.get(threat_type, 'LOW')
        
    def get_alerts(self):
        """Get recent alerts"""
        return self.alerts.copy()
        
    def get_stats(self):
        """Get detection statistics"""
        return {
            'packets_analyzed': len(self.packet_history),
            'active_connections': len(self.connections),
            'alerts_count': len(self.alerts),
            'baseline_established': self.baseline_established
        }
