"""
SecureGuard AI - Local Network Security Agent
This is the main entry point for the desktop application.
"""

import sys
import yaml
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

# Import our modules (we'll create these next)
from network_capture import NetworkCapture
from anomaly_detector import AnomalyDetector
from cloud_uploader import CloudUploader
from gui import SecureGuardGUI

# Load environment variables
load_dotenv()

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logger.add(
    "logs/agent.log",
    rotation="50 MB",
    retention="7 days",
    level="INFO"
)


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Main application entry point"""
    logger.info("Starting SecureGuard AI Agent...")
    
    try:
        # Load configuration
        config = load_config()
        logger.info(f"Configuration loaded from config.yaml")
        
        # Initialize components
        network_capture = NetworkCapture(config['network'])
        anomaly_detector = AnomalyDetector(config['detection'])
        cloud_uploader = CloudUploader(config['aws'])
        
        # Start GUI (or CLI mode)
        if '--cli' in sys.argv:
            logger.info("Running in CLI mode")
            # Start background services
            network_capture.start()
            anomaly_detector.start()
            cloud_uploader.start()
            
            # Keep running
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Shutting down...")
        else:
            logger.info("Launching GUI...")
            app = SecureGuardGUI(
                network_capture,
                anomaly_detector,
                cloud_uploader
            )
            app.run()
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
