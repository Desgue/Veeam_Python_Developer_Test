from pathlib import Path
import shutil
import filecmp

class Directory:
    def __init__(self, path):
        self.path = Path(path)
        self.files = [x for x in self.path.iterdir() if x.is_file()]
        self.sub_dirs = [x for x in self.path.iterdir() if x.is_dir()]

    def __str__(self):
        return f"\n\tSub directories: {self.sub_dirs}\n\tFiles: {self.files}\n"


class Synchronizer:
    def __init__(self, source, replica):
        self.source = source
        self.replica = replica
        self.watcher = Watcher(source, replica)
        
    def __str__(self):
        return f"Source: {self.source}\nReplica: {self.replica}"
    def copy_all(self):
        return shutil.copytree( self.source,  self.replica,  copy_function=shutil.copy2, dirs_exist_ok=True )
    def delete_all(self):
        return shutil.rmtree(self.replica)
    def synchronize(self) -> None:
        """ Sync the folders """
        self.delete_all()
        return self.copy_all()

class Watcher: 
    def __init__(self, source, replica):
        self.source = Path(source)       
        self.source_sub_dirs = [x for x in self.source.iterdir() if x.is_dir()]
        self.source_files = [x for x in self.source.iterdir() if x.is_file()]

        self.replica = Path(replica)
        self.replica_sub_dirs = [x for x in self.replica.iterdir() if x.is_dir()]
        self.replica_files = [x for x in self.replica.iterdir() if x.is_file()]

    def __str__(self):
        return f"\n\tSub directories: {self.sub_dirs}\n\tFiles: {self.files}"

    def watch(self):
        compared = filecmp.dircmp(self.source, self.replica)
        for item in compared.left_only:
            to_copy = Path(self.source, item)
            if to_copy.is_file():
                print(f"\nCopying file-> {to_copy} to {self.replica}\n")
            if to_copy.is_dir():
                print(f"\nCopying folder-> {to_copy} to {self.replica}\n")
        
        for item in compared.right_only:
            to_delete = Path(self.replica, item)
            if to_delete.is_file():
                print(f"\nDeleting file-> {to_delete}\n")
            if to_delete.is_dir():
                print(f"\nDeleting folder-> {to_delete}\n")

        for item in compared.diff_files:
            to_copy = Path(self.source, item)
            if to_copy.is_file():
                print(f"\nCopying file-> {to_copy} to {self.replica}\n")
            if to_copy.is_dir():
                print(f"\nCopying folder-> {to_copy} to {self.replica}\n")

        for item in compared.common_dirs:
            print(f"\nWatching {item}\n")
            Watcher(self.source.joinpath(item), self.replica.joinpath(item)).watch()