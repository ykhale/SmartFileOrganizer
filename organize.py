#!/usr/bin/env python3

import os
import shutil
import argparse
from datetime import datetime
import logging

# Configure logging
LOG_FILE = os.path.expanduser('~/SmartFileOrganizer/logs/organize.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define file type categories
FILE_CATEGORIES = {
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.md'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv'],
    'Music': ['.mp3', '.wav', '.flac'],
    'Archives': ['.zip', '.tar', '.gz', '.rar'],
    'Scripts': ['.sh', '.py', '.js', '.rb'],
    'Others': []
}

def get_category(file_extension):
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category
    return 'Others'

def organize_files(target_dir, by_date=False):
    if not os.path.isdir(target_dir):
        logging.error(f"Directory does not exist: {target_dir}")
        print(f"Error: Directory does not exist: {target_dir}")
        return

    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)

        if os.path.isfile(item_path):
            file_ext = os.path.splitext(item)[1]
            category = get_category(file_ext)

            if by_date:
                creation_time = os.path.getctime(item_path)
                date_folder = datetime.fromtimestamp(creation_time).strftime('%Y/%m-%B')
                dest_dir = os.path.join(target_dir, category, date_folder)
            else:
                dest_dir = os.path.join(target_dir, category)

            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, item)

            try:
                shutil.move(item_path, dest_path)
                logging.info(f"Moved '{item}' to '{dest_dir}'")
                print(f"Moved '{item}' to '{dest_dir}'")
            except Exception as e:
                logging.error(f"Failed to move '{item}': {e}")
                print(f"Error: Failed to move '{item}': {e}")

def main():
    parser = argparse.ArgumentParser(description='Smart File Organizer')
    parser.add_argument('target_dir', help='Directory to organize')
    parser.add_argument('--by-date', action='store_true', help='Organize files by creation date')
    args = parser.parse_args()

    organize_files(args.target_dir, by_date=args.by_date)

if __name__ == "__main__":
    main()

