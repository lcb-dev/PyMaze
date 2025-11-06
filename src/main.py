import logging
import argparse
import src.processor as processor
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(
        filename="pymaze.log", 
        format='(%(asctime)s) [%(filename)s:%(funcName)s:%(levelname)s]:: %(message)s', 
        datefmt='%d/%m/%Y %I:%M:%S %p', 
        level=logging.DEBUG)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', type=str, required=True, help="Path to image to process for map.")
    args = parser.parse_args()
    return args

def main():
    logger.info("Script started successfully.")
    logger.info("Loading modules...")
    logger.info("Processor module version: %s", processor.__version__)

    logger.info("Loading CLI args...")
    cli_args = parse_args()
    map_image_file = Path(cli_args.img)
    process_image(map_image_file)
    logger.info("Shutting down.\n\n")

def process_image(imageFile: Path):
    if imageFile.exists():
        logger.info("Image file found!")
        bitmap, (w, h), bitmap_image_file = processor.image_reader.read_image(imageFile, grid_size=(1920, 1920))
        print(f"Result size: W={w}, H={h}")
        bitmap_image_file.save("maze_bitmap.bmp")
        logger.info("Image saved. 'maze_bitmap.bmp'")

        entrances = processor.maze_utils.find_entrances(bitmap)
        print(f"Entrances found: {entrances}")
        
    else:
        logger.error("File not found!")
    

if __name__ == '__main__':
    main()