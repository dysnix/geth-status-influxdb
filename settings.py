import os

# Ethereum
ETH_RPC_HOST = os.environ.get('ETH_RPC_HOST', 'ethereum.default')
ETH_RPC_PORT = int(os.environ.get('ETH_RPC_PORT', 8545))
ETH_RPC_TIMEOUT = int(os.environ.get('ETH_RPC_TIMEOUT', 100))

# InfluxDB
INFLUXDB_HOST = os.environ.get('INFLUXDB_HOST', 'influxdb-influxdb.monitoring')
INFLUXDB_PORT = int(os.environ.get('INFLUXDB_PORT', 8086))
INFLUXDB_DB_NAME = os.environ.get('INFLUXDB_DB_NAME', 'k8s')

# Update interval
UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL', 60))

try:
    from local_settings import *
except ImportError:
    pass
