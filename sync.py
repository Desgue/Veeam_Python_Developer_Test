from pathlib import Path
import shutil
import filecmp
import os

class Synchronizer:
    def __init__(self, source, replica, logger):
        self.source = source
        self.replica = replica
        self.logger = logger
        self.error_message = "Error %s %s -> %s"
        self.log_message = "%s %s -> %s to %s"
        self.delete_message = "Deleting %s -> %s"
        
    def __str__(self):
        return f"Source: {self.source}\nReplica: {self.replica}"

    def synchronize(self) -> None:
        """ Sync the folders """
        compared = filecmp.dircmp(self.source, self.replica)
        for item in compared.left_only:
            to_copy = Path(self.source, item)
            action = "Copying"
            if to_copy.is_file():
                try:
                    shutil.copy2(to_copy, Path(self.replica, item))
                    self.logger.info(self.log_message, action, "file", to_copy, self.replica)
                except Exception as e:
                    self.logger.error(self.error_message,action, "file", e)
                    
            if to_copy.is_dir():
                try:
                    shutil.copytree(to_copy, Path(self.replica, item), copy_function=shutil.copy2, dirs_exist_ok=True)
                    self.logger.info(self.log_message, action, "folder", to_copy, self.replica)

                except Exception as e:
                    self.logger.error(error_message,action, to_copy, e)


        
        for item in compared.right_only:
            to_delete = Path(self.replica, item)
            action = "Deleting"
            if to_delete.is_file():
                try:
                    os.unlink(to_delete)
                    self.logger.info(self.delete_message, "file", to_delete)

                except Exception as e:
                    self.logger.error(self.error_message, action, "file", to_delete, e)

            if to_delete.is_dir():
                try:
                    shutil.rmtree(to_delete)
                    self.logger.info(self.delete_message, "folder", to_delete)

                except Exception as e:
                    self.logger.error(self.error_message, action, "folder", to_delete, e)

        for item in compared.diff_files:
            to_copy = Path(self.source, item)
            action = "Copying"
            if to_copy.is_file():
                try:
                    shutil.copy2(to_copy, Path(self.replica, item))
                    self.logger.info(self.log_message, action, "file", to_copy, self.replica)
                except Exception as e:
                    self.logger.error(f"Error copying {to_copy} -> {e}")
            if to_copy.is_dir():
                try:
                    shutil.copytree(to_copy, Path(self.replica, item), copy_function=shutil.copy2, dirs_exist_ok=True)
                    self.logger.info(self.log_message, action, "folder", to_copy, self.replica)
                except Exception as e:
                    self.error_message(self.error_message, action, "folder", to_copy, e)

        for item in compared.common_dirs:
            Synchronizer(self.source.joinpath(item), self.replica.joinpath(item), self.logger).synchronize()

