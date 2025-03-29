from db import insert_component_data
import sys
from datetime import datetime

MODEL_POSITIONS = {
    "PC": (6, 10),
    "AB": (8, 12),
    "XY": (10, 12)
}

def extract_batch_data(batch_id):
    for model, (start, end) in MODEL_POSITIONS.items():
        if batch_id.startswith(model):
            return model, batch_id[start:end]
    return None, None

def process_batch(feeder_id, batch_id):
    model_type, important_data = extract_batch_data(batch_id)

    if important_data:
        insert_component_data(feeder_id, batch_id, model_type, important_data)
        print(f"Processed: {batch_id} (Feeder: {feeder_id}, Model: {model_type}, Data: {important_data})")
        return True
    else:
        print(f"Error: Unrecognized batch format - {batch_id}", file=sys.stderr)
        return False

if __name__ == "__main__":
    test_cases = [
        ("Feeder1", "PC012012345HA"),
        ("Feeder2", "PC000012345DB"),
        ("Feeder3", "AB000012345DC"),
        ("Feeder4", "XY000012345DC"),
        ("Feeder5", "INVALID123456")
    ]

    for feeder_id, batch_id in test_cases:
        process_batch(feeder_id, batch_id)