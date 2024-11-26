from database.connector import get_db_connection
import uuid

def create_project(project_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    project_uuid = str(uuid.uuid4())

    # Inserir um novo usuário no banco de dados
    cursor.execute("INSERT INTO project (name, uuid) VALUES (%s, %s)", (project_name, project_uuid))
    connection.commit()

    # Fechar a conexão
    cursor.close()
    connection.close()
    return True

def get_all_projects():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, uuid FROM project")
    projects = cursor.fetchall()

    cursor.close()
    connection.close()
    return projects

def get_project(project_uuid):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM project WHERE uuid = %s", (project_uuid,))
    project = cursor.fetchone()

    cursor.close()
    connection.close()
    return project
