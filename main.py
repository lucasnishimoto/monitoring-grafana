import os, re, redis
from influxdb import InfluxDBClient
from typing import List, Dict

def get_env_var(var_name: str) -> str:
    var_value = os.environ.get(var_name)
    if var_value is None:
        raise EnvironmentError(f"Environment variable '{var_name}' is not set.")
    return var_value

def get_env_var_as_int(var_name: str) -> int:
    return int(get_env_var(var_name))

variaveis = {
    'REDIS_HOST': get_env_var('REDIS_HOST'),
    'REDIS_PORT': get_env_var_as_int('REDIS_PORT'),
    'INFLUXDB_HOST': get_env_var('INFLUXDB_HOST'),
    'INFLUXDB_PORT': get_env_var_as_int('INFLUXDB_PORT'),
    'INFLUXDB_DB': get_env_var('INFLUXDB_DB'),
    'AMBIENTE': get_env_var('AMBIENTE')
}

r = redis.Redis(host=variaveis['REDIS_HOST'], port=variaveis['REDIS_PORT'], db=0)
client = InfluxDBClient(host=variaveis['INFLUXDB_HOST'], port=variaveis['INFLUXDB_PORT'], database=variaveis["INFLUXDB_DB"])

def generate_json_payload(item: str, item2: str) -> List[Dict[str, Dict[str, str]]]:
    return [
        {
            "measurement": "Parakeet",
            "tags": {
                'Hostname': item,
                'Ips': item2
            },
            "fields": {
                "Ambiente": variaveis['AMBIENTE']
            }
        }
    ]

def main():
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

if __name__ == "__main__":
    main()
