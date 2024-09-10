from indexstore.index_store import IndexStore
from typedefs.models.attribute_def import AttributeDef
from typedefs.models.entity_def import EntityDef
from indexstore.models import Index


def add_attribute_index(index_store: IndexStore, entity_def: EntityDef, attribute: AttributeDef) -> None:
    index_store.add_attribute_index(entity_def, attribute)


def remove_attribute_index(index_store: IndexStore, entity_def: EntityDef, attribute: AttributeDef) -> None:
    index_store.remove_attribute_index(entity_def, attribute)


def attribute_index_exists(index_store: IndexStore, entity_def: EntityDef, attribute: AttributeDef) -> bool:
    return index_store.attribute_index_exists(entity_def, attribute)


def list_indices(index_store: IndexStore) -> list[Index]:
    return index_store.list_indices()


def generate_index_name(index_store: IndexStore, entity_def: EntityDef, attribute: AttributeDef) -> str:
    return index_store.generate_index_name(entity_def, attribute)


def get_attribute_type_name(index_store: IndexStore, attribute: AttributeDef) -> str:
    return index_store.get_attribute_type_name(attribute)


def init_index(index_store: IndexStore) -> None:
    index_store.init_index()
