import os
from neo4j import GraphDatabase

EMBEDDING_MODEL = "text-embedding-ada-002"
LARGE_EMBEDDING_MODEL = "text-embedding-3-large"
PUB_LISTING_URL = "https://www.designsafe-ci.org/api/publications/v2"
NEO4J_URI = os.environ.get("NEO4J_URI")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")

#for local connection with repo, change NEO4J_URI in env to neo4j://localhost:7687
def get_neo4j_driver():
    """
    Create and return a Neo4j driver instance with customizable configuration
    """

    auth = (NEO4J_USERNAME, NEO4J_PASSWORD)
    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=auth,
        #additional settings
    )

    return driver
