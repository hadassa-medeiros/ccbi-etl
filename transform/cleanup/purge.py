from pathlib import Path
import csv
from datetime import datetime
import os


today = datetime.today().date()

class Purge:
    def __init__(self, where_to_purge, deletable_extensions):
        self.deletable_extensions = deletable_extensions
        self.where_to_purge = where_to_purge

    def scan(self):
        dir = Path(self.where_to_purge)

        files_by_extension = []

        for ext in self.deletable_extensions:
            print(ext)
            deletable_files = dir.rglob(f"*{ext}")
            files_by_extension.extend(deletable_files)
            print(files_by_extension)

        filename = f'_{dir.name}_{today.strftime("%Y-%m-%d")}.csv'  # F-string e formatação
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([[f] for f in files_by_extension])  # Escreve como lista de listas (uma coluna)
            os.startfile(filename)
    # def execute(self):,