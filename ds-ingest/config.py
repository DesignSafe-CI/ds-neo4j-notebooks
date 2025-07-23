import os

EMBEDDING_MODEL = "text-embedding-ada-002"
LARGE_EMBEDDING_MODEL = "text-embedding-3-large"
PUB_LISTING_URL = "https://www.designsafe-ci.org/api/publications/v2"
NEO4J_URI = os.environ.get("NEO4J_URI", "neo4j://localhost:7687")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
