import os
import csv
from pathlib import Path
from datetime import datetime

today = datetime.today().date()

def map_directory(path: Path):
    path = Path(path)
    origin_files_dicts = {}
    all_keys = set()

    for item in path.rglob('*'):
        if item.is_file() and item.suffix != '.ini':
            mtime_timestamp = item.stat().st_mtime
            last_modification_date = datetime.fromtimestamp(mtime_timestamp).strftime('%Y-%m-%d')
            parents = [parent.name for parent in reversed(item.parents[0:-4])]
            file_info = {
                "Nome": item.stem,
                "Extensão": item.suffix,
                "Tamanho (bytes)": item.stat().st_size,
                "Última atualização": last_modification_date,
                "Hash (ID)": '',
                "Cópia": '',
                "Loc. Cópia": '',
                "Tamanho Cópia (para conferência)": ''

            }
            for index, parent in enumerate(parents):
                file_info[f'Nível {index}'] = parent
            origin_files_dicts[item] = file_info
            all_keys.update(file_info.keys())

    fieldnames = sorted(list(all_keys))
    return {"headers": fieldnames, "content": origin_files_dicts}

def save_dict_to_csv(data: dict, filename: str, fieldnames):
    filename = filename + f'_{today.strftime("%Y-%m-%d")}.csv'
    # print(filename)
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=' ')
        writer.writeheader()
        for value in data.values():
            writer.writerow(value)
        os.startfile(filename)
