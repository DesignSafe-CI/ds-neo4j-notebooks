# Jupyter Notebooks for DesignSafe Neo4j Integration
## Overview
This repository contains Jupyter notebooks for translating DesignSafe publications into 
Neo4J graphs. These notebooks are meant for development work targeting a local Neo4j database, 
and will serve as the foundation for a more robust ETL pipeline for publications.

## Running the Notebooks
This repository uses uv to manage dependencies. Instructions on how to install uv can be found at https://docs.astral.sh/uv/getting-started/installation/

To get started with local development:
1. Navigate to the repository root.
2. Copy the contents of `dev.env.sample` to `dev.env` (`cp dev.env.sample dev.env`) and set any secret variables, such as openAI keys.
3. Run `docker compose up` to start the Neo4j instance
4. Run `uv run --env-file=dev.env --with jupyter jupyter lab` to open Jupyter
5. Navigate to the `pub_ingest.ipynb` notebook in the Jupyter browser window that opens.
6. Navigate to http://localhost:7474/browser/ and connect to the database at `neo4j://localhost:7687` with "No Authentication Type" selected.

## References
- Neo4j Python driver manual: https://neo4j.com/docs/python-manual/current/
- NetworkX reference: https://networkx.org/documentation/stable/reference/index.html