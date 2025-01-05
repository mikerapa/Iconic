from logging import getLogger, Formatter, DEBUG
from logging.handlers import RotatingFileHandler
import os
import sys

class NewestFirstRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, maxBytes=0, backupCount=0):
        super().__init__(filename, maxBytes=maxBytes, backupCount=backupCount)
        # Create the file if it doesn't exist
        if not os.path.exists(filename):
            open(filename, 'wb').close()
    
    def emit(self, record):
        try:
            # Close the current stream if it exists
            if self.stream:
                self.stream.close()
                self.stream = None
            
            # Read existing content
            with open(self.baseFilename, 'rb') as f:
                content = f.read()
            
            # Write new content
            with open(self.baseFilename, 'wb') as f:
                msg = self.format(record) + '\n'
                f.write(msg.encode())
                f.write(content)
            
        except Exception:
            self.handleError(record)

def get_logger(name):
    logger = getLogger(name)
    
    # Only add handler if it hasn't been added before
    if not logger.handlers:
        logger.setLevel(DEBUG)
        
        # Determine if we're running tests
        is_test = 'pytest' in sys.modules or 'unittest' in sys.modules
        log_file = 'test.log' if is_test else 'iconic.log'
        
        handler = NewestFirstRotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
        handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
    
    return logger 
