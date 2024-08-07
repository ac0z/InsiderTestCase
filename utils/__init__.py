import logging
from datetime import datetime
import os

def setup_logger():
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = f'test_log_{today}.log'
    
    # Eğer log dosyası yoksa oluştur, varsa mevcut dosyaya ekleme yap
    if not os.path.exists(log_file):
        open(log_file, 'w').close()
    
    logging.basicConfig(filename=log_file, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='a')  # 'a' modu, mevcut dosyaya ekleme yapar
    return logging.getLogger()