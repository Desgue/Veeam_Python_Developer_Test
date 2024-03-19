from pathlib import Path
import shutil
import filecmp
import os
import time
""" Naive Solution """

"""
1. Check if the source folder exists
2. Check if the replica folder exists
3. If Replica folder does not exist, create it and copy the contents of the source folder
4. If Source and Replica folder exists, check if they have the same content
5. If they have same content do nothing
6. If content differs, copy the new content from the source folder to the replica folder

"""
SOURCE = "C:/Users/guede/code/Veeam_Python_Developer_Test/Source"
REPLICA = "C:/Users/guede/code/Veeam_Python_Developer_Test/Replica"

def folder_exists(path_to_folder: str) -> bool:
    """ Check if folder exists"""  
    return Path(path_to_folder).exists()

def copy_folder_contents(source: str, replica: str) -> None:
    """Copy the contents of the folder, if Replica folder does not yet exist it will be created"""
    return shutil.copytree(
        source, 
        replica, 
        copy_function=shutil.copy2,
        dirs_exist_ok=True
        )
def delete_extra_in_replica(source: str, replica: str) -> None:
    """Delete the contents of the folder"""
    c = filecmp.dircmp(source, replica)
    for content in c.right_only:
        file_path= Path().joinpath(replica, content)
        try:
            if file_path.is_file():
                print(f"Deleting {file_path}")
                os.unlink(file_path)
            elif file_path.is_dir():
                print(f"Deleting {file_path}")
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    return

def copy_diff_content(source: str, replica: str) -> None:
    """ Copy the different contents between both folders """
    c = filecmp.dircmp(source, replica)
    for file in c.diff_files:
        to_copy = Path().joinpath(source, file)
        if to_copy.is_file():
            destination = Path().joinpath(replica, file)
            shutil.copy2(to_copy, destination )
            print(f"Copying {to_copy} to {destination}")
        if to_copy.is_dir():
            copy_folder_contents(to_copy, Path().joinpath(replica, file))
    for file in c.left_only:
        to_copy = Path().joinpath(source, file)
        if to_copy.is_file():
            shutil.copy2(Path().joinpath(source, file), Path().joinpath(replica, file))
            print(f"Copying {file} to {replica}")
        if to_copy.is_dir():
            copy_folder_contents(to_copy, Path().joinpath(replica, file))
    return

def sync_folders(source: str, replica: str) -> None:
    """ Sync the folders """
    copy_diff_content(source, replica)
    delete_extra_in_replica(source, replica)
    return

def main() -> None:
    """ Main function """
    while True:
        if not folder_exists(SOURCE):
            print("Source folder does not exist")
            break
        if not folder_exists(REPLICA):
            print("Replica folder does not exist\nCreating Replica folder and copying source files...")
            copy_folder_contents(SOURCE, REPLICA)

        sync_folders(SOURCE, REPLICA)
        time.sleep(5)
        
    return

if __name__ == "__main__":
    main()

