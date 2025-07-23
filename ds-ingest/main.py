from neo4j import GraphDatabase, RoutingControl
from .config import NEO4J_URI
from .utils import setup_db
from .api import iterate_publications
from .ingestion import ingest_publication

def main():
    with GraphDatabase.driver(NEO4J_URI) as driver:
        setup_db(driver)

    #Ingesting all datasets
    with GraphDatabase.driver(NEO4J_URI) as driver:
        for pub_json in iterate_publications():
            project_id = (pub_json.get("baseProject", {}).get("projectId"))

            print(f"Ingesting publication: {project_id} - {pub_json.get('baseProject', {}).get('title', '')}")
            ingest_publication(pub_json, driver)
            print(f"Finished ingesting project: {project_id} =========================")



    #Ingesting a certain amount of datasets
    # import itertools
    # count = 10
    # with GraphDatabase.driver(NEO4J_URI) as driver:
    #     for pub_json in itertools.islice(iterate_publications(), count):
    #         project_id = (pub_json.get("baseProject", {}).get("projectId"))

    #         print(f"Ingesting publication: {project_id} - {pub_json.get('baseProject', {}).get('title', '')}")
    #         ingest_publication(pub_json, driver)
    #         print(f"Finished ingesting project: {project_id} =========================")

    # print("Completed ingesting first", count, "publications =======================")

if __name__ == "__main__":
    main()
