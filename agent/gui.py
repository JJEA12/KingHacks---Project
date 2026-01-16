"""
Simple GUI for SecureGuard AI Agent
This is a basic GUI - you can enhance it with PyQt6 for a better desktop app.
"""

import sys
import time
import threading
from loguru import logger


class SecureGuardGUI:
    """Simple text-based GUI (console interface) for the agent"""
    
    def __init__(self, network_capture, anomaly_detector, cloud_uploader):
        self.network_capture = network_capture
        self.anomaly_detector = anomaly_detector
        self.cloud_uploader = cloud_uploader
        self.is_running = False
        
    def run(self):
        """Run the GUI application"""
        self.is_running = True
        
        # Start background services
        self.network_capture.start()
        self.anomaly_detector.start()
        self.cloud_uploader.start()
        
        # Start packet processing thread
        processing_thread = threading.Thread(target=self._process_packets, daemon=True)
        processing_thread.start()
        
        # Display menu and handle user input
        self._display_menu()
        
    def _process_packets(self):
        """Process packets from capture queue"""
        while self.is_running:
            packet = self.network_capture.get_packet(timeout=1)
            if packet:
                # Analyze for anomalies
                threats = self.anomaly_detector.analyze_packet(packet)
                
                # Queue for cloud upload
                self.cloud_uploader.queue_telemetry(packet)
                
                # Upload threats immediately
                if threats:
                    for threat in threats:
                        self.cloud_uploader.upload_threat_event(threat)
                        
    def _display_menu(self):
        """Display console menu and handle commands"""
        print("\n" + "="*60)
        print("🛡️  SECUREGUARD AI - Network Security Agent")
        print("="*60)
        print("\nAgent Status: RUNNING ✅")
        print("\nCommands:")
        print("  stats  - Show statistics")
        print("  alerts - Show recent alerts")
        print("  help   - Show this menu")
        print("  quit   - Stop agent and exit")
        print("\nType a command and press Enter:")
        print("="*60 + "\n")
        
        try:
            while self.is_running:
                command = input("> ").strip().lower()
                
                if command == 'stats':
                    self._show_stats()
                elif command == 'alerts':
                    self._show_alerts()
                elif command == 'help':
                    self._display_menu()
                elif command == 'quit':
                    print("\n🛑 Shutting down SecureGuard AI...")
                    self._shutdown()
                    break
                else:
                    print(f"Unknown command: {command}. Type 'help' for commands.")
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Interrupted. Shutting down...")
            self._shutdown()
            
    def _show_stats(self):
        """Display current statistics"""
        capture_stats = self.network_capture.get_stats()
        detector_stats = self.anomaly_detector.get_stats()
        uploader_stats = self.cloud_uploader.get_stats()
        
        print("\n" + "="*60)
        print("📊 STATISTICS")
        print("="*60)
        print(f"\n📡 Network Capture:")
        print(f"  Total packets: {capture_stats['total_packets']}")
        print(f"  TCP: {capture_stats['tcp_packets']}")
        print(f"  UDP: {capture_stats['udp_packets']}")
        print(f"  ICMP: {capture_stats['icmp_packets']}")
        
        print(f"\n🔍 Anomaly Detection:")
        print(f"  Packets analyzed: {detector_stats['packets_analyzed']}")
        print(f"  Active connections: {detector_stats['active_connections']}")
        print(f"  Alerts generated: {detector_stats['alerts_count']}")
        
        print(f"\n☁️  Cloud Upload:")
        print(f"  Queue size: {uploader_stats['queue_size']}")
        print(f"  Batch size: {uploader_stats['batch_size']}")
        print(f"  Endpoint configured: {uploader_stats['endpoint_configured']}")
        print("="*60 + "\n")
        
    def _show_alerts(self):
        """Display recent alerts"""
        alerts = self.anomaly_detector.get_alerts()
        
        print("\n" + "="*60)
        print("🚨 RECENT ALERTS")
        print("="*60)
        
        if not alerts:
            print("\nNo alerts detected yet. Your network appears secure! ✅")
        else:
            for i, alert in enumerate(alerts[-10:], 1):  # Show last 10
                print(f"\n{i}. {alert['type'].upper()} - {alert['severity']}")
                print(f"   Time: {alert['timestamp']}")
                
        print("="*60 + "\n")
        
    def _shutdown(self):
        """Clean shutdown of all services"""
        self.is_running = False
        self.network_capture.stop()
        self.anomaly_detector.stop()
        self.cloud_uploader.stop()
        logger.info("SecureGuard AI stopped")
        print("✅ Shutdown complete.\n")
        sys.exit(0)
