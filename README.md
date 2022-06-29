# whirlcmd

A command-line tool to control Samourai Whirlpool CoinJoins using the Whirlpool API.

## Prerequisites

Before using whirlcmd, you will need to:

- Correctly install and configure our whirlpool-cli
- Add option `cli.api.http-enable=true` to `whirlpool-cli-config.properties`
- Create a new Onion service that will give access to our port 8898
- Leave whirlpool-cli running in tmux or screen
- We need Tor running on the client machine

## Installation

In order to install this script, simply clone the repository and install the requirements (if necessary) via the below commands:

```bash
git clone https://github.com/j4imefoo/whirlcmd.git
python3 -m pip install -r requirements.txt
```

***Please note that you must be running Tor (either via the daemon or the Tor browser) in order for the script to properly gather offers over Tor. The easiest way to get started if you're unfamiliar is to download and run [the Tor browser](https://www.torproject.org/download/) and edit `TOR_PORT` to `9150` as shown below.***

## Configuration

All configurable parameters can be found in the `whirlcmdconfig.ini` configuration file:

- `url`: will point to our onion service, i.e. `http://our-onion-service-address.onion:8898/rest/`
- `apiKey`: the key you will find in your `whirlpool-cli-config.properties`
- `apiVersion`: the value you will find in `https://code.samourai.io/whirlpool/whirlpool-client-cli/-/blob/develop/src/main/java/com/samourai/whirlpool/cli/api/protocol/CliApi.java`
- `TOR_PORT`: The local Tor SOCKS5 port to use, usually 9050 in case of Tor daemon or 9150 for Tor browser

## Usage

This script will allow you to interact with your remote whirlpool-cli installation.

Please note that this was intended to be used on an Android mobile phone using Termux but it can be used in any machine running Python.

The following commands are accepted:

```bash
$ whirlcmd -h
usage: whirlcmd.py [-h] [-u] [-g] [-l {postmix,premix,deposit} | -p | -d | -s START | -t STOP]

A command-line tool to control Samourai Whirlpool CoinJoins using the Whirlpool API.

optional arguments:
  -h, --help            show this help message and exit
  -u, --unlock          Unlock the Whirlpool wallet
  -g, --light           Light mode. Display more compact information
  -l {postmix,premix,deposit}, --list {postmix,premix,deposit}
                        List utxos in postmix, premix or deposit wallets
  -p, --pools           List of pools
  -d, --deposit         Get a new address to receive bitcoin
  -s {all,utxo}, --start {all,utxo}
                        Start mixing a utxo or all of them
  -t {all,utxo}, --stop {all,utxo}  Stop mixing a utxo or all of them
```

## More information:

https://twitter.com/j4imefoo

If you want to buy me a beer:
- https://paynym.is/+luckywood116
- https://tippin.me/@j4imefoo
