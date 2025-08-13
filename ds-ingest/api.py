import requests
from .config import PUB_LISTING_URL

def get_ds_pubs():
    """Return a generator of top-level publication metadata"""
    offset = 0
    limit = 100
    res_length = 100
    while res_length == 100:
        res = requests.get(PUB_LISTING_URL, params={"offset": offset, "limit": limit})
        res_json = res.json()

        yield from res_json["result"]
        res_length = len(res_json["result"])
        offset += 100


def get_publication(project_id: str):
    """Retrieve published metadata using the project ID."""
    res = requests.get(f"{PUB_LISTING_URL}/{project_id}")
    return res.json()


def iterate_publications():
    """Generator of all published metadata"""
    for pub in get_ds_pubs():
        if pub["type"] not in ["other", "field_reconnaissance"]:
            yield get_publication(pub["projectId"])
