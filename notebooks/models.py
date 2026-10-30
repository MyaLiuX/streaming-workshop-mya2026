from dataclasses import dataclass
import dataclasses
import json
import hashlib

@dataclass
class Ride:
    event_id: str
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    total_amount: float
    tpep_pickup_datetime: int

def ride_from_row(row):
    pu, do = int(row['PULocationID']), int(row['DOLocationID'])
    ts = int(row['tpep_pickup_datetime'].timestamp() * 1000)
    dist, amt = float(row['trip_distance']), float(row['total_amount'])
    event_id = hashlib.md5(f"{pu}|{do}|{ts}|{dist}|{amt}".encode()).hexdigest()
    return Ride(event_id, pu, do, dist, amt, ts)

def ride_serializer(ride):
    ride_dict = dataclasses.asdict(ride)
    json_str = json.dumps(ride_dict)
    return json_str.encode('utf-8')

def ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)