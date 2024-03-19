from comparer import Comparer
from pathlib import Path
import shutil
import filecmp
import os

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
    
    def __init__(self, source: Path, replica: Path, logger):
        """
        Constructor for the Synchronizer object
        
        @param source: pathlib.Path 
            Path to the source folder
        @param replica: pathlib.Path 
            Path to the replica folder
        @param logger: logging.Logger 
            Logger object responsible for logging the actions to a file and to stdout
        
        """
        self.source = source
        self.replica = replica
        self.logger = logger
        self.compared = Comparer(self.source, self.replica)
        self.error_message = "Error %s %s -> %s"
        self.log_message = "%s %s -> %s to %s"
        self.delete_message = "Deleting %s -> %s"
        
    def __str__(self):
        return f"Source: {self.source}\nReplica: {self.replica}"

    def add_missing_in_backup(self) -> None:
        """Search for files and folders not present in backup but present in source and copy it to backup"""
        for item in self.compared.source_only:
            to_copy = Path(self.source, item)
            action = "Copying"
            if to_copy.is_file():
                try:
                    shutil.copy2(to_copy, Path(self.replica, item))
                    self.logger.info(f"File {to_copy} is not present in replica folder and will be copied.")
                    self.logger.info(self.log_message, action, "file", to_copy, self.replica)
                except Exception as e:
                    self.logger.error(self.error_message,action, "file", e)
                    
            if to_copy.is_dir():
                try:
                    shutil.copytree(to_copy, Path(self.replica, item), copy_function=shutil.copy2, dirs_exist_ok=True)
                    self.logger.info(f"Folder {to_copy} is not present in replica folder and will be copied.")
                    self.logger.info(self.log_message, action, "folder", to_copy, self.replica)
                except Exception as e:
                    self.logger.error(error_message,action, to_copy, e)

    def remove_extra_in_backup(self) -> None:
        """Search for files and folders not present in source but present in backup and remove it from backup"""
        for item in self.compared.replica_only:
            to_delete = Path(self.replica, item)
            action = "Deleting"
            if to_delete.is_file():
                try:
                    os.unlink(to_delete)
                    self.logger.info(f"File {to_delete} is not present in source folder and will be deleted from replica.")
                    self.logger.info(self.delete_message, "file", to_delete)

                except Exception as e:
                    self.logger.error(self.error_message, action, "file", to_delete, e)

            if to_delete.is_dir():
                try:
                    shutil.rmtree(to_delete)
                    self.logger.info(f"Folder {to_delete} is not present in source folder and will be deleted from replica.")
                    self.logger.info(self.delete_message, "folder", to_delete)

                except Exception as e:
                    self.logger.error(self.error_message, action, "folder", to_delete, e)

    def sync_changed_files(self) -> None:
        """Search for files that have been changed and sync it to backup"""
        for item in self.compared.diff_files:
            to_copy = Path(self.source, item)
            action = "Syncing"
            if to_copy.is_file():
                try:
                    shutil.copy2(to_copy, Path(self.replica, item))
                    self.logger.info(f"File {self.source.joinpath(to_copy)} is out of sync with {self.replica.joinpath(item)}.")
                    self.logger.info(self.log_message, action, "file", to_copy, self.replica.joinpath(item))
                except Exception as e:
                    self.logger.error(self.error_message, action, "file", to_copy, e)

    def search_child_folders(self) -> None:
        """Recursively search common folders between source and backup"""
        for item in self.compared.common_dirs:
            Synchronizer(Path(self.source, item), Path(self.replica, item), self.logger).synchronize()

    def synchronize(self) -> None:
        """ Main method to synchronize the source and replica folders """
        self.add_missing_in_backup()
        self.remove_extra_in_backup()
        self.sync_changed_files()
        self.search_child_folders()

