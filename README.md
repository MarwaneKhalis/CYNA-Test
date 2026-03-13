# CYNA Technical Test
## Log Analyzer

This project simulates a real-time monitoring tool for network security logs (IDS - Intrusion Detection System).

## How the system works:

-Generation: Continuous, high-speed creation of IDS logs.

-Enrichment: On-the-fly cross-referencing of IP addresses with the Ipsum list to identify malicious traffic.

-Storage: Sending and indexing the enriched logs in ElasticSearch.

-Monitoring: Real-time tracking and analysis using a Kibana dashboard.

## Setup

Now let's see how to setup my solution. 
The first step is to download the whole project from github, then open a terminal and go to the root of the project.
Next we have to run some commands : 
-"docker-compose up -d" to setup ElasticSearch and Kibana
-"python -m venv venv" if you want to use a virtual environnement, assuming you already have python on your machine.
-"venv\scripts\activate.bat" to use the environnement.
-"pip install -r requirements.txt" to install the required libraries.

You should now be able to run the main file without any problem : "python main.py"  (in the terminal).
Once the process has started, go to Kibana (http://localhost:5601) > Stack Management > Saved Objects.

Click Import and upload dashboard.ndjson.
