from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
import time

# Le nom de notre "table" dans Elasticsearch
INDEX_NAME = "cyna-security-logs"

def get_es_client():
    
    # On crée et retourne la connexion à ElasticSearch.
    
    
    print("⏳ Tentative de connexion à Elasticsearch...")
    
    # On se connecte à notre conteneur local
    es = Elasticsearch("http://127.0.0.1:9200")
    
    # Petite boucle de vérification pour s'assurer qu'ES est bien démarré
    for i in range(5):
        try:
            es.info()
            print("✅ Connecté à Elasticsearch avec succès !")
            return es
        except Exception as e:
            print(f"⚠️ Tentative {i + 1}/5 échouée.")
            # 🔍 LA LIGNE MAGIQUE POUR COMPRENDRE LE PROBLÈME :
            print(f"🔍 Détail de l'erreur : {e}") 
            time.sleep(5)
            
    print("❌ Impossible de se connecter à Elasticsearch. Vérifiez que le conteneur Docker tourne.")
    return None

def setup_index(es):

    #On crée l'index et définit le 'Mapping' (le typage des données).
    
    mapping = {
        "mappings": {
            "properties": {
                # Les champs standards qu'on va générer
                "@timestamp": {"type": "date"},
                "log_type": {"type": "keyword"}, # keyword = idéal pour filtrer (ex: Web, IDS, Endpoint)
                "message": {"type": "text"},
                
                
                # Les champs d'enrichissement (Threat Intel)
                "is_malicious": {"type": "boolean"},
                "threat_level": {"type": "integer"}
            }
        }
    }

    # On vérifie si l'index existe déjà 
    if not es.indices.exists(index=INDEX_NAME):
        print(f"🏗️ Création de l'index '{INDEX_NAME}' avec son mapping strict...")
        es.indices.create(index=INDEX_NAME, body=mapping)
        print("✅ Index créé !")
    else:
        print(f"ℹ️ L'index '{INDEX_NAME}' existe déjà, on le réutilise.")


#TEST


if __name__ == "__main__":
    client = get_es_client()
    if client:
        setup_index(client)