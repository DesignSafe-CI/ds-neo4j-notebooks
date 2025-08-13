import neo4j
from .config import EMBEDDING_MODEL
from .embedding import get_embedding, oai_client


def ingest_entity(driver: neo4j.Driver, uuid: str, title: str, description: str, **kwargs):
    """
    Ingest an entity in neo4j. Its properties will be the provided uuid/title/description
    and any other provided kwargs. If 'name' is provided it will be used as an additional label
    """
    label = ":Entity"
    # Replacing spaces & periods with underscores
    if 'name' in kwargs and kwargs["name"]:
        cleaned_name = '_'.join(kwargs['name'].split()).replace('.', '_')
        label += f":{cleaned_name}"

    extra_fields = [f"{k}: ${k}" for k in kwargs]
    extra_fields_str = ""
    if extra_fields:
        extra_fields_str = ", " + ", ".join(extra_fields)
    add_entity_query = \
    f"""
    MERGE (e{label} {{uuid: $uuid}})
    SET e = {{uuid: $uuid}} // Allow properties to be unset with subsequent calls
    SET e += {{ title: $title,
                description: $description
                {extra_fields_str}
             }}
    """
    driver.execute_query(add_entity_query, uuid=uuid, title=title, description=description, **kwargs)

    description_chunks = description.split(". ")
    to_embed = [title, *description_chunks] + [kwargs[key] for key in kwargs]
    for e in to_embed:
        embedding = get_embedding(oai_client, e, EMBEDDING_MODEL)
        embedding_query = """
        MATCH (ent:Entity {uuid: $uuid})
        MERGE (ent)-[:HAS_EMBEDDING]->(:Embedding {text: $text, embedding: $embedding})
        """
        driver.execute_query(embedding_query, uuid=uuid, text=e, embedding=embedding)




def ingest_entity_rel(driver: neo4j.Driver, parent_uuid: str, child_uuid: str, order: int=0):
    """
    Create a :HAS_CHILD relationship in the graph between 2 nodes given their UUIDs
    """
    add_rel_query = \
    """
    MATCH (parent:Entity {uuid: $parent_uuid})
    WITH parent
    MATCH(child: Entity {uuid: $child_uuid})
    MERGE (parent)-[:HAS_CHILD {order: $order}]->(child)
    """
    driver.execute_query(add_rel_query, parent_uuid=parent_uuid, child_uuid=child_uuid, order=order)


def ingest_file(driver: neo4j.Driver, file_info: dict):
    """
    Ingest a file in Neo4j using file_info.
    File's path as its unique identifier.
    """
    file_path = file_info.get("path")
    merge_query = """
    MERGE (f:File {path: $file_path})
    SET f.name = $file_name,
        f.type = $file_type,
        f.length = $file_length,
        f.system = $file_system,
        f.lastModified = $file_last_modified
    """
    driver.execute_query(
        merge_query,
        file_path=file_path,
        file_name=file_info.get("name"),
        file_type=file_info.get("type"),
        file_length=file_info.get("length"),
        file_system=file_info.get("system"),
        file_last_modified=file_info.get("lastModified")
    )

    to_embed = [file_info.get("name")]
    for e in to_embed:
        embedding = get_embedding(oai_client, e, EMBEDDING_MODEL)
        embedding_query = """
        MATCH (ent:File {path: $file_path})
        MERGE (ent)-[:HAS_EMBEDDING]->(:Embedding {text: $text, embedding: $embedding})
        """
        driver.execute_query(embedding_query, file_path=file_path, text=e, embedding=embedding)

def ingest_entity_file_rel(driver: neo4j.Driver, entity_uuid: str, file_path: str):
    """
    Create a relationship from an entity node to a file node.
    """
    query = """
    MATCH (e:Entity {uuid: $entity_uuid})
    MATCH (f:File {path: $file_path})
    MERGE (e)-[:HAS_FILE]->(f)
    """
    driver.execute_query(query, entity_uuid=entity_uuid, file_path=file_path)


def ingest_person(driver: neo4j.Driver, person_data: dict):
    """
    Create or update a :Person node based on unique person identifier.
    Using email as unique identifier.
    """
    unique_id = person_data.get("email")

    merge_person_query = """
    MERGE (p:Person {personId: $unique_id})
    SET p.inst = $inst,
        p.email = $email,
        p.fname = $fname,
        p.lname = $lname,
        p.username = $username
    """
    driver.execute_query(
        merge_person_query,
        unique_id=unique_id,
        inst=person_data.get("inst"),
        email=person_data.get("email"),
        fname=person_data.get("fname"),
        lname=person_data.get("lname"),
        username=person_data.get("username")
    )

    to_embed = [f'Author with name {person_data.get("fname")} {person_data.get("lname")} at {person_data.get("inst")}']
    for e in to_embed:
        embedding = get_embedding(oai_client, e, EMBEDDING_MODEL)
        embedding_query = """
        MATCH (ent:Person {personId: $unique_id})
        MERGE (ent)-[:HAS_EMBEDDING]->(:Embedding {text: $text, embedding: $embedding})
        """
        driver.execute_query(embedding_query, unique_id=unique_id, text=e, embedding=embedding)

def ingest_entity_person_rel(driver: neo4j.Driver, entity_uuid: str, person_data: dict, source: str):
    """
    Create a :CONTRIBUTED relationship from an Entity node to a Person node.
    Stores the person's role (e.g., "pi", "co_pi", etc.) and the source array ("users" or "authors").
    """
    unique_id = person_data.get("email")
    contrib_query = """
    MATCH (e:Entity {uuid: $entity_uuid})
    MATCH (p:Person {personId: $unique_id})
    MERGE (e)-[r:HAS_CONTRIBUTOR {role: $role, source: $source}]->(p)
    """
    driver.execute_query(
        contrib_query,
        entity_uuid=entity_uuid,
        unique_id=unique_id,
        role=person_data.get("role"),
        source=source
    )


def ingest_facility(driver:neo4j.Driver, facility_info: dict):
    """
    Ingest a facility node in Neo4j using facility_info.
    Uses the facility 'name' as the unique identifier.
    """
    facility_id = facility_info.get("id")
    facility_name = facility_info.get("name")

    merge_query = """
    MERGE (fac:Facility {name: $facility_name})
    SET fac.facilityId = $facility_id
    """

    driver.execute_query(
        merge_query,
        facility_name=facility_name,
        facility_id=facility_id
    )

    to_embed = [f'Facility {facility_name}']
    for e in to_embed:
        embedding = get_embedding(oai_client, e, EMBEDDING_MODEL)
        embedding_query = """
        MATCH (ent:Facility {name: $facility_name})
        MERGE (ent)-[:HAS_EMBEDDING]->(:Embedding {text: $text, embedding: $embedding})
        """
        driver.execute_query(embedding_query, facility_name=facility_name, text=e, embedding=embedding)


def ingest_entity_facility_rel(driver: neo4j.Driver, entity_uuid:str, facility_info:dict):
    """
    Create a relationship from an Entity node to a Facility node.
    The relationship is labeled :HAS_FACILITY.
    """
    facility_name = facility_info.get("name")
    query = """
    MATCH (e:Entity {uuid: $entity_uuid})
    MATCH (fac:Facility {name: $facility_name})
    MERGE (e)-[:HAS_FACILITY]->(fac)
    """

    driver.execute_query(query, entity_uuid=entity_uuid, facility_name=facility_name)
