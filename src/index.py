import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from database.models.project import create_project, get_all_projects, get_project, edit_project_name
from database.models.sample import get_samples_from_project, edit_sample_name
from controller.sample_handler import add_sample, remove_sample, get_sample_info
from controller.project_handler import remove_project
from controller.download_files import download_file
sys.path.append('../')
from config import ROOT_PATH

import os
import json

app = Flask(__name__)

CORS(app)

print(ROOT_PATH)
# Pasta para armazenar os arquivos recebidos
UPLOAD_FOLDER = ROOT_PATH + 'pipeline/Phenotypes_Finder/dataset/FASTQ'
RESULT_FOLDER = ROOT_PATH + 'pipeline/Phenotypes_Finder/result/Trimmomatic'
TRIMM_FOLDER = ROOT_PATH + 'pipeline/Phenotypes_Finder/result/Trimmomatic/trimmed'
SHEET_FOLDER = ROOT_PATH + 'pipeline/Phenotypes_Finder/result/SNP_Sheet'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def root():
    return "ok"

@app.route('/projects/create', methods=['POST'])
def api_create_project():
    data = request.get_json()
    name = data.get('name')
    create_project(name)
    return jsonify({"message": "Project successfully created!"}), 201

@app.route('/projects/edit', methods=['POST'])
def api_edit_project():
    data = request.get_json()
    project_name = data.get('name')
    project_uuid = data.get('uuid')
    edit_project_name(project_uuid, project_name)
    return jsonify({"message": "Project successfully edited!"}), 201

@app.route('/projects/remove/<string:project_uuid>', methods=['DELETE'])
def api_remove_project(project_uuid):
    # Procura o projeto com o UUID fornecido
    remove_project(project_uuid, UPLOAD_FOLDER, RESULT_FOLDER, TRIMM_FOLDER, SHEET_FOLDER)
    
    return jsonify({"message": "Sample successfully removed!"}), 201

@app.route('/projects/get-all', methods=['GET'])
def api_get_all_projects():
    return jsonify(get_all_projects())

@app.route('/projects/<string:project_uuid>', methods=['GET'])
def api_get_project(project_uuid):
    # Procura o projeto com o UUID fornecido
    project = get_project(project_uuid)
    
    if project:
        return jsonify(project), 200  # Retorna o projeto encontrado
    else:
        return jsonify({"error": "Project not found"}), 404

# Endpoint para envio de arquivos
@app.route('/fastq/upload/<project_uuid>', methods=['POST'])
def upload_fastq(project_uuid):
    if 'files[]' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    json_data = request.form.get('json_data')
    if not json_data:
        return jsonify({"error": "JSON data is missing"}), 400

    json_data = json.loads(json_data)  # Converte de string para um dicionário
    genes = json_data.get('genes')    # Campo genes
    is_sra = json_data.get('isSRA')
    files = request.files.getlist('files[]')

    return add_sample(f"{UPLOAD_FOLDER}/{project_uuid}", project_uuid, files, genes, is_sra)

@app.route('/samples/<string:project_uuid>', methods=['GET'])
def api_get_samples_from_project(project_uuid):
    # Procura o projeto com o UUID fornecido
    samples = get_samples_from_project(project_uuid)
    
    if samples:
        return jsonify(samples), 200  # Retorna o projeto encontrado
    else:
        return jsonify({"error": "Project not found"}), 404

@app.route('/samples/remove/<string:sample_uuid>', methods=['DELETE'])
def api_remove_sample(sample_uuid):
    # Procura o projeto com o UUID fornecido
    remove_sample(sample_uuid, UPLOAD_FOLDER, RESULT_FOLDER, TRIMM_FOLDER, SHEET_FOLDER)
    
    return jsonify({"message": "Sample successfully removed!"}), 201

@app.route('/samples/edit', methods=['POST'])
def api_edit_sample():
    data = request.get_json()
    sample_name = data.get('name')
    sample_uuid = data.get('uuid')
    edit_sample_name(sample_uuid, sample_name)
    return jsonify({"message": "Sample successfully edited!"}), 201

@app.route('/samples/info/<string:sample_uuid>', methods=['GET'])
def api_get_sample_info(sample_uuid):
    # Procura o projeto com o UUID fornecido
    sample_data = get_sample_info(sample_uuid)
    
    if sample_data:
        return jsonify(sample_data), 200  # Retorna o projeto encontrado
    else:
        return jsonify({"error": "Error processing sample"}), 404
    

# Endpoint para download de arquivos
@app.route('/samples/download/<string:sample_uuid>/<string:gene>/<string:filename>', methods=['GET'])
def api_download_file(sample_uuid, gene, filename):
    file = download_file(filename, sample_uuid, gene)
    print(file['path'])
    print(file['file_name'])
    
    return send_file(file['path'], as_attachment=True, download_name=file['file_name'])

if __name__ == '__main__':
    app.run(debug=True)
