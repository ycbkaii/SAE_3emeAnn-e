from fastapi import APIRouter, Depends
from fastapi import Security
from fastapi.security import APIKeyHeader

from embeddings.embeddingsController import (
    check_client,
    initialize_elastic_search,
)

api_key = APIKeyHeader(name="admin-api-key")

ADMIN_KEY = "changeme"


def admin_api_key(key: str = Security(api_key)):
    return key == ADMIN_KEY


admin_router = APIRouter(dependencies=[Depends(admin_api_key)], prefix="/admin")


@admin_router.get("/es_info")
def elastic_search_info():
    """Renvoie les infos du clients ElasticSearch"""
    return check_client()


@admin_router.get("/init_es")
def init_es():
    return initialize_elastic_search()


@admin_router.get("/modify_api_key/{new_key}")
def modify_api_key(new_key: str):
    global ADMIN_KEY
    ADMIN_KEY = new_key
    return "Api key successfully updated"
