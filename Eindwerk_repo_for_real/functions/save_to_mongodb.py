from pymongo import MongoClient
from uuid import UUID
from dotenv import load_dotenv
import os

# Laad .env bestand
load_dotenv()

# Verbind met MongoDB
uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

# Gebruik database 'powerlink' en collectie 'projects'
db = client["powerlink"]
projects_collection = db["projects"]

def save_project_to_mongodb(projectname, data_comps, data_lines):
    # Serialiseer componenten
    serialized_comps = []
    for comp in data_comps:
        comp_data = comp.__dict__.copy()
        if isinstance(comp_data.get('id'), UUID):
            comp_data['id'] = str(comp_data['id'])
        comp_data['class_name'] = comp.__class__.__name__
        serialized_comps.append(comp_data)

    # Serialiseer verbindingen
    serialized_connections = []
    for conn in data_lines:
        conn_data = conn.__dict__.copy()
        if isinstance(conn_data.get('id'), UUID):
            conn_data['id'] = str(conn_data['id'])
        conn_data['class_name'] = conn.__class__.__name__
        serialized_connections.append(conn_data)

    # Maak document
    project_document = {
        "projectname": projectname,
        "components": serialized_comps,
        "connections": serialized_connections,
        "user_id": None,
        "group_id": None
    }

    # Voeg toe aan MongoDB
    try:
        result = projects_collection.insert_one(project_document)
        print(f"✅ Project '{projectname}' opgeslagen in MongoDB met ID: {result.inserted_id}")
    except Exception as e:
        print(f"❌ Fout bij MongoDB-opslag: {e}")
