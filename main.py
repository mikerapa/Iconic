from model.log_handler import get_logger

logger = get_logger(__name__)

def main():
    logger.debug("Iconic started")
    print("Hello from iconic!")

if __name__ == "__main__":
    main()
