import sys
import os
import shutil

sys.path.append('../')

from database.models.sample import get_samples_from_project
from database.models.project import remove_project_from_database
from controller.sample_handler import remove_sample

def remove_project(project_uuid, upload_path, result_path, trimm_path, sheet_path):
    project_samples = get_samples_from_project(project_uuid)
    for sample in project_samples:
        remove_sample(sample['uuid'], upload_path, result_path, trimm_path, sheet_path)

    project_path = f"{upload_path}/{project_uuid}"
    if os.path.exists(project_path):
        try:
            shutil.rmtree(project_path)
            print(f"Diretório '{project_path}' removido com sucesso.")
        except OSError as e:
            print(f"Erro ao remover o diretório '{project_path}': {e}")
    remove_project_from_database(project_uuid)