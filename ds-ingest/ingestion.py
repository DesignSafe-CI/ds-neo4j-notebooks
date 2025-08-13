import networkx as nx
from .objects import ingest_entity, ingest_facility, ingest_entity_facility_rel, ingest_file, ingest_entity_file_rel, ingest_person, ingest_entity_person_rel, ingest_entity_rel

def ingest_publication(pub_json, driver):
    project_id = (pub_json.get("baseProject", {}).get("projectId"))
    pub_tree = nx.tree_graph(pub_json['tree'])
    for node in pub_tree.nodes:
        node_data = pub_tree.nodes[node]
        if not node_data.get("value"):
            continue
        title = node_data["value"]["title"]
        if node == "NODE_ROOT":
            uuid = project_id
        else:
            uuid = node
        name = node_data["name"]
        meta_uuid = node_data["uuid"]
        description = node_data["value"].get("description", None)
        other_fields = {k: str(node_data["value"][k]) for k in node_data["value"] if node_data["value"][k] and k not in ["title", "description"]}
        ingest_entity(driver, uuid, title, description, name=name, meta_uuid=meta_uuid, **other_fields)

        fac = node_data["value"].get("facility")
        facs = node_data["value"].get("facilities", [])
        facilities = []
        if fac:
            facilities.append(fac)
        facilities.extend(facs)

        for facility_info in facilities:
            ingest_facility(driver, facility_info)
            ingest_entity_facility_rel(driver, uuid, facility_info)

        file_objs = node_data["value"].get("fileObjs", [])
        for file_info in file_objs:
            ingest_file(driver, file_info)
            ingest_entity_file_rel(driver, uuid, file_info["path"])

        users = node_data["value"].get("users", [])
        for user in users:
            ingest_person(driver, user)
            ingest_entity_person_rel(driver, uuid, user, source="users")

        authors = node_data["value"].get("authors", [])
        for author in authors:
            ingest_person(driver, author)
            ingest_entity_person_rel(driver, uuid, author, source="authors")

        # for ev in node_data["value"].get("nhEvents", []):
        #     ingest_hazard_event(driver, ev)
        #     ingest_entity_hazard_rel(driver, uuid, ev)

        dfs_pred = nx.dfs_predecessors(pub_tree, 'NODE_ROOT')
        for key in dfs_pred:
            child_uuid = key
            parent_uuid = dfs_pred[key]
            order = pub_tree.nodes[key].get("order", 0)
            if parent_uuid == "NODE_ROOT":
                parent_uuid = project_id
            ingest_entity_rel(driver, parent_uuid, child_uuid, order)
