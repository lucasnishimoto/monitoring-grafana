import redis, re, os 
from influxdb import InfluxDBClient  

variaveis = dict(
    REDIS_HOST=os.environ.get('REDIS_HOST'),
    REDIS_PORT=int(os.environ.get('REDIS_PORT')),
    INFLUXDB_HOST=os.environ.get('INFLUXDB_HOST'),
    INFLUXDB_PORT=int(os.environ.get('INFLUXDB_PORT')),
    INFLUXDB_DB=os.environ.get('INFLUXDB_DB')
)

r = redis.Redis(host=variaveis['REDIS_HOST'] , port=variaveis['REDIS_PORT'], db=0)

client = InfluxDBClient(host=variaveis['INFLUXDB_HOST'],port= variaveis['INFLUXDB_PORT'], database=variaveis["INFLUXDB_DB"])


for key in r.scan_iter():
    print(key)
    valor = r.mget(key)
    print(valor)
    ips = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", str(key))
    for element in valor:
        stringlist=[x.decode('utf-8') for x in valor]
    for item, item2 in zip(stringlist, ips):
        json_payload = []
        data = {
             "measurement": "Parakeet",
             "tags": {
                  'Hostname': item,
                  'Ips': item2
             },
             "fields": {
                  "Ambiente": "DEV"
             }
        }
        json_payload.append(data)
        client.write_points(json_payload)   
