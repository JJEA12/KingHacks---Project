#!/usr/bin/env python3
"""
SecureGuard AI - DEMO MODE
Runs without admin privileges by simulating network traffic instead of capturing real packets.
Perfect for testing and demonstrations!
"""

import sys
import time
import random
from pathlib import Path
from datetime import datetime
from loguru import logger

# Add agent directory to path
sys.path.insert(0, str(Path(__file__).parent / 'agent'))

from anomaly_detector import AnomalyDetector
from cloud_uploader import CloudUploader
import yaml

# Configure logging
logger.remove()  # Remove default handler
logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")

print("\n" + "="*70)
print("🛡️  SECUREGUARD AI - DEMO MODE")
print("="*70)
print("Running in SIMULATION mode (no admin privileges required)")
print("Generating realistic network traffic patterns...\n")

# Load config
config_path = Path(__file__).parent / 'agent' / 'config.yaml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Initialize components
anomaly_detector = AnomalyDetector(config['detection'])
cloud_uploader = CloudUploader(config['aws'])

# Start services
anomaly_detector.start()
cloud_uploader.start()

# Simulation data
normal_ports = [80, 443, 22, 25, 53, 3306, 5432, 8080]
suspicious_ports = [31337, 12345, 6666, 4444, 1234]
protocols = ['TCP', 'UDP', 'ICMP']

def generate_packet(is_threat=False):
    """Generate simulated network packet"""
    if is_threat:
        # Generate suspicious traffic
        threat_type = random.choice(['port_scan', 'suspicious_port', 'ddos'])
        
        if threat_type == 'port_scan':
            # Same source, many different ports
            return {
                'timestamp': datetime.now().isoformat(),
                'protocol': 'TCP',
                'src_ip_hash': 'attacker_001',
                'dst_ip_hash': f'target_{random.randint(1,5):03d}',
                'src_port': random.randint(1024, 65535),
                'dst_port': random.randint(1, 1000),  # Scanning low ports
                'packet_size': random.randint(40, 100),
                'flags': 'S'  # SYN flag (port scan)
            }
        elif threat_type == 'suspicious_port':
            return {
                'timestamp': datetime.now().isoformat(),
                'protocol': 'TCP',
                'src_ip_hash': f'suspicious_{random.randint(1,10):03d}',
                'dst_ip_hash': f'internal_{random.randint(1,5):03d}',
                'src_port': random.randint(1024, 65535),
                'dst_port': random.choice(suspicious_ports),
                'packet_size': random.randint(100, 1500),
                'flags': 'SA'
            }
        else:  # ddos
            # Many packets to same destination
            return {
                'timestamp': datetime.now().isoformat(),
                'protocol': random.choice(['TCP', 'UDP']),
                'src_ip_hash': f'botnet_{random.randint(1,100):03d}',
                'dst_ip_hash': 'victim_server',
                'src_port': random.randint(1024, 65535),
                'dst_port': 80,
                'packet_size': random.randint(40, 100),
                'flags': 'S'
            }
    else:
        # Generate normal traffic
        return {
            'timestamp': datetime.now().isoformat(),
            'protocol': random.choice(protocols),
            'src_ip_hash': f'client_{random.randint(1,20):03d}',
            'dst_ip_hash': f'server_{random.randint(1,10):03d}',
            'src_port': random.randint(1024, 65535),
            'dst_port': random.choice(normal_ports),
            'packet_size': random.randint(40, 1500),
            'flags': random.choice(['S', 'SA', 'A', 'PA'])
        }

# Statistics
stats = {
    'total_packets': 0,
    'threats_detected': 0,
    'start_time': time.time()
}

try:
    logger.info(" Starting network simulation")
    logger.info("Press Ctrl+C to stop and view statistics\n")
    
    while True:
        # Generate mostly normal traffic with occasional threats
        is_threat = random.random() < 0.05  # 5% chance of threat
        
        packet = generate_packet(is_threat)
        stats['total_packets'] += 1
        
        # Analyze packet
        threats = anomaly_detector.analyze_packet(packet)
        
        # Queue for cloud upload
        cloud_uploader.queue_telemetry(packet)
        
        # Display interesting events
        if threats:
            stats['threats_detected'] += 1
            for threat in threats:
                logger.warning(f" THREAT DETECTED: {threat['type'].upper()} (Severity: {threat['severity']})")
                cloud_uploader.upload_threat_event(threat)
        elif stats['total_packets'] % 100 == 0:
            # Show progress every 100 packets
            logger.info(f"📊 Processed {stats['total_packets']} packets | Threats: {stats['threats_detected']}")
        
        # Simulate real-time traffic (10-50 packets per second)
        time.sleep(random.uniform(0.02, 0.1))
        
except KeyboardInterrupt:
    print("\n\n Stopping simulation...")
    
    # Stop services
    anomaly_detector.stop()
    cloud_uploader.stop()
    
    # Calculate runtime
    runtime = time.time() - stats['start_time']
    
    # Display final statistics
    print("\n" + "="*70)
    print(" FINAL STATISTICS")
    print("="*70)
    
    print(f"\n  Runtime: {runtime:.1f} seconds")
    print(f" Total Packets Processed: {stats['total_packets']}")
    print(f" Threats Detected: {stats['threats_detected']}")
    print(f" Packets/Second: {stats['total_packets']/runtime:.1f}")
    
    # Component statistics
    detector_stats = anomaly_detector.get_stats()
    uploader_stats = cloud_uploader.get_stats()
    
    print(f"\n Anomaly Detector:")
    print(f"   - Packets analyzed: {detector_stats['packets_analyzed']}")
    print(f"   - Active connections tracked: {detector_stats['active_connections']}")
    print(f"   - Total alerts: {detector_stats['alerts_count']}")
    
    print(f"\n  Cloud Uploader:")
    print(f"   - Queue size: {uploader_stats['queue_size']}")
    print(f"   - Pending batch: {uploader_stats['batch_size']}")
    print(f"   - API configured: {uploader_stats['endpoint_configured']}")
    
    print("\n" + "="*70)
    print(" Demo completed successfully!")
    print("="*70)
    print("\n Next Steps:")
    print("   1. Configure AWS credentials in .env to enable cloud features")
    print("   2. Deploy AWS infrastructure: cd infrastructure && npm install && cdk deploy")
    print("   3. Run with real packet capture: sudo python3 agent/main.py --cli")
    print("\n")
