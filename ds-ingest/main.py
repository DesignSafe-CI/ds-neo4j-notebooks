from .config import get_neo4j_driver, NEO4J_URI
from .utils import setup_db
from .api import iterate_publications
from .ingestion import ingest_publication

def main():
    with get_neo4j_driver() as driver:
        setup_db(driver)

    #Ingesting all datasets
    with get_neo4j_driver() as driver:
        for pub_json in iterate_publications():
            project_id = (pub_json.get("baseProject", {}).get("projectId"))

            print(f"Ingesting publication: {project_id} - {pub_json.get('baseProject', {}).get('title', '')}")
            ingest_publication(pub_json, driver)
            print(f"Finished ingesting project: {project_id} =========================")

    #Ingesting a certain amount of datasets
    # import itertools
    # count = 2
    # with get_neo4j_driver() as driver:
    #     for pub_json in itertools.islice(iterate_publications(), count):
    #         project_id = (pub_json.get("baseProject", {}).get("projectId"))

    #         print(f"Ingesting publication: {project_id} - {pub_json.get('baseProject', {}).get('title', '')}")
    #         ingest_publication(pub_json, driver)
    #         print(f"Finished ingesting project: {project_id} =========================")

    # print("Completed ingesting first", count, "publications =======================")

if __name__ == "__main__":
    main()
