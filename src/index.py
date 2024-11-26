from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from database.models.project import create_project, get_all_projects, get_project
from database.models.sample import create_sample, get_samples_from_project, get_sample
from controller.fastq_addition import add_sample, remove_sample

import os
import json

app = Flask(__name__)

CORS(app)

# Pasta para armazenar os arquivos recebidos
FULL_PATH = '/home/domdeny/src/bioinfo/genome-api/'
UPLOAD_FOLDER = FULL_PATH + 'pipeline/Phenotypes_Finder/dataset/FASTQ'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def root():
    return "ok"

@app.route('/projects/create', methods=['POST'])
def create_project_route():
    data = request.get_json()
    name = data.get('name')
    create_project(name)
    return jsonify({"message": "Project successfully created!"}), 201

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

    return add_sample(f"{app.config['UPLOAD_FOLDER']}/{project_uuid}", project_uuid, files, genes)

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
    samples = get_samples_from_project(sample_uuid)
    
    if samples:
        return jsonify(samples), 200  # Retorna o projeto encontrado
    else:
        return jsonify({"error": "Project not found"}), 404
    

# Endpoint para download de arquivos
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Arquivo não encontrado"}), 404
    
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
