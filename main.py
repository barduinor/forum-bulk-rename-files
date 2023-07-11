"""main.py"""

import logging
from app.config import AppConfig

from app.box_client import get_client
from original_method import rename_file
from sample_folders import check_sample_folders

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)

conf = AppConfig()

SAMPLES_DIR = "samples"


def main():
    """
    Simple script to demonstrate how to use the Box SDK
    with oAuth2 authentication
    """

    check_sample_folders(SAMPLES_DIR)

    client = get_client(conf)

    # samples folder ID
    root_items = client.folder("0").get_items()
    samples_folders = [
        root_item.id for root_item in root_items if root_item.name == "samples"
    ]

    samples_folder = samples_folders[0]

    # get all items in the samples folder
    items = client.folder(samples_folder).get_items()

    for item in items:
        # if file name contain file_, skip it
        if item.name.startswith("file_"):
            continue
        rename_file(client, samples_folder, item, "file.txt")


if __name__ == "__main__":
    main()
