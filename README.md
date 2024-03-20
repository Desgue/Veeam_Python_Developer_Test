# Veeam_Python_Developer_Test
This is an assessment for a job position at Veeam as a Python Developer in QA

## The Challenge

Please implement a program that synchronizes two folders: source and replica. The
program should maintain a full, identical copy of source folder at replica folder.
Solve the test task by writing a program in one of these programming languages:

- Python
- C/C++
- C#

1. Synchronization must be one-way: after the synchronization content of the
replica folder should be modified to exactly match content of the source
folder;

2. Synchronization should be performed periodically.

3. File creation/copying/removal operations should be logged to a file and to the
console output;

4. Folder paths, synchronization interval and log file path should be provided using the command line arguments;

5. It is undesirable to use third-party libraries that implement folder
synchronization;

6. It is allowed (and recommended) to use external libraries implementing other
well-known algorithms. For example, there is no point in implementing yet
another function that calculates MD5 if you need it for the task – it is
perfectly acceptable to use a third-party (or built-in) library.

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
    - Uses file name, last modified time and file size for a first comparison to avoid the memory consuming hashing function.
    - Uses the md5 hashing function from [hashlib](https://docs.python.org/3/library/hashlib.html) if any of the previous checks fail.
    - This comparison approach makes a tradeoff between security for performance, a production grade tool might have to focus more on security or provide a flag for the user to choose between which approach best suits him.
    
With that I can implement the Synchronizer class in the same way when using the [filecmp](https://docs.python.org/3/library/filecmp.html) lib in the [naive solution](https://github.com/Desgue/Veeam_Python_Developer_Test/tree/implement/naive-solution)



## The Synchronizer class
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
This class implements 4 methods that satisfies the requirements for the challenge.

1. add_missing_in_backup
    - Checks the source_only list for files or folders that are only present in the source folder and copies them to the replica folder.

2. remove_extra_in_backup
    - Checks the replica_only list for files or folders that are not present in the source and remove them from the replica folder.

3. sync_changed_files
    - Checks the diff_files list for items that are presents in both folders but have different contents and them copies from source folder to replica folder.

4. search_child_folders
    - Check for folders present in both source and replica folders and peform a recursion creating a new Synchronizer object and performing the same sync process in both child folders until there is no more child folder common between two parents.
   
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

### Arguments

#### `-h`, `--help`
- Description: Show the help menu that indicates what each command does and how to use it.
- Usage: `-h` or `--help` 

#### `-s`, `--source`
- Description: Absolute path for the source folder.
- Usage: `--source <absolute_path_to_source_folder>` or `-s <absolute_path_to_source_folder>` 
- Required: True
- Type: String

#### `-b`, `--backup` 
- Description: Absolute path to the replica folder.
- Usage: `--backup <absolute_path_to_replica_folder>` or `-b <absolute_path_to_replica_folder>`
- Required: True
- Type: String

#### `-l`, `--log` 
- Description: Absolute path to the .log file, if the file do not exist it will be created.
- Usage: `--l <absolute_path_to_log_file>` or `--log <absolute_path_to_log_file>`
- Required: True
- Type: String 

#### `-i`, `--interval`
- Description: Specify the interval time to wich the program will perform the synchronization task. Expressed in seconds. Default is 60 seconds.
- Usage: `-i <interval_number_in_seconds>` or `--interval <interval_number_in_seconds>`
- Default: 60s
- Type: Integer


## Final Considerations

1. Error handling could be improve, for that I need to read the docs of each lib I am using and understand what kind of exceptions can happen with the methods.
2. Even tough I performed manual testing to ensure all behaviors function as expected, an automated test script can be created to check thoroughly.
3. Better handling of the terminal interface to accept a more gracefull shutdown instead using ctrl+c to stop the script, thus making it possible to also log the end of script session for further analysis.

Total time spend In this project was about 8 hours spread between reading about folder synchronization, searching for and reading the docs of which libraries I decided to use and actually implementing and refactoring the code. 

