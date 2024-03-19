# Veeam_Python_Developer_Test
This is an assessment for a job position at Veeam as a Python Developer in QA

## The Final Solution
In my final approach I decided to implement my own version of the main functionality I need from [filecmp](https://docs.python.org/3/library/filecmp.html).  

For that I created a Comparer class that compare two paths and produces lists for different comparison scenarios that I can in turn use to sync based on each scenario.

1. source_only
    - List of the content names that are only in the source folder

2.  replica_only
    - List of the content names that are only in the replica folder

3. common_dirs
    - List of directory names that are common between source and replica

4. diff_files
    - List of file names that are common between source and replica and have changed.
    - Uses last modified time and file size for a first comparison to avoid the memory consuming hashing function.
    - Uses the md5 hashing function from [hashlib](https://docs.python.org/3/library/hashlib.html) if any of the previous checks fail.
    - This comparison approach makes a tradeoff between security for performance, a production grade tool might have to focus more on security or provide a flag for the user to choose between which approach best suits him.
    
With that I can implement the Synchronizer class in the same way I was when using the filecmp lib in the naive solution



## The Synchronizer class
```Python
class Synchronizer:
    """
    Synchronizer class to sync the source and replica folders

    @param source: pathlib.Path 
        Path to the source folder
    @param replica: pathlib.Path 
        Path to the replica folder
    @param logger: loggin.Logger 
        Logger object responsible for logging the actions to a file and to stdout

    All methods are only performed in root level of the source and replica folders, thats why there is a recursive call to the synchronize method in the search_child_folders method.

    @method add_missing_in_backup: Search for files and folders not present in backup but present in source and copy it to backup
    @method remove_extra_in_backup: Search for files and folders not present in source but present in backup and remove it from backup 
    @method sync_changed_files: Search for files that have been changed and sync it to backup
    @method search_child_folders: Recursively search common folders between source and backup
    @method synchronize: Main method to synchronize the source and replica folders

    """
```
This class implements 3 methods that satisfies the requirements for the challenge.

1. add_missing_in_backup
    - Checks the source_only list for files or folders that are only present in the source folder and copies them to the replica folder.

2. remove_extra_in_backup
    - Checks the replica_only list for files or folders that are not present in the source and remove them from the replica folder.

3. sync_changed_files
    - Checks the diff_files list for items that are presents in both folders but have different contents and them copies from source folder to replica folder.

4. search_child_folders
    - Check for folders present in both source and replica folders and peform a recursion creating a new Synchronizer object and performing the same sync process in both child folders until there is no more child folder common between two parent ones.
   
## Installation
### Requirements

**Python v3.12**

**pip v23.3.2**

1. Clone the repository

```
git clone https://github.com/Desgue/Veeam_Python_Developer_Test/tree/implement/final-solution
```

## Usage

```bash
python main.py [--source <path_to_source_folder>] [--backup <path_to_backup_folder>] [--log <path_to_log_file>] [--interval <interval_number_in_seconds>]
 ```

