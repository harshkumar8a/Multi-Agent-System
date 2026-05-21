# Multi-Agent AI System for Web Research



<p align="center">
  <img src="assest\video.gif" width="400" alt="Alt Text">
</p>

This repository contains a Multi-Agent AI System designed for automated web research and data extraction. By combining the search capabilities of Tavily with the precision of BeautifulSoup, the system can autonomously find relevant topics and scrape detailed information to provide comprehensive insights.

## Project Structure

        MULTI-AGENT-SYSTEM/
        │
        ├── .venv/
        │
        ├── src/
        │   ├── __pycache__/
        │   │
        │   ├── config/
        │   │
        │   ├── graph/
        │   │   ├── __pycache__/
        │   │   ├── __init__.py
        │   │   ├── nodes.py
        │   │   ├── state.py
        │   │   └── workflow.py
        │   │
        │   ├── observability/
        │   │   ├── __pycache__/
        │   │   ├── __init__.py
        │   │   ├── evaluators.py
        │   │   ├── logging_config.py
        │   │   └── metrics.py
        │   │
        │   ├── prompts/
        │   │   ├── __pycache__/
        │   │   ├── __init__.py
        │   │   ├── critic_prompt.py
        │   │   └── writer_prompt.py
        │   │
        │   └── tools/
        │
        ├── __init__.py
        ├── .env
        ├── .gitignore
        ├── .python-version
        ├── app.py
        ├── pyproject.toml
        ├── README.md
        ├── tools.py
        └── uv.lock
    




## Key Technical Components

1. **Tavily Search Tool**: Used by the primary agent to perform high-quality, AI-optimized searches to retrieve names and URLs related to a specific query.

2. **Scraping Tool (BeautifulSoup)**: A secondary tool that processes the URLs found by Tavily to extract clean, structured content from the web pages.

3. **Agentic Pipeline**: A sophisticated orchestration layer that manages the flow of information between the tools and the reasoning engine.

4. **Streamlit UI**: A clean, interactive front-end for users to input queries and visualize the agent's research process in real-time.

5. **UV Environment**: Managed using uv for lightning-fast, reproducible python environment management.

6. **Observability**: Use for tell me performance of the Agent like latency, metrics, hallucination, etc.





## Setup and Installation
This project uses uv for environment and dependency management.

Clone the repository:

Bash

    git clone https://github.com/harshkumar8a/Multi-Agent-System.git
    cd multi-agent-researcher

Install dependencies:

Bash

    uv init
    .venv\Scripts\activate
    uv sync

Configure API Keys:

Create a .env file and add your credentials:

    TAVILY_API_KEY = "Tavily-api-key"

    LANGCHAIN_API_KEY="API_KEY"
    LANGCHAIN_PROJECT="Project-Name"
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

    # ── Local model (Ollama) ────────────────────────────────────────────────────────
    # Install Ollama: https://ollama.ai
    # Pull model:     ollama pull llama3.2
    OLLAMA_BASE_URL=http://localhost:11434
    OLLAMA_MODEL="Model-Name"

Run the application:

    streamlit run app.py


# Connect to me 

**Name**: Harsh Kumar

**Email**: [Link](harshkumar811h@gmail.com)

**LinkedIn**: [Link](https://www.linkedin.com/in/harshkumar-8h/)
