import os
import re
import requests
from database.models.sample import get_project_from_sample, edit_sample_name

# Regex para extrair a informação desejada
regex_pattern = r'[A-Za-z0-9\-]+_S\d+_L\d{3}_R[12]_001'

# Função para buscar o conteúdo no site e extrair a string com o regex
def get_renaming_pattern(srr_id):
    url = f"https://www.ncbi.nlm.nih.gov/sra/{srr_id}"
    response = requests.get(url)
    if response.status_code == 200:
        match = re.search(regex_pattern, response.text)
        if match:
            return match.group(0)  # Retorna a string encontrada
    return None

# Função principal para processar os arquivos
def rename_sample_sra(result_path, sample_name, sample_uuid):
    project_uuid = get_project_from_sample(sample_uuid)['uuid']
    sample_path = f"{result_path}/{project_uuid}/{sample_uuid}"

    for filename in os.listdir(sample_path):
        # Extrai o ID SRR
        
        # Busca o padrão de renomeação no site NCBI
        new_pattern = get_renaming_pattern(sample_name)
        print(new_pattern)

        reverse_sra=[f for f in os.listdir(sample_path) if f.startswith(f"{sample_name}_R2")]
        
        if new_pattern:
            # Renomear os arquivos R1 e R2
            print(filename)
            new_filename = f"{new_pattern}.fastq.gz"
            new_reverse_filename = f"{new_pattern.replace('R1', 'R2')}.fastq.gz"
            
            # Renomeia o arquivo
            old_file_path = os.path.join(sample_path, filename)
            new_file_path = os.path.join(sample_path, new_filename)
            
            print(f"Renomeando {old_file_path} para {new_file_path}")
            os.rename(old_file_path, new_file_path)

            old_file_path = os.path.join(sample_path, reverse_sra[0])
            new_file_path = os.path.join(sample_path, new_reverse_filename)
            
            print(f"Renomeando {old_file_path} para {new_file_path}")
            os.rename(old_file_path, new_file_path)
            edit_sample_name(sample_uuid, new_pattern)
        else:
            print(f"Padrão não encontrado para {sample_name}")
