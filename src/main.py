import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
        filename="pymaze.log", 
        format='(%(asctime)s) [%(filename)s:%(funcName)s:%(levelname)s]:: %(message)s', 
        datefmt='%d/%m/%Y %I:%M:%S %p', 
        level=logging.DEBUG)

def main():
    logger.info("Script started successfully.")
    # TODO: Other logic here... 
    logger.info("Shutting down.")

if __name__ == '__main__':
    main()