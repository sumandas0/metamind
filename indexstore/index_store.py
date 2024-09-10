from typing import Protocol, Callable
from typedefs.models.attribute_def import AttributeDef
from typedefs.models.entity_def import EntityDef
from indexstore.models import Index


class IndexStore(Protocol):
    def init_index(self) -> None: ...

    def get_attribute_type_name(self, attribute: AttributeDef) -> str: ...

    def generate_index_name(self, entity_def: EntityDef, attribute: AttributeDef) -> str: ...

    def add_attribute_index(self, entity_def: EntityDef, attribute: AttributeDef) -> None: ...

    def remove_attribute_index(self, entity_def: EntityDef, attribute: AttributeDef) -> None: ...

    def attribute_index_exists(self, entity_def: EntityDef, attribute: AttributeDef) -> bool: ...

    def list_indices(self) -> list[Index]: ...
