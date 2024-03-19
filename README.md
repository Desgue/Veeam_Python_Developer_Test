# Veeam_Python_Developer_Test
This is an assessment for a job position at Veeam as a Python Developer in QA

## The (naive) Solution

My first approach to this problem was use a built in pyhon library to perform the filer/folder comparison and focus on the synchronization logic, as I wasnt sure if using a lib for that purpose was allowed I later implemented my own version using MD5 hash algorithm from hashlib to perform the comparison.

The main alrogithm logic is the following:

1. Check if there is any missing file or folder in the replica comparing to the files/folders in source.
2. Remove any extra file/folder in replica that is not present in source.
3. Check for common files that have changed between replica and source folders and copy the changed files to replica.
4. Recursively search inside the common folders between source and replica.

The lib used for comparing produces different generators for each scenario:

. left_only

. right_only

. diff_files

. common_dirs

Were the ones I used to perform the checking necessary. In the final solution I recreated this same functionality so I could reuse the code in the Synchronizer class with minimum changes as possible.

The Synchronizer class hold the logic for the algorithm.

```Python
class Synchronizer:
    """
    Synchronizer class to sync the source and replica folders

    @param source: pathlib.Path 
        Path to the source folder
    @param replica: pathlib.Path 
        Path to the replica folder
    @param logger: logging.Logger 
        Logger object responsible for logging the actions to a file and to stdout

    All methods are only performed in root level of the source and replica folders, thats why there is a recursive call to the synchronize method in the search_child_folders method.

    @method add_missing_in_backup: Search for files and folders not present in backup but present in source and copy it to backup
    @method remove_extra_in_backup: Search for files and folders not present in source but present in backup and remove it from backup 
    @method sync_changed_files: Search for files that have been changed and sync it to backup
    @method search_child_folders: Recursively search common folders between source and backup
    @method synchronize: Main method to synchronize the source and replica folders

    """
```

## Installation
### Requirements

**Python v3.12**

**pip v23.3.2**

1. Clone the repository

```
git clone https://github.com/Desgue/Veeam_QA_WEB_Test_task.git
```

## Usage

```bash
python main.py [--source <path_to_source_folder>] [--backup <path_to_backup_folder>] [--log <path_to_log_file>] [--interval <interval_number_in_seconds>]
 ```


