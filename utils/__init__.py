import logging
from datetime import datetime
import os

def setup_logger():
    today = datetime.now().strftime('%Y-%m-%d')
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Logs')
    
    # Create Logs directory if it doesn't exist
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_file = os.path.join(logs_dir, f'test_log_{today}.log')
    
    # Create log file if it doesn't exist, otherwise append to the existing file
    if not os.path.exists(log_file):
        open(log_file, 'w').close()
    
    logging.basicConfig(filename=log_file, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='a')  # 'a' mode appends to the existing file
    return logging.getLogger()
