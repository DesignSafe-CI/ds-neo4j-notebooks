import os
from neo4j import GraphDatabase

URI = os.environ.get("NEO4J_URI")
username = os.environ.get("NEO4J_USERNAME")
password = os.environ.get("NEO4J_PASSWORD")

print(f"URI: {URI}")
print(f"Username: {username}")
print(f"Password: {'*' * len(password) if password else 'None'}")

try:
    driver = GraphDatabase.driver(URI, auth=(username, password))
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        print("Connection successful!")
        print(result.single()["test"])
    driver.close()
except Exception as e:
    print(f"Connection failed: {e}")


