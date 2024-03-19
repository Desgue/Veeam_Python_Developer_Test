from pathlib import Path
import shutil
import filecmp
import os

class Synchronizer:
    def __init__(self, source, replica):
        self.source = source
        self.replica = replica

        
    def __str__(self):
        return f"Source: {self.source}\nReplica: {self.replica}"

    def synchronize(self) -> None:
        """ Sync the folders """
        compared = filecmp.dircmp(self.source, self.replica)
        for item in compared.left_only:
            to_copy = Path(self.source, item)
            if to_copy.is_file():
                print(f"\nCopying file-> {to_copy} to {self.replica}\n")
                try:
                    shutil.copy2(to_copy, Path(self.replica, item))
                except Exception as e:
                    print(f"Error copying {to_copy} -> {e}")

            if to_copy.is_dir():
                print(f"\nCopying folder-> {to_copy} to {self.replica}\n")
                try:
                    shutil.copytree(to_copy, Path(self.replica, item), copy_function=shutil.copy2, dirs_exist_ok=True)
                except Exception as e:
                    print(f"Error copying {to_copy} -> {e}")
        
        for item in compared.right_only:
            to_delete = Path(self.replica, item)
            if to_delete.is_file():
                print(f"\nDeleting file-> {to_delete}\n")
                try:
                    os.unlink(to_delete)
                except Exception as e:
                    print(f"Error deleting {to_delete} -> {e}")

            if to_delete.is_dir():
                print(f"\nDeleting folder-> {to_delete}\n")
                try:
                    shutil.rmtree(to_delete)
                except Exception as e:
                    print(f"Error deleting {to_delete} -> {e}") 

        for item in compared.diff_files:
            to_copy = Path(self.source, item)
            if to_copy.is_file():
                print(f"\nCopying file-> {to_copy} to {self.replica}\n")
                try:
                    shutil.copy2(to_copy, Path(self.replica, item))
                except Exception as e:
                    print(f"Error copying {to_copy} -> {e}")
            if to_copy.is_dir():
                print(f"\nCopying folder-> {to_copy} to {self.replica}\n")
                try:
                    shutil.copytree(to_copy, Path(self.replica, item), copy_function=shutil.copy2, dirs_exist_ok=True)
                except Exception as e:
                    print(f"Error copying {to_copy} -> {e}")

        for item in compared.common_dirs:
            print(f"\nSynching {item}\n")
            Synchronizer(self.source.joinpath(item), self.replica.joinpath(item)).synchronize()

