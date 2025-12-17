Deployment of the Isolated LLM Service (Ollama + RAG)
This directory contains the Docker Compose configuration to set up the Language Model Generation service (Ollama) and the Vector Database service (ChromaDB), which are essential for integration with Ignition via RAG (Retrieval-Augmented Generation).

The deployment must be performed in two mandatory phases to comply with the requirement of complete isolation from the public internet during operation.

PHASE 1: Model Download (Temporary Internet Access)
The container requires Internet access only once to download the language model (phi3:mini) and store it permanently in the ollama_data volume.

1. Configuration Check
Ensure that, in the docker-compose.yml file, the custom isolated_backend network configuration is commented out for the ollama service:
# In services:ollama:
    networks:
      # - isolated_backend  <-- Must be commented out (or removed) for this phase.
2. Execute and Download
Run Docker Compose to bring up the services. Ollama will use the default Docker bridge network, which allows Internet access for the download.

    docker compose up -d

3. Monitor the Download
Wait until the download is complete. This may take several minutes depending on your connection speed and the model size.

    docker logs llm_service

4. Stop Services
Once the logs indicate that the Ollama server has started and the model is loaded, shut down all services.

    docker compose down

PHASE 2: Isolated Execution (Production Mode)
In this phase, the ollama container will be forced to use the isolated_backend network, which has no valid outbound route to the Internet. The model will be loaded from the local ollama_data volume.

1. Restore the Isolation Configuration
Uncomment the isolated_backend network configuration for the ollama service (and chroma, if used).

YAML

# In services:ollama:
    networks:
      - isolated_backend  <-- Must be UNCOMMENTED for this phase.

2. Execute Isolated
Bring the services back up. The containers are now isolated from the external network but are available to the Ignition Gateway via the mapped ports (11434 and 11743).

docker compose up -d

Connecting to Ignition
The LLM service is now available to the Ignition Gateway on port 11434 (Ollama) or 11743 (ChromaDB), accessible via the IP of the host machine running Docker.

Ollama URL: http://<Host_IP>:11434/api/generate

ChromaDB URL: http://<Host_IP>:11743