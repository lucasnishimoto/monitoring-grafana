# Monitorando com Grafana
## _Redis, Influxdb e Grafana_

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)]()

## Pré-requisitos 

- Linux
- Arquivo dump.rdb para o Redis
- Docker-compose, Docker e python3

## Estrutura

**Redis** 
O Redis vai ser o banco de dados, na qual vai ter as informações de hostname e ip, exemplo:

```
set Ubuntu 255.255.255.0/24
```

| Key | Value |
| ------ | ------ |
| Ubuntu | 255.255.255.0/24

**Python**

O script main.py vai ter a função de filtrar os dados e entregar os dados filtrados no Influxdb. 

**Influxdb**

O Influx por ser um banco timeserial, ele irá gravar que horas o dado foi inserido no banco. 

## Objetivo 

Criar um monitor que disponibiliza a leitura de hostname e ips cadstrados no Redis com o tempo que ele foi cadastrado.


