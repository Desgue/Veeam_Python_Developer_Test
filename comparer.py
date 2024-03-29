from pathlib import Path
import hashlib


class Comparer:
    """
    This class is responsible for comparing the source and replica folders providing the differences between them.

    @param source_path: pathlib.Path
        Path to the source folder
    @param replica_path: pathlib.Path
        Path to the replica folder
    @class attributes:
    self.source_content: list
        List of the content names of the source folder
    self.replica_content: list
        List of the content names of the replica folder
    self.source_only: list
        List of the content names that are only in the source folder
    self.replica_only: list
        List of the content names that are only in the replica folder
    self.common_dirs: list
        List of directory names that are common between source and replica
    self.common_file_names: list
        List of file names that are common between source and replica
    self.diff_files: list
        List of file names that are common between source and replica and have changed
    
    @method _compare: None
        Private method to compare the source and replica folders and store the results in class attributes
    @method file_changed: bool
        Private method to check if the file has changed by first comparing the size and modification time and later the hash
        to avoid unnecessary file reading
    """
     
    def __init__(self, source_path: Path, replica_path: Path):
        self.source_path = source_path
        self.replica_path = replica_path
        self._compare() 

    def _compare(self) -> None:
        """ Compare the source and replica folders and store the results in class attributes """
        self.source_content = [i.name for i in self.source_path.iterdir()]
        self.replica_content = [i.name for i in self.replica_path.iterdir()]
        self.source_only = [i for i in self.source_content if i not in self.replica_content]
        self.replica_only = [i for i in self.replica_content if i not in self.source_content]
        self.common_dirs = [i for i in self.source_content if i in self.replica_content and Path(self.source_path, i).is_dir() and Path(self.replica_path, i).is_dir()]
        self.common_file_names = [file_name for file_name in self.source_content if file_name in self.replica_content and Path(self.source_path, file_name).is_file() and Path(self.replica_path, file_name).is_file()]
        self.diff_files = [file_name for file_name in self.common_file_names if self._file_changed(Path(self.source_path, file_name), Path(self.replica_path, file_name))]

    def _file_changed(self, source_file: Path, replica_file: Path) -> bool:
        """
        Check if the file has changed by first comparing the size and modification time and later the hash
        to avoid unnecessary file reading
        """

        size_is_equal = source_file.stat().st_size == replica_file.stat().st_size
        last_MT_is_equal = source_file.stat().st_mtime == replica_file.stat().st_mtime

        if size_is_equal and last_MT_is_equal:
            return False
     
        with open(source_file, "rb") as f:
            source_hash = hashlib.md5(f.read())
            f.close()
        with open(replica_file, "rb") as f:
            replica_hash = hashlib.md5(f.read())
            f.close()
        return source_hash.hexdigest() != replica_hash.hexdigest()
