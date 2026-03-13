import time
import re
import subprocess
import sys
from datetime import datetime
from elasticsearch.helpers import bulk
from blacklist import load_ipsum_feed 
from ES_connect import get_es_client, setup_index, INDEX_NAME

GENERATOR_DIR = "Security-Log-Generator-main"
LOG_FILE_PATH = f"{GENERATOR_DIR}/logs/ids.log"

# Expression permettant de "traduire" les logs
LOG_PATTERN = re.compile(r"^(?P<timestamp>.*?) - (?P<logger>.*?) - (?P<severity>.*?) - (?P<proto>.*?) - (?P<src_ip>.*?):(?P<src_port>\d+) --> (?P<dest_ip>.*?):(?P<dest_port>\d+) - (?P<flag>.*?) - (?P<message>.*)$")


# On applique le paterne aux logs pour en faire des dictionnaires
def parse_line(line):
    match = LOG_PATTERN.match(line.strip())
    if match:
        return match.groupdict()
    return None

def lire_fichier_en_continu(filepath):
    with open(filepath, 'r') as f:
        while True:
            ligne = f.readline()
            if not ligne:
                time.sleep(0.1)
                continue
            yield ligne

def main():
    malicious_ips = load_ipsum_feed()
    es = get_es_client()
    if not es: return
    setup_index(es)
    
    # Lancement des générateurs
    processus = [subprocess.Popen([sys.executable, "main.py"], cwd=GENERATOR_DIR) for _ in range(3)]
    
    batch_size = 1000          # Modulable, choisi 1000 pour limiter le nombres d'opérations et gagner en performance
    logs_batch = []
    
    print(f"Analyse et ingestion du fichier IDS en cours...")
    
    try:
        for ligne in lire_fichier_en_continu(LOG_FILE_PATH):
            log_data = parse_line(ligne)
            if log_data:

                # 1. Correction de la date vers @timestamp

                raw_date = log_data["timestamp"].replace(',', '.')
                try:
                    dt = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S.%f")
                    log_data["@timestamp"] = dt.isoformat() + "+01:00"
                except Exception:
                    log_data["@timestamp"] = datetime.utcnow().isoformat()

                
                # Suppression de l'ancien timestamp

                del log_data["timestamp"]

            
                # 2. Enrichissement des logs avec la liste IPsum

                ip = log_data["src_ip"]
                if ip in malicious_ips:
                    log_data["is_malicious"] = True
                    log_data["threat_level"] = malicious_ips[ip]
                else:
                    log_data["is_malicious"] = False

                logs_batch.append({"_index": INDEX_NAME, "_source": log_data})
                
                if len(logs_batch) >= batch_size:
                    bulk(es, logs_batch)
                    print(f" {len(logs_batch)} logs structurés et envoyés.")
                    logs_batch.clear()
                    
    except KeyboardInterrupt:
        print("\nArrêt propre")
    finally:
        if logs_batch:
            bulk(es, logs_batch)
        for p in processus:
            p.terminate()

if __name__ == "__main__":
    main()