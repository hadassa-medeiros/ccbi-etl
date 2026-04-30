import os
import csv
from pathlib import Path
from datetime import datetime
import hashlib
from send2trash import send2trash


def get_hash(file_path: Path) -> str:
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except (OSError, IOError) as e:
        print(f"Erro ao calcular hash para {file_path}: {e}")
        return ''

today = datetime.today()

def map_directory(path: Path):
    path = Path(path)
    results = {}
    all_keys = set()

    counter = 0
    for item in path.rglob('*'):
        if item.is_file() and item.suffix != '.ini':
            counter += 1
            if counter % 5000 == 0:
                print(f"  ...{counter} arquivos processados")
            mtime_timestamp = item.stat().st_mtime
            last_modification_date = datetime.fromtimestamp(mtime_timestamp).strftime('%Y-%m-%d')
            parents = [parent.name for parent in reversed(item.parents[0:-2])]
            file_info = {
                "Nome": item.stem,
                "Extensão": item.suffix.lower(),
                "Tamanho (bytes)": item.stat().st_size,
                "Última atualização": last_modification_date,
                # "Hash (ID)": get_hash(item),
                "Hash (ID)": '',
                "Tem cópia": '',
                "Loc. Cópia": '',
                "Tamanho Cópia (para conferência)": '',
                "Hash (ID) da cópia": '',
                "Status": '',
                "Caminho completo (desktop)": str(item)
            }
            for index, parent in enumerate(parents):
                file_info[f'Nível {index}'] = parent
            results[item] = file_info
            all_keys.update(file_info.keys())

    fieldnames = sorted(list(all_keys))
    return {"headers": fieldnames, "content": results}

def save_dict_to_csv(data: dict, filename: str):
    filename = filename + f'_{today.strftime("%Y-%m-%d-%H-%M")}.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data["headers"], delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for value in data["content"].values():
            writer.writerow(value)
        print(f'CSV salvo: {filename}')
        # os.startfile(filename)  # Removido para evitar abertura automática

def find_empty_dirs(path: Path):
    path = Path(path)
    results = []
    all_keys = set()

    for item in path.rglob('*'):
        item_size = item.stat().st_size
        if item.is_dir() and item_size == 0:
            print(item.stem, item_size)
        results.append(item)
    return results

def delete_dirs(dirs: list[str]):
    deleted = []
    for dir in dirs:
        print(f'Excluindo {dir}')
        send2trash(dir)
        deleted.append()
    print(deleted)
    return deleted
    

# def compare_hashes_from_csvs(csv_A, csv_B):
    