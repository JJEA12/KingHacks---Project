"""
Network Capture Module
Captures network packets using scapy and processes them for analysis.
"""

import hashlib
import threading
from queue import Queue
from datetime import datetime
from loguru import logger
from scapy.all import sniff, IP, TCP, UDP, ICMP


class NetworkCapture:
    """Captures and processes network packets"""
    
    def __init__(self, config):
        self.config = config
        self.packet_queue = Queue(maxsize=config.get('buffer_size', 10000))
        self.is_running = False
        self.capture_thread = None
        self.stats = {
            'total_packets': 0,
            'tcp_packets': 0,
            'udp_packets': 0,
            'icmp_packets': 0,
            'other_packets': 0
        }
        
    def start(self):
        """Start packet capture in background thread"""
        if self.is_running:
            logger.warning("Network capture already running")
            return
            
        self.is_running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        logger.info("Network capture started")
        
    def stop(self):
        """Stop packet capture"""
        self.is_running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=5)
        logger.info("Network capture stopped")
        
    def _capture_loop(self):
        """Main packet capture loop"""
        try:
            # Get network interface
            interface = self.config.get('interface', 'auto')
            if interface == 'auto':
                interface = None  # Let scapy auto-detect
                
            # Start sniffing
            logger.info(f"Starting packet capture on interface: {interface or 'auto'}")
            sniff(
                iface=interface,
                prn=self._process_packet,
                store=False,
                stop_filter=lambda _: not self.is_running,
                filter=self.config.get('capture_filter', 'tcp or udp')
            )
        except PermissionError:
            logger.error("⚠️  Permission denied! Run with sudo/admin privileges to capture packets.")
        except Exception as e:
            logger.error(f"Capture error: {e}")
            
    def _process_packet(self, packet):
        """Process a single captured packet"""
        try:
            # Extract basic info
            if IP in packet:
                packet_data = self._extract_packet_info(packet)
                
                # Update statistics
                self.stats['total_packets'] += 1
                if TCP in packet:
                    self.stats['tcp_packets'] += 1
                elif UDP in packet:
                    self.stats['udp_packets'] += 1
                elif ICMP in packet:
                    self.stats['icmp_packets'] += 1
                else:
                    self.stats['other_packets'] += 1
                
                # Add to queue for further processing
                if not self.packet_queue.full():
                    self.packet_queue.put(packet_data)
                else:
                    logger.warning("Packet queue full, dropping packet")
                    
        except Exception as e:
            logger.error(f"Packet processing error: {e}")
            
    def _extract_packet_info(self, packet):
        """Extract and anonymize packet information"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'protocol': 'unknown',
            'src_port': None,
            'dst_port': None,
            'packet_size': len(packet),
            'flags': []
        }
        
        # Get IP information (anonymized if configured)
        if IP in packet:
            if self.config.get('privacy', {}).get('hash_ips', True):
                # Hash IPs for privacy
                data['src_ip_hash'] = self._hash_ip(packet[IP].src)
                data['dst_ip_hash'] = self._hash_ip(packet[IP].dst)
            else:
                data['src_ip'] = packet[IP].src
                data['dst_ip'] = packet[IP].dst
        
        # Get protocol-specific information
        if TCP in packet:
            data['protocol'] = 'TCP'
            data['src_port'] = packet[TCP].sport
            data['dst_port'] = packet[TCP].dport
            data['flags'] = str(packet[TCP].flags)
        elif UDP in packet:
            data['protocol'] = 'UDP'
            data['src_port'] = packet[UDP].sport
            data['dst_port'] = packet[UDP].dport
        elif ICMP in packet:
            data['protocol'] = 'ICMP'
            data['icmp_type'] = packet[ICMP].type
            
        return data
    
    @staticmethod
    def _hash_ip(ip_address):
        """Hash IP address for privacy"""
        return hashlib.sha256(ip_address.encode()).hexdigest()[:16]
    
    def get_packet(self, timeout=1):
        """Get next packet from queue"""
        try:
            return self.packet_queue.get(timeout=timeout)
        except:
            return None
            
    def get_stats(self):
        """Get capture statistics"""
        return self.stats.copy()
