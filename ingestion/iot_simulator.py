"""
IoT Device Event Simulator
Simulates real-time IoT device data streams for pipeline ingestion.
"""

import json
import random
import time
from datetime import datetime


def generate_iot_event(device_id: str) -> dict:
    """Generate a single IoT device event."""
    return {
        "device_id": device_id,
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": round(random.uniform(65.0, 130.0), 2),
        "pressure": round(random.uniform(90.0, 110.0), 2),
        "status": random.choice(["active", "active", "active", "alert", "inactive"]),
        "location": random.choice(["plant_A", "plant_B", "plant_C"])
    }


def simulate_stream(device_count: int = 5, events: int = 20) -> list:
    """Simulate a stream of IoT events across multiple devices."""
    devices = [f"D{str(i).zfill(3)}" for i in range(1, device_count + 1)]
    stream = []

    for _ in range(events):
        device = random.choice(devices)
        event = generate_iot_event(device)
        stream.append(event)
        print(f"[STREAM] {event}")

    return stream


if __name__ == "__main__":
    print("Starting IoT Event Simulation...\n")
    events = simulate_stream(device_count=5, events=10)
    with open("data/simulated_events.json", "w") as f:
        json.dump(events, f, indent=2)
    print(f"\nSimulated {len(events)} events saved to data/simulated_events.json")