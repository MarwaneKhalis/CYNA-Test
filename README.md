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

- **Python vs. Logstash:** I originally intended to use Logstash. However, due to strict time (imitating a fast real-time stream) and spatial constraints (ensuring the process runs smoothly on 8GB of RAM), I needed precise control over resource consumption. I ultimately chose Python because I felt more comfortable managing the complexity to respect these limits efficiently.
- **ElasticSearch & Kibana:** I chose this stack for its high convenience. ElasticSearch seamlessly handles fast data indexing, and Kibana allows for instant, dynamic dashboard creation. Most importantly, I specifically chose to learn and build with these tools because I know it is the stack I will be using if I join CYNA.


## Achievements: What Works?

- Continuous Real-Time Pipeline: The system successfully tails, parses, and enriches a high-speed stream of IDS logs without crashing.

- Efficient Enrichment: The in-memory lookup against the Ipsum threat list allows for lightning-fast threat detection without slowing down the ingestion.

- Optimized Ingestion: Implemented Elasticsearch bulk API batching to handle the massive log volume and eliminate network bottlenecks.


## Dashboard Insights

The Kibana dashboard provides an immediate, real-time SOC view:

- The total volume of processed network logs versus detected threats.

- A temporal timeline of attacks to quickly spot activity spikes.

- A ranked list of the most aggressive malicious IPs (Threat Level & Occurrence) to prioritize incident response.


## Challenges & Compromises

The rarity of attacks: The generator creates random IP addresses (4.3 billion possibilities) against an Ipsum list of ~50,000 IPs. 
It takes time to see a "Malicious IP" pop up on the dashboard. It wasn't until the 65 000 log integrated by ES that I had my first malicious IP. I chose to let the pipeline run naturally instead of hardcoding fake malicious entries to prove the logic works on a true random data stream.

 Other challenge: I'm used to building dashboards on Power BI so Kibana felt really bad to manipulate at least for the the first hour. I would be ashamed to say how long I spent trying to move each visuals around the board to where I wanted them.



##  Thank you ! 

Thank you for taking the time to review my work. I didn't really go into details about the role of each files to avoid making this too long, so I look forward to discussing my technical choices with you and, hopefully, joining the CYNA team!





