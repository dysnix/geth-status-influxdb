#!/usr/bin/env python
import time
import datetime

import requests
from influxdb import InfluxDBClient
from web3 import Web3, HTTPProvider
import settings

# InfluxDB init
db = InfluxDBClient(host=settings.INFLUXDB_HOST, port=settings.INFLUXDB_PORT, database=settings.INFLUXDB_DB_NAME)

w3 = Web3(HTTPProvider('http://{host}:{port}'.format(host=settings.ETH_RPC_HOST, port=settings.ETH_RPC_PORT),
                       request_kwargs={'timeout': settings.ETH_RPC_TIMEOUT}))


def get_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')


def get_etherscan_highest_block():
    request_params = {'module': 'proxy',
                      'action': 'eth_blockNumber',
                      'apikey': settings.ETHERSCAN_API_KEY}
    response = requests.get(settings.ETHERSCAN_API_URL, params=request_params)
    response_json = response.json()
    highest_block_hex = response_json.get('result')
    highest_block = int(highest_block_hex, 0)
    return highest_block


def get_eth_status():
    highest_block = get_etherscan_highest_block()
    current_block = w3.eth.blockNumber
    sync_diff = highest_block - current_block

    # pending_txs_count = w3.eth.pendingTransactions.length
    accounts_count = len(w3.eth.accounts)

    status = {
        'highestBlock': highest_block,
        'currentBlock': current_block,
        'syncDiff': sync_diff,
        # 'pendingTransactionsCount': pending_txs_count,
        'accountsCount': accounts_count
    }

    return status


def send_stats_to_db(db, status):
    json_body = [
        {
            "measurement": "eth_status",
            "tags": {
                "host": "all",
            },
            "time": get_timestamp(),
            "fields": status
        }
    ]
    db.write_points(json_body)


def main():
    try:
        while not time.sleep(settings.UPDATE_INTERVAL):
            status = get_eth_status()
            send_stats_to_db(db, status)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
