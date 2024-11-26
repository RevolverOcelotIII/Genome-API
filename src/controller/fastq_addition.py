import sys
import threading
import os
import shutil

sys.path.append('../')

from flask import Flask, jsonify
from database.models.sample import create_sample, remove_sample_from_database, get_project_from_sample
from pipeline.Phenotypes_Finder.implementation.pipeline_Trimmomatic.Trimmomatic import trimmomatic

def run_pipeline(sample_name, sample_uuid, project_uuid, genes):
    trimmomatic(project_uuid, sample_name, sample_uuid, genes)

def add_sample(project_folder, project_uuid, files, genes):
    samples = []
    sample_name = ''
    sample_folder = ''
    for file in sorted(files, key=lambda file: ("R1" not in file.filename, file.filename.lower())):
        if file.filename and file.filename.endswith('.fastq.gz'):  # Certifique-se de que o arquivo tenha um nome válido
            if '_R1' in file.filename:
                sample_name = file.filename.strip('.fastq.gz').split('_R1')[0]
                sample_uuid = create_sample(project_uuid, sample_name)
                sample_folder = f"{project_folder}/{sample_uuid}"
                if not os.path.exists(sample_folder):
                    os.makedirs(sample_folder)
                samples.append({'name': sample_name, 'uuid': sample_uuid})
            filepath = os.path.join(sample_folder, file.filename)
            file.save(filepath)
    for sample in samples:
        run_pipeline( sample['name'], sample['uuid'], project_uuid, genes)
        #thread = threading.Thread(target=run_pipeline, args=(sample_name, project_uuid, genes))
        #thread.start()

    return jsonify({
        "message": "Arquivos salvos com sucesso!"
    }), 200

def remove_sample(sample_uuid, base_path):
    project_uuid = get_project_from_sample(sample_uuid)
    remove_sample_from_database(sample_uuid)
    sample_path = f"{base_path}/{project_uuid}/{sample_uuid}"
    if os.path.exists(sample_uuid):
        try:
            shutil.rmtree(sample_path)
            print(f"Diretório '{sample_path}' removido com sucesso.")
        except OSError as e:
            print(f"Erro ao remover o diretório '{sample_path}': {e}")
