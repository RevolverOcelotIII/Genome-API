from database.connector import get_db_connection
import uuid

def create_sample(project_uuid, sample_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    sample_uuid = str(uuid.uuid4())

    # Inserir um novo usuário no banco de dados
    cursor.execute("INSERT INTO sample (name, uuid, gene_id, project_id) VALUES (%s, %s, 1, (SELECT id FROM project WHERE uuid = %s))", (sample_name, sample_uuid, project_uuid))
    connection.commit()

    # Fechar a conexão
    cursor.close()
    connection.close()
    return sample_uuid

def remove_sample_from_database(sample_uuid):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM sample WHERE uuid = %s", (sample_uuid,))

    # Commit para aplicar a remoção
    connection.commit()

def get_sample(sample_uuid):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM sample WHERE uuid = %s", (sample_uuid,))
    sample = cursor.fetchone()

    cursor.close()
    connection.close()
    return sample

def get_samples_from_project(project_uuid):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM sample WHERE project_id = (SELECT id FROM project WHERE uuid = %s)", (project_uuid,))
    samples = cursor.fetchall()

    cursor.close()
    connection.close()
    return samples

def get_project_from_sample(sample_uuid):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT project.uuid FROM project inner join sample on project.id = sample.project_id WHERE sample.uuid = %s", (sample_uuid,))
    project_uuid = cursor.fetchone()

    cursor.close()
    connection.close()
    return project_uuid['uuid']

def get_gene_id(gene_name):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT id FROM gene WHERE name = %s", (gene_name,))
    gene = cursor.fetchone()

    cursor.close()
    connection.close()
    return gene['id']