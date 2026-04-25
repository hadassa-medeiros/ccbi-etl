import yaml
from pathlib import Path


class Purge:
    def __init__(self, where_to_purge, deletable_extensions):
        self.deletable_extensions = deletable_extensions
        self.where_to_purge = where_to_purge

    def scan(self):
        dir = Path(self.where_to_purge)
        all_deletable_files = []
        for deletable_extension in self.deletable_extensions:
            print(deletable_extension)
            deletable_files = dir.rglob(f"*{deletable_extension}")
            print(deletable_files)
            all_deletable_files.extend(deletable_files)
        print(dir, all_deletable_files)
    # def execute(self):