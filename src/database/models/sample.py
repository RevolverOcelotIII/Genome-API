from database.connector import get_db_connection
import uuid

def create_sample(project_uuid, sample_name, genes):
    connection = get_db_connection()
    cursor = connection.cursor()

    sample_uuid = str(uuid.uuid4())

    # Inserir uma nova amostra no banco de dados
    cursor.execute("INSERT INTO sample (name, uuid, project_id) VALUES (%s, %s, (SELECT id FROM project WHERE uuid = %s))", (sample_name, sample_uuid, project_uuid))
    connection.commit()
    sample_id = cursor.lastrowid
    print(sample_id)
    for gene in genes:
        gene_id = get_gene_id(gene)
        cursor.execute("INSERT INTO gene_x_sample (sample_id, gene_id) VALUES (%s, %s)", (sample_id, gene_id))
    connection.commit()
    # Fechar a conexão
    cursor.close()
    connection.close()
    return sample_uuid

def remove_sample_from_database(sample_uuid):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM gene_x_sample WHERE sample_id = (select id from sample where uuid = %s)", (sample_uuid,))
    cursor.execute("DELETE FROM sample WHERE uuid = %s", (sample_uuid,))

    # Commit para aplicar a remoção
    connection.commit()

def edit_sample_name(sample_uuid, sample_name):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE sample SET name=%s WHERE uuid = %s", (sample_name, sample_uuid,))

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

def get_sample_genes(sample_uuid):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT gene.name FROM gene inner join gene_x_sample on gene_x_sample.gene_id = gene.id inner join sample on gene_x_sample.sample_id = sample.id WHERE sample.uuid=%s", (sample_uuid,))
    genes = cursor.fetchall()

    cursor.close()
    connection.close()
    return genes

def update_sample_process(sample_uuid, state):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE sample SET state=%s WHERE uuid = %s", (state, sample_uuid,))

    # Commit para aplicar a remoção
    connection.commit()