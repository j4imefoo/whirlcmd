# whirlcmd
A commandline tool to control Samourai's Whirlpool coinjoins using Whirlpool API

## Prerequisites
We will need to:
- Correctly install and configure our whirlpool-cli
- Add option `cli.api.http-enable=true` to `whirlpool-cli-config.properties`
- Create a new Onion service that will give access to our port 8898
- Leave whirlpool-cli running in tmux or screen
- We need tor running on the client machine

## Configuration
All configurable parameters can be found in the script

- `url` will point to our onion service: `url = 'http://our-onion-service-address.onion:8898/rest/'`
- `apiKey` the key you will find in your `whirlpool-cli-config.properties`
- `apiVersion` the value you will find in `https://code.samourai.io/whirlpool/whirlpool-client-cli/-/blob/develop/src/main/java/com/samourai/whirlpool/cli/api/protocol/CliApi.java`

## Usage
This script will allow you to interact with your remote whirlpool-cli installation. 

Please note that this was intended to be used on an Android mobile phone using Termux but it can be used in any machine running Python.

The following commands are accepted:

- `whirlcmd lspost` : list all utxos being mixed in the postmix wallet
- `whirlcmd lspre` : list all utxos in the premix wallet
- `whirlcmd lsdepo` : list all utxos in the deposit wallet
- `whirlcmd pools` : list all pools and their state
- `whirlcmd deposit` : get a new deposit address
- `whirlcmd start all` : start to mix all utxos in the postmix wallet
- `whirlcmd start utxo:n` : start to mix a certain utxo
- `whirlcmd stop all` : stop mixing all utxos
- `whirlcmd stop utxo:n` : stop mixing a certain utxo


## More information:
https://twitter.com/j4imefoo

If you want to buy me a beer:
- https://paynym.is/+luckywood116
- https://tippin.me/@j4imefoo
