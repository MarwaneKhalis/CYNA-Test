# CYNA Technical Test
### Log Analyzer

This project simulates a real-time monitoring tool for network security logs (IDS - Intrusion Detection System).


## How the system works:

- Generation: Continuous, high-speed creation of IDS logs.

- Enrichment: On-the-fly cross-referencing of IP addresses with the Ipsum list to identify malicious traffic.

- Storage: Sending and indexing the enriched logs in ElasticSearch.

- Monitoring: Real-time tracking and analysis using a Kibana dashboard.


## Setup

Now let's see how to setup my solution. 
The first step is to download the whole project from github, then open a terminal and go to the root of the project.
Next we have to run some commands: 
- "docker-compose up -d" to setup ElasticSearch and Kibana
- "python -m venv venv" if you want to use a virtual environnement, assuming you already have python on your machine.
- "venv\scripts\activate.bat" to use the environnement.
- "pip install -r requirements.txt" to install the required libraries.

You should now be able to run the main file without any problem : "python main.py"  (in the terminal).
Once the process has started, go to Kibana (http://localhost:5601) > Stack Management > Saved Objects.

Click Import and upload dashboard.ndjson.


## Architectural choices

* **Python vs. Logstash:** I originally intended to use Logstash. However, due to strict time (imitating a fast real-time stream) and spatial constraints (ensuring the process runs smoothly on 8GB of RAM), I needed precise control over resource consumption. I ultimately chose Python because I felt more comfortable managing the complexity to respect these limits efficiently.
* **Elasticsearch & Kibana:** I chose this stack for its high convenience—Elasticsearch seamlessly handles fast data indexing, and Kibana allows for instant, dynamic dashboard creation without coding a custom frontend. Most importantly, I specifically chose to learn and build with these tools because I know it is the stack I will be using if I join CYNA.









