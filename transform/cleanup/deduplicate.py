from pathlib import Path
import csv
from datetime import datetime
import os
from extract.map import get_hash
from send2trash import send2trash


def excluir_arquivos_com_copias(confirmed_copies):
    excluidos_contagem = 0
    for item in confirmed_copies:
        path = item['Caminho Arquivo A']
        try:
            send2trash(path)
            excluidos_contagem += 1
        except FileNotFoundError as e:
            print(f"{path} não encontrado para exclusão.")
    print(f"{excluidos_contagem} arquivo(s) excluído(s).")

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
        

def compare(dict_A, dict_B, comparison_key_A: str, comparison_key_B: str, comparison_key_C: str):
    lookup_B = {}
    for path_B, info_B in dict_B.items():
        key = (info_B.get(comparison_key_A), info_B.get(comparison_key_B), info_B.get(comparison_key_C))
        if key not in lookup_B:
            lookup_B[key] = []
        lookup_B[key].append((path_B, info_B))
    confirmed_copies = []
    excluidos_contagem = 0

    for path_A, info_A in dict_A.items():
        key_A = (info_A.get(comparison_key_A), info_A.get(comparison_key_B), info_A.get(comparison_key_C))
        if key_A in lookup_B:
            hash_A = get_hash(path_A)
            for path_B, info_B in lookup_B[key_A]:
                hash_B = get_hash(path_B)
                if hash_A and hash_B and hash_A == hash_B:
                    print(f"Cópia confirmada: {path_A.name} == {path_B.name} (hash: {hash_A})")
                    info_A['Hash (ID)'] = hash_A
                    info_A['Hash (ID) da cópia'] = hash_B
                    confirmed_copies.append({
                        'Caminho Arquivo A': path_A,
                        'Arquivo A': str(path_A),
                        'Arquivo B': str(path_B),
                        'ID Arquivo A': hash_A,
                        'ID Arquivo B': hash_B,
                        'Status': 'Excluído'
                    })
                    send2trash(path_A)
                    excluidos_contagem += 1
                    print(excluidos_contagem)

                else:
                    print(f"Match nos critérios, mas hash diferente: {path_A.name} vs {path_B.name}")

    # return dict_A
    return confirmed_copies

if __name__ == '__main__':
    