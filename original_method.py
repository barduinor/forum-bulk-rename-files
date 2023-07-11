from boxsdk import BoxAPIException, Client
import os
from boxsdk.object.folder import Folder
from boxsdk.object.file import File
from boxsdk.object.item import Item


def rename_file(client: Client, folder_id, file: File, new_name: str):
    # client = box.box_client()

    # Split the new name into base and extension
    base, extension = os.path.splitext(new_name)
    while True:
        try:
            # Get all file names in the current folder
            items = client.folder(folder_id).get_items(limit=None, offset=0)
            existing_names = [
                item.name
                for item in items
                # if isinstance(item, File) and item.id != file.id
                if item.type == "file" and item.id != file.id
            ]

            suffix = 1
            # If the new name already exists, increase the suffix
            while f"{base}_{suffix}{extension}" in existing_names:
                suffix += 1
            name = f"{base}_{suffix}{extension}"

            client.file(file.id).update_info(data={"name": name}, etag=file.etag)
            print(f'File {file.id} {file.name} renamed "{name}" with success.')
            break  # if successful, break the while loop

        except BoxAPIException as e:
            if e.status == 409:  # name conflict
                print(f"File {file.id} with the same name already exists. Retrying...")
                continue  # retry if the name is in use
            if e.status == 412:  # file was modified in the mean time
                print(f"File {file.id} was renamed in the mean time. Skiping...")
                break  # skip if the file was modified
            else:
                raise  # if the error is not due to name conflict, raise it
