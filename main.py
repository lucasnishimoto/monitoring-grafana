import redis, re, os 
from influxdb import InfluxDBClient  

variaveis = dict(
    REDIS_HOST=os.environ.get('REDIS_HOST'),
    REDIS_PORT=int(os.environ.get('REDIS_PORT')),
    INFLUXDB_HOST=os.environ.get('INFLUXDB_HOST'),
    INFLUXDB_PORT=int(os.environ.get('INFLUXDB_PORT')),
    INFLUXDB_DB=os.environ.get('INFLUXDB_DB')
)

r = redis.Redis(host=variaveis['REDIS_HOST'], port=variaveis['REDIS_PORT'], db=0)

client = InfluxDBClient(host=variaveis['INFLUXDB_HOST'], port=variaveis['INFLUXDB_PORT'], database=variaveis["INFLUXDB_DB"])


def generate_json_payload(item, item2):
    return [
        {
            "measurement": "Parakeet",
            "tags": {
                'Hostname': item,
                'Ips': item2
            },
            "fields": {
                "Ambiente": "DEV"
            }
        }
    ]


keys = list(r.scan_iter())

with r.pipeline() as pipe:
    for key in keys:
        pipe.mget(key)
    values = pipe.execute()

for key, value in zip(keys, values):
    print(key)
    ips = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", str(key))
    if not ips:
        continue
    for item, item2 in zip(value, ips):
        json_payload = generate_json_payload(item.decode('utf-8'), item2)
        client.write_points(json_payload)
