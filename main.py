from pathlib import Path
import shutil
import filecmp
import os
import time

from sync import Synchronizer
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



def main() -> None:
    """ Main function """

    while True:

        if not Path(SOURCE).exists():
            print("Source folder does not exist")
            return
        if not Path(REPLICA).exists():
            os.mkdir(REPLICA)

        source = Path(SOURCE)
        replica = Path(REPLICA)
        sync = Synchronizer(source, replica)
        sync.synchronize()

        time.sleep(5)

if __name__ == "__main__":
    main()

