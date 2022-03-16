#!/usr/bin/env python3

import json
import sys
import subprocess
import requests

url = 'http://our-onion-service-address.onion:8898/rest/'
apiKey = 'api-key-from-whirlpool-cli-config.properties'
apiVersion = "0.10"

headers = {'apiKey': apiKey, 'apiVersion': apiVersion }
cmd_deposit = "wallet/deposit?increment=true"
cmd_list = "utxos"
cmd_start = "/startMix"
cmd_stop = "/stopMix"
cmd_startAll = "mix/start"
cmd_stopAll = "mix/stop"
cmd_pools = "pools"

feeTarget = ["BLOCKS_2", "BLOCKS_4", "BLOCKS_6", "BLOCKS_12", "BLOCKS_24"]

def get_tor_session():
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
    return session

def exit_usage():
     print("Usage: %s lspost|lspre|lsdepo|pools|deposit|start|stop [utxo:n]|[all]"% (sys.argv[0]))
     print("         lspost | lspre | lsdepo: list utxos in postmix, premix or deposit wallets")
     print("         pools: list whirlpool running pools")
     print("         deposit: generate a new deposit address")
     print("         start utxo:n | all: start mixing a specific utxo or all")
     print("         stop utxo:n | all: stop mixing a specific utxo or all")
     exit(1)

def listutxos(wallet):
    req = session.get(url + cmd_list, verify=False, headers=headers)
    result = req.json()
    utxos = result[wallet]['utxos']
    print("Total: %d utxos = %.3f"% (len(utxos), result[wallet]['balance']/100000000))
    if (len(utxos)>0):
        print("%s %s %-66s %-42s %11s %11s %s"% ("balance", "confs", "utxo", "address", "status", "mixable", "mixes"))
    for entry in utxos:
        print("%7.3f %5d %s:%d %s %11s %11s %d"% (entry['value']/100000000, entry['confirmations'], entry['hash'], entry['index'], entry['address'], entry['status'], entry['mixableStatus'], entry['mixsDone']))

def deposit():
    req = session.get(url + cmd_deposit, verify=False, headers=headers)
    result = req.json()
    print(result['depositAddress'])

def pools():
    req = session.get(url + cmd_pools + "?tx0FeeTarget=" + feeTarget[4], verify=False, headers=headers)
    result = req.json()
    pools = result['pools']
    print("%10s %10s %10s %10s %10s %15s %s"% ("pool", "fee", "Freeriders", "Premixers", "last (h)", "status", "balance min"))
    for entry in pools:
        print("%10s %10.4f %10d %10d %10.1f %15s %.8f"% (entry['poolId'], entry['feeValue']/100000000, entry['nbRegistered'], entry['nbConfirmed'], entry['elapsedTime']/1000/60/60, entry['mixStatus'],  entry['tx0BalanceMin']/100000000))

def control(operation, element):
    if element=="all":
        if operation=="start":
            command=cmd_startAll
        elif operation=="stop":
            command=cmd_stopAll
    else:
        try:
            utxohash, utxoindex = sys.argv[2].split(":")
        except:
            exit_usage()
        if operation=="start":
            command="utxos/" + utxohash + ":" + utxoindex + cmd_start
        elif operation=="stop":
            command="utxos/" + utxohash + ":" + utxoindex + cmd_stop
    req = session.post(url + command, verify=False, headers=headers)
    if req.status_code == 200:
        print("OK!")
    elif req.status_code == 500:
        print("Error")
    else:
        print(req)

if __name__ == "__main__":
    
    session = get_tor_session()

    if len(sys.argv)==3 and (sys.argv[1]=="start" or sys.argv[1]=="stop"):
        control(sys.argv[1], sys.argv[2]);
    elif len(sys.argv)==2 and sys.argv[1]=="deposit":
        deposit()
    elif len(sys.argv)==2 and sys.argv[1]=="lspost":
        listutxos('postmix')
    elif len(sys.argv)==2 and sys.argv[1]=="lsdepo":
        listutxos('deposit')
    elif len(sys.argv)==2 and sys.argv[1]=="lspre":
        listutxos('premix')
    elif len(sys.argv)==2 and sys.argv[1]=="pools":
        pools()
    else:
        exit_usage()
