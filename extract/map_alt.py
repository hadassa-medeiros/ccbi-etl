from datetime import datetime
from pathlib import Path
from map import get_hash
import csv
import os
from send2trash import send2trash

ROOT_ADMIN = "H:/Mi unidad/"
ROOT = "G:/.shortcut-targets-by-id/1eACn2_6E0dyS_j62ZPQLosrnryGZJHJg/"

AUX_DIR = "_CCBI ESTAGIARIOS/"
MAIN_DIR = ROOT_ADMIN + AUX_DIR + 'Ex bolsistas/'


SPECIFIC_DIR_ORIGIN = MAIN_DIR + '-Ana Letícia/Niate CTG CCEN'
SPECIFIC_DIR_REF = ROOT_ADMIN + '_CCBI COORDENAÇÃO/_CAMPI - DOCUMENTOS GERAIS/- 2 CAMPUS JOAQUIM AMAZONAS/46 NIATE CTG CCEN/46.1 Edifício Sede'

DIR_OUTPUTS = ROOT + '_CCBI COORDENAÇÃO/Organização Drive/[00] Administrativo/[01] Servidores/Hadassa Medeiros/ADMIN-Estruturacao_Banco_de_Dados/Entregas/'

SKIP_EXTENSIONS = {".ini", ".lnk", ".tmp"}

TODAY = datetime.now().strftime('%y-%m-%d_%H-%M')

folders = sorted([d for d in Path(MAIN_DIR).iterdir() if d.is_dir()])

# collect hashes for every file except inuteis
def gather_file_objects(folder: str) -> dict:
    folder_path_object = Path(folder)
    return [file for file in folder_path_object.rglob('*') if file.is_file() and file.suffix.lower() not in SKIP_EXTENSIONS]

def get_hashes(filepaths: list) -> list:
    names_and_hashes = []
    for file in filepaths:
        if file.is_file() and file.suffix.lower() not in SKIP_EXTENSIONS:
            hash = get_hash(file)
            names_and_hashes.append((file, hash))
    return names_and_hashes

def store_as_csv(data: list, header_titles, filename):
    with open(filename, mode='w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerow(header_titles)
        # prever n colunas conforme estrutura de data entrante
        writer.writerows([[x,y] for x,y in data])
        os.startfile(filename)

def read_csv(csvfile):
    with open(csvfile, encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=' ')
        for row in reader:
            print(row[-1])
        
if __name__ == '__main__':
    # csv_to_read = 'G:\.shortcut-targets-by-id\\1eACn2_6E0dyS_j62ZPQLosrnryGZJHJg\_CCBI COORDENAÇÃO\Organização Drive\[00] Administrativo\[01] Servidores\Hadassa Medeiros\ADMIN-Estruturacao_Banco_de_Dados\Entregas\_46 NIATE CTG CCEN_46.1 Edifício Sede_26-04-30_15-01.csv'
    # read_csv(csv_to_read)
    conjunto_A = get_hashes(gather_file_objects(SPECIFIC_DIR_ORIGIN))
    conjunto_B = get_hashes(gather_file_objects(SPECIFIC_DIR_REF))
    print(conjunto_B)
    matches = []
    for filepath_A,filehash_A in conjunto_A:
        for filepath_B, filehash_B in conjunto_B:
            print(filehash_A == filehash_B)
            if filehash_A == filehash_B:
                matches.append((filepath_B,(filehash_A, filehash_B)))
    print('matches', len(matches))
    print(matches)

    carpeta_madre = SPECIFIC_DIR_ORIGIN.split('/')[-1]
    carpeta_abuela = SPECIFIC_DIR_ORIGIN.split('/')[-2]
    filename = f'{DIR_OUTPUTS}_{carpeta_abuela}_{carpeta_madre}_{TODAY}.csv'
    store_as_csv(matches, ['Duplicatas'], filename)
#     else:
#         path = SPECIFIC_SUBDIR
#     data = gather_file_objects(path)
#     data_with_hashes = get_hashes(data)
#     header_titles = ['Caminho do arquivo', 'ID']
#     carpeta_madre = path.split('\\')[-1]
#     carpeta_abuela = path.split('\\')[-2]
#     filename = f'{DIR_OUTPUTS}_{carpeta_abuela}_{carpeta_madre}_{TODAY}.csv'
#     store_as_csv(data_with_hashes, header_titles, filename)
