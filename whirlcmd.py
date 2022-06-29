#!/usr/bin/env python3

import configparser
import getpass
import json
import sys
import signal
import requests
import argparse

# Import user configuration from whirlcmdconfig.ini file
config = configparser.ConfigParser()
config.read('whirlcmdconfig.ini')

cmd = {'deposit': 'wallet/deposit?increment=true', 'list': 'utxos', 'start': '/startMix', 'stop': '/stopMix', 'startAll': 'mix/start', 'stopAll': 'mix/stop', 'pools': 'pools', 'unlock': 'cli/login'}
headers = {'apiKey': config['DEFAULT']['apiKey'], 'apiVersion': config['DEFAULT']['apiVersion'] }
feeTarget = ['BLOCKS_2', 'BLOCKS_4', 'BLOCKS_6', 'BLOCKS_12', 'BLOCKS_24']

def sigint_handler(signal, frame):
    print ('Cancelled.')
    sys.exit(0)

def get_tor_session():
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:' + config['DEFAULT']['TOR_PORT'],
                       'https': 'socks5h://127.0.0.1:' + config['DEFAULT']['TOR_PORT']}
    return session

def unlock():
    try:
        req = session.get(config['DEFAULT']['url'] + "cli", verify=False, headers=headers)
        response = req.json()
        if response['loggedIn'] == True:
            print("Whirlpool is already unlocked!")
        else:
            passphrase = getpass.getpass('Please enter your Whirlpool wallet passphrase:')
            payload = { 'seedPassphrase': passphrase }
            req = session.post(config['DEFAULT']['url'] + cmd['unlock'], verify=False, headers=headers, json=payload)
            response = req.json()
            if response['loggedIn'] == True:
                print("Unlocked Whirlpool successfully!")
            else:
                print("Unable to unlock Whirlpool, please check the passphrase you entered and try again!")
                exit(1)
    except IOError:
        print("Please, make sure you are running Tor!")
        exit(1)

def listutxos(wallet):
    try:
        req = session.get(config['DEFAULT']['url'] + cmd['list'], verify=False, headers=headers)
    except IOError:
        print("Please, make sure you are running Tor!")
        exit(1)
    result = req.json()
    try:
        utxos = result[wallet]['utxos']
    except KeyError:
        print("Please, make sure your Whirlpool wallet is unlocked via --unlock!")
        exit(1)
    if full_output:
        print("Total: %d utxos = %.3f"% (len(utxos), result[wallet]['balance']/100000000))
    if (len(utxos)>0):
        if full_output:
            print(f"{'balance'} {'confs'} {'utxo':66} {'address':42} {'mixes':5} {'status':11}")
        else:
            print(f"{'balance'} {'confs'} {'mixes':5} {'status':11}")
    lines = []
    for entry in utxos:
        line = {}
        line['value'] = entry['value']/100000000
        line['confs'] = entry['confirmations']
        line['utxo'] = f"{entry['hash']}:{entry['index']}"
        line['address'] = entry['address']
        line['mixes'] = entry['mixsDone']
        line['status'] = entry['status']
        lines.append(line)

    lines.sort(key=lambda item: item.get("mixes"))
    
    for line in lines:
        if full_output:
            print(f"{line['value']:7.3f} {line['confs']:5d} {line['utxo']} {line['address']} {line['mixes']:5} {line['status']:11}")
        else:
            print(f"{line['value']:7.3f} {line['confs']:5d} {line['mixes']:5} {line['status']:11}")

def deposit():
    try:
        req = session.get(config['DEFAULT']['url'] + cmd['deposit'], verify=False, headers=headers)
    except IOError:
        print("Please, make sure you are running Tor!")
        exit(1)
    result = req.json()
    print(result['depositAddress'])

def pools():
    try:
        req = session.get(config['DEFAULT']['url'] + cmd['pools'] + "?tx0FeeTarget=" + feeTarget[4], verify=False, headers=headers)
    except IOError:
        print("Please, make sure you are running Tor!")
        exit(1)
    result = req.json()
    pools = result['pools']
    print("%10s %10s %10s %10s %10s %15s %s"% ("pool", "fee", "Freeriders", "Premixers", "last (h)", "status", "balance min"))
    for entry in pools:
        print("%10s %10.4f %10d %10d %10.1f %15s %.8f"% (entry['poolId'], entry['feeValue']/100000000, entry['nbRegistered'], entry['nbConfirmed'], entry['elapsedTime']/1000/60/60, entry['mixStatus'],  entry['tx0BalanceMin']/100000000))

def control(operation, element):
    if element=="all":
        if operation=="start":
            command=cmd['startAll']
        elif operation=="stop":
            command=cmd['stopAll']
    else:
        try:
            utxohash, utxoindex = sys.argv[2].split(":")
        except:
            print('Error in utxo')
            sys.exit(1)
        if operation=="start":
            command="utxos/" + utxohash + ":" + utxoindex + cmd['start']
        elif operation=="stop":
            command="utxos/" + utxohash + ":" + utxoindex + cmd['stop']
    try:
        req = session.post(config['DEFAULT']['url'] + command, verify=False, headers=headers)
    except IOError:
        print("Please, make sure you are running Tor!")
        sys.exit(1)
    if req.status_code == 200:
        print("OK!")
    elif req.status_code == 500:
        print("Error")
    else:
        print(req)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    session = get_tor_session()
    parser = argparse.ArgumentParser(description='A command-line tool to control Samourai Whirlpool CoinJoins using the Whirlpool API.')
    parser.add_argument(
        '-u',
        '--unlock',
        help='Unlock the Whirlpool wallet',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-g',
        '--light',
        help='Light mode. Display more compact information',
        action='store_true',
        default=False
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-l',
        '--list',
        help='List utxos in postmix, premix or deposit wallets',
        type=str,
        choices=['postmix', 'premix', 'deposit'],
        default=False,
    )
    group.add_argument(
        '-p',
        '--pools',
        help='List of pools',
        action='store_true',
        default=False
    )
    group.add_argument(
        '-d',
        '--deposit',
        help='Get a new address to receive bitcoin',
        action='store_true',
        default=False
    )
    group.add_argument(
        '-s',
        '--start',
        help='Start mixing a utxo or all of them',
        type=str
    )
    group.add_argument(
        '-t',
        '--stop',
        help='Stop mixing a utxo or all of them',
        type=str
    )


    args = parser.parse_args()
    full_output = not args.light
    if args.unlock:
        unlock()
    elif args.start:
        control('start', args.start)
    elif args.stop:
        control('stop', args.stop)
    elif args.deposit:
        deposit()
    elif args.list:
        listutxos(args.list)
    elif args.pools:
        pools()
