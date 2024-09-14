from indexstore.index_store import IndexStore
from typedefs.models.attribute_def import AttributeDef
from typedefs.models.entity_def import EntityDef
from indexstore.models import Index
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def add_attribute_index(index_store: IndexStore, entity_def: EntityDef, attribute: AttributeDef) -> None:
    LOGGER.info(f"Adding attribute index for entity {entity_def.name}, attribute {attribute.name}")
    index_store.add_attribute_index(entity_def, attribute)
    LOGGER.debug(f"Attribute index added successfully for {entity_def.name}.{attribute.name}")


def remove_attribute_index(index_store: IndexStore, entity_def: EntityDef, attribute: AttributeDef) -> None:
    LOGGER.info(f"Removing attribute index for entity {entity_def.name}, attribute {attribute.name}")
    index_store.remove_attribute_index(entity_def, attribute)
    LOGGER.debug(f"Attribute index removed successfully for {entity_def.name}.{attribute.name}")


def attribute_index_exists(index_store: IndexStore, entity_def: EntityDef, attribute: AttributeDef) -> bool:
    LOGGER.debug(f"Checking if attribute index exists for entity {entity_def.name}, attribute {attribute.name}")
    exists = index_store.attribute_index_exists(entity_def, attribute)
    LOGGER.debug(f"Attribute index exists: {exists}")
    return exists


def list_indices(index_store: IndexStore) -> list[Index]:
    LOGGER.info("Listing all indices")
    indices = index_store.list_indices()
    LOGGER.debug(f"Found {len(indices)} indices")
    return indices


def generate_index_name(index_store: IndexStore, entity_def: EntityDef, attribute: AttributeDef) -> str:
    LOGGER.debug(f"Generating index name for entity {entity_def.name}, attribute {attribute.name}")
    index_name = index_store.generate_index_name(entity_def, attribute)
    LOGGER.debug(f"Generated index name: {index_name}")
    return index_name


def get_attribute_type_name(index_store: IndexStore, attribute: AttributeDef) -> str:
    LOGGER.debug(f"Getting attribute type name for attribute {attribute.name}")
    type_name = index_store.get_attribute_type_name(attribute)
    LOGGER.debug(f"Attribute type name: {type_name}")
    return type_name


def init_index(index_store: IndexStore) -> None:
    LOGGER.info("Initializing index")
    index_store.init_index()
    LOGGER.info("Index initialized successfully")
