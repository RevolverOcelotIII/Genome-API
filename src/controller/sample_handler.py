import sys
import threading
import os
import shutil
import re
import requests

sys.path.append('../')

from flask import jsonify
from database.models.sample import create_sample, remove_sample_from_database, get_project_from_sample, get_sample_genes, get_sample, edit_sample_name
from controller.get_sra_info import rename_sample_sra
from pipeline.Phenotypes_Finder.implementation.pipeline_Trimmomatic.Trimmomatic import trimmomatic
from pipeline.Phenotypes_Finder.implementation.Find_SNPs.SNP_finder import find_snps

def run_pipeline_in_background(sample_name, sample_uuid, project_uuid, genes):
    thread = threading.Thread(target=trimmomatic, args=(project_uuid, sample_name, sample_uuid, genes))
    thread.start()
    #trimmomatic(project_uuid, sample_name, sample_uuid, genes)

def add_sample(project_folder, project_uuid, files, genes, is_sra):
    samples = []
    sample_name = ''
    sample_folder = ''
    for file in sorted(files, key=lambda file: (file.filename.lower())):
        print(file.filename)
        if file.filename and file.filename.endswith('.fastq.gz'):  # Certifique-se de que o arquivo tenha um nome válido
            sample_name = file.filename.strip('.fastq.gz').split('_R1')[0].split('_R2')[0]
            if not any(sample['name'] == sample_name for sample in samples):
                sample_uuid = create_sample(project_uuid, sample_name, genes)
                sample_folder = f"{project_folder}/{sample_uuid}"
                if not os.path.exists(sample_folder):
                    os.makedirs(sample_folder, exist_ok=True)
                samples.append({'name': sample_name, 'uuid': sample_uuid})
            filepath = os.path.join(sample_folder, file.filename)
            file.save(filepath)

    for sample in samples:
        if is_sra:
            get_sra_sample_name(sample['uuid'], sample['name'])

        print(sample)
        run_pipeline_in_background(sample['name'], sample['uuid'], project_uuid, genes)
        
    return jsonify({
        "message": "Arquivos salvos com sucesso!"
    }), 200

def remove_sample(sample_uuid, upload_path, result_path, trimm_path, sheet_path):
    project_uuid = get_project_from_sample(sample_uuid)
    remove_sample_from_database(sample_uuid)
    sample_path = f"{upload_path}/{project_uuid}/{sample_uuid}"
    if os.path.exists(sample_path):
        try:
            shutil.rmtree(sample_path)
            print(f"Diretório '{sample_path}' removido com sucesso.")
        except OSError as e:
            print(f"Erro ao remover o diretório '{sample_path}': {e}")
    sample_path = f"{result_path}/{sample_uuid}"
    if os.path.exists(sample_path):
        try:
            shutil.rmtree(sample_path)
            print(f"Diretório '{sample_path}' removido com sucesso.")
        except OSError as e:
            print(f"Erro ao remover o diretório '{sample_path}': {e}")
    sample_path = f"{trimm_path}/{sample_uuid}"
    if os.path.exists(sample_path):
        try:
            shutil.rmtree(sample_path)
            print(f"Diretório '{sample_path}' removido com sucesso.")
        except OSError as e:
            print(f"Erro ao remover o diretório '{sample_path}': {e}")

    sample_path = f"{sheet_path}/{sample_uuid}"
    if os.path.exists(sample_path):
        try:
            shutil.rmtree(sample_path)
            print(f"Diretório '{sample_path}' removido com sucesso.")
        except OSError as e:
            print(f"Erro ao remover o diretório '{sample_path}': {e}")
    sample_path = f"{trimm_path}/{sample_uuid}"
    if os.path.exists(sample_path):
        try:
            shutil.rmtree(sample_path)
            print(f"Diretório '{sample_path}' removido com sucesso.")
        except OSError as e:
            print(f"Erro ao remover o diretório '{sample_path}': {e}")

def get_sample_info(sample_uuid):
    genes = get_sample_genes(sample_uuid)
    project_uuid = get_project_from_sample(sample_uuid)
    sample_name = get_sample(sample_uuid)['name']
    sample_data = {}
    for gene in genes:
        sample_data[gene['name']] = find_snps(project_uuid, sample_name, sample_uuid, gene['name'])
    print(sample_data)
    
    return sample_data

def get_sra_sample_name(sample_uuid, sample_name):
    regex_pattern = r'[A-Za-z0-9\-]+_S\d+_L\d{3}_R[12]_001'
    url = f"https://www.ncbi.nlm.nih.gov/sra/{sample_name}"
    response = requests.get(url)
    if response.status_code == 200:
        match = re.search(regex_pattern, response.text)
        if match:
            edit_sample_name(sample_uuid, match.group(0).split('_R1')[0])
            return 
    return None