import os
import orjson
from typedefs.models.entity_def import EntityDef


def load_types(parent_folder: str):
    typedefs = []
    for root, _, files in os.walk(parent_folder):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file), "rb") as f:
                    data = orjson.loads(f.read())
                    entity_def = EntityDef(**data)
                    typedefs.append(entity_def)
    return typedefs


entity_defs = load_types("types")

for entity_def in entity_defs:
    print(entity_def.get_json())
