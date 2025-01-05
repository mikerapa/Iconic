from logging import getLogger, Formatter, DEBUG
from logging.handlers import RotatingFileHandler
import os


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

# Configure logging with custom handler
logger = getLogger(__name__)
logger.setLevel(DEBUG)  # Set the logger's level
handler = NewestFirstRotatingFileHandler('iconic.log', maxBytes=1024*1024, backupCount=5)
handler.setFormatter(Formatter('%(asctime)s - Iconic - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def main():
    logger.debug("Iconic started")
    print("Hello from iconic!")

if __name__ == "__main__":
    main()
