import neo4j

def setup_db(driver: neo4j.Driver):
    """Create constraints/indices for DesignSafe entities"""
    driver.execute_query("""
    CREATE INDEX entity_uuid IF NOT EXISTS FOR (e:Entity) ON e.uuid
    """)
    # Vector index for embeddings
    driver.execute_query("""
    CREATE VECTOR INDEX designsafeEmbeddings IF NOT EXISTS
    FOR (e:Embedding)
    ON e.embedding OPTIONS { indexConfig: {
         `vector.dimensions`: 1536,
         `vector.similarity_function`: 'cosine'
    }}
    """)

def cleanup_db(driver: neo4j.Driver):
    """Clear all entries in the database"""
    driver.execute_query("MATCH (n) DETACH DELETE n")
