'''
1-if nome e size match, é cópia

'''
from pathlib import Path
import csv
from datetime import datetime
import os
import hashlib

def get_hash(file_path: Path) -> str:
    """Calcula o hash SHA256 do arquivo para identificação única."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except (OSError, IOError) as e:
        print(f"Erro ao calcular hash para {file_path}: {e}")
        return ''


class Deduplicate:
    def __init__(self, origin_dir, ref_dir):
        self.origin_dir = origin_dir
        self.ref_dir = ref_dir

    def find_duplicates(self):
        p_origin = Path(self.origin_dir)
        p_ref = Path(self.ref_dir)

        origin_files_dicts = {}
        all_keys = set()

        for item in p_origin.rglob('*'):
            if item.is_file() and item.suffix != '.ini':
                mtime_timestamp = item.stat().st_mtime
                last_modification_date = datetime.fromtimestamp(mtime_timestamp).strftime('%Y-%m-%d')
                parents = [parent.name for parent in reversed(item.parents[0:-4])]
                file_info = {
                    "Nome": item.stem,
                    "Extensão": item.suffix,
                    "Tamanho (bytes)": item.stat().st_size,
                    "Última atualização": last_modification_date,
                    "Hash (ID)": get_hash(item)
                }
                for index, parent in enumerate(parents):
                    file_info[f'Nível {index}'] = parent
                origin_files_dicts[item] = file_info
                all_keys.update(file_info.keys())
        

def compare(files_A, files_B, comparison_key_A: str, comparison_key_B: str, comparison_key_C: str):
    # files_A e files_B são dicts {path: info_dict}
    # Cria um dicionário de lookup para files_B, usando uma tupla como chave composta pelos 3 critérios
    lookup_B = {}
    for path_B, info_B in files_B.items():
        key = (info_B.get(comparison_key_A), info_B.get(comparison_key_B), info_B.get(comparison_key_C))
        if key not in lookup_B:
            lookup_B[key] = []
        lookup_B[key].append((path_B, info_B))  # Armazena (path, info) para acesso ao path

    # Lista para armazenar as cópias confirmadas (após verificação de hash)
    confirmed_copies = []

    for path_A, info_A in files_A.items():
        key_A = (info_A.get(comparison_key_A), info_A.get(comparison_key_B), info_A.get(comparison_key_C))
        if key_A in lookup_B:
            # Match nos 3 critérios: calcula hash para confirmar
            hash_A = get_hash(path_A)
            for path_B, info_B in lookup_B[key_A]:
                hash_B = get_hash(path_B)
                if hash_A and hash_B and hash_A == hash_B:
                    # Cópia confirmada
                    confirmed_copies.append({
                        'arquivo_A': str(path_A),
                        'hash_A': hash_A,
                        'arquivo_B': str(path_B),
                        'hash_B': hash_B
                    })
                    print(f"Cópia confirmada: {path_A.name} == {path_B.name} (hash: {hash_A})")
                else:
                    print(f"Match nos critérios, mas hash diferente: {path_A.name} vs {path_B.name}")

    return confirmed_copies