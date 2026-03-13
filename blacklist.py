import requests

def load_ipsum_feed(url="https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt"):
    """
    Télécharge la liste Ipsum depuis GitHub et la charge en mémoire.
    Retourne un dictionnaire : { 'Adresse_IP': Niveau_de_confiance }
    """
    print("Téléchargement de la liste des IP malveillantes (Ipsum)...")
    malicious_ips = {}
    


    try:
        # On ajoute un timeout de 10 secondes pour ne pas bloquer le script indéfiniment
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Déclenche une erreur si le téléchargement rate
        
        # On lit le texte ligne par ligne
        for line in response.text.splitlines():
            # On ignore les lignes vides et les commentaires
            if not line.strip() or line.startswith("#"):
                continue
            
            # Dans le fichier, l'IP et le niveau sont séparés par un espace ou une tabulation
            parts = line.split()
            if len(parts) >= 2:
                ip = parts[0]
                level = int(parts[1])
                
                # On stocke dans le dictionnaire
                malicious_ips[ip] = level
                
        print(f"Liste chargée avec succès : {len(malicious_ips)} IP malveillantes prêtes en mémoire.")
        return malicious_ips
        

    except requests.exceptions.RequestException as e:
        print(f" Erreur réseau lors du téléchargement de la liste Ipsum : {e}")
        print(" Le script va continuer, mais sans enrichissement (les logs passeront normaux).")
        return {} # On retourne un dictionnaire vide pour ne pas faire planter la suite

#TEST

if __name__ == "__main__":
    ips = load_ipsum_feed()
    if ips:
        sample_ip = list(ips.keys())[0]
        print(f"Exemple -> IP: {sample_ip}, Niveau de menace: {ips[sample_ip]}")