# truffle-docker

## start local ganache instance

during this tutorial we will deploy a smart contract to the blockchain.

for the sake of this tutorial we will use a dockerized test instance based on [ganache](https://www.trufflesuite.com/ganache).
follow the description in [ganache-docker repository]( 
https://github.com/matthiaszimmermann/ganache-docker)

to spin up a ganache container using the following command.

```bash
docker run -p 7545:8545 -d --name ganache ganache
```

## build the truffle docker image

the node version manager is used as the starting point of the dockerized setup based on the suggestion in "mastering ethereum" in 
[appendix dev tools](https://github.com/ethereumbook/ethereumbook/blob/develop/appdx-dev-tools.asciidoc)
about truffle

the dockerized truffle in this repository is based on updated version of the some [github](https://github.com/phusion/baseimage-docker)
[repositories](https://github.com/tzenderman/docker-nvm)

to create the truffle docker image run the following command.

```bash
docker build -t truffle .
```

## run the truffle container

```bash
docker run -it --rm -v $PWD:/app truffle bash
```

you now have access to the command line inside the container.
check that truffle is installed successfully via `truffle version`.

```bash
root@cc3de96a171d:/app# truffle version
Truffle v5.4.11 (core: 5.4.11)
Solidity v0.5.16 (solc-js)
Node v14.17.6
Web3.js v1.5.2
```

please note that the exact version numbers may change (increase) over time.

## create a truffle project

still inside the container use the following commands to create the project folder (assuming you are located in this repositorys root directory, otherwise you need to create directory `faucet` first).

```bash
root@cc3de96a171d:/app#
cd faucet
```

### initalize the faucet project

the following steps are different if you want to create your own project or if you are located in the existing github project.

1) exploring this github repository
2) setting up your own faucet project

in case you are exploring this github project you skip the steps about `truffle init`, `npm init` adding the solidty faucet contract file and the javascript migration/deployment file.

in case you'd like to setup your own project you can now use truffle for scaffolding of the faucet project

```bash
truffle init
```

now check the created directory structure using the `tree` utility

```bash
root@cc3de96a171d:/app/faucet#
tree
.
├── contracts
│   └── Migrations.sol
├── migrations
│   └── 1_initial_migration.js
├── test
└── truffle-config.js
```

then, let `npm` do its work

```bash
npm init
```

accept all suggestions to create a default `package.json` file.

### add solidity contract source file

in folder contracts add file [`Faucet.sol`]()

```javascript
// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Faucet {

    // default function to accept payments to contract
    function () external payable {}

    function withdraw(uint withdraw_amount) public {
        msg.sender.transfer(withdraw_amount);
    }
}
```

### add migration/deployment script

in folder migrations the file [`2_deploy_contracts.js`]().
this file tells truffle how the contract should be deployed to the blockchain.

in the case of the faucet contract there is hardly anything to do and the script looks a bit like overkill.
but then, truffle was created with more complex setups in mind.

```javascript
const Faucet = artifacts.require("./Faucet.sol");

module.exports = function (deployer) {
  deployer.deploy(Faucet);
};
```

## compile the contract 

with the completed project setup we are now ready to complile our smart contract.
for this, truffle provides the command `truffle compile` as shown below.

```bash
truffle compile
```

## deploy the contract

for deployment/migration truffle relies on its configuration file `truffle-config.js`.

as we had initially started a dockerized local ganache chain we need to provide the coordinates of this chain to truffle in order to deploy the contract to that chain.

to keep the `truffle-config.js` somewhat generic the example file in this github repository uses environment variables to obtain the necessary information.

```bash
cat > .env <<EOL
MNEMONIC="candy maple cake sugar pudding cream honey rich smooth crumble sweet treat"
HTTP_PROVIDER="http://host.docker.internal:7545"
TRUFFLE_HOST=host.docker.internal
TRUFFLE_PORT=7545
TRUFFLE_NETWORK_ID=*
EOL
```

in case your docker installation does not support `host.docker.internal` you will need to work with the explicit IP address of your machine.
tools like `ifconfig` help to figure out this address.

using network development (implicitly, see truffle-config.json)

```bash
truffle migrate
```

a successful deploy will provide useful information such as the contracts address, similar to the sample output provided below.

```bash
2_deploy_contracts.js
=====================

   Deploying 'Faucet'
   ------------------
   > transaction hash:    0x2332e50d737751b41138f27ac6b35c80cf2eccd457685bb97f8c756a277668bc
   > Blocks: 0            Seconds: 0
   > contract address:    0x345cA3e014Aaf5dcA488057592ee47305D9B3e10
   > block number:        3
   > block timestamp:     1632403979
   > account:             0x627306090abaB3A6e1400e9345bC60c78a8BEf57
   > balance:             9999.99177132
   > gas used:            124621 (0x1e6cd)
   > gas price:           20 gwei
   > value sent:          0 ETH
   > total cost:          0.00249242 ETH


   > Saving migration to chain.
   > Saving artifacts
   -------------------------------------
   > Total cost:          0.00249242 ETH


Summary
=======
> Total deployments:   2
> Final cost:          0.00737842 ETH```
```

successful deployment will also update the meta data files in directory `build` maintained by truffle to keep track of what contracts have been deployed on which networks/chains.

for the faucet contract this information will be stored in file `build/contracts/Faucet.json` relative to the faucet project directory.

## fund the faucet contract

before the deployed contract send any ethers to any requesting address the contract itself needs to actually have its own funds.

for this, move some ethers from the ganache address 0: `0x627306090abaB3A6e1400e9345bC60c78a8BEf57` to the faucet contract
as described in the readme of [ganache-docker repository]( 
https://github.com/matthiaszimmermann/ganache-docker)

you may use metamask to transfer funds to the contract address (using the command line output of `truffle migrate` or the information in `Faucet.json` under attribute `networks.<network-id>.address`)

## call the contract "withdraw" method

call the withdraw method using the python script

```bash
python3 ../faucet_client.py \
    -a 0x627306090abaB3A6e1400e9345bC60c78a8BEf57 \
    -k 0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3
```

if successful the output should look similar to the one provided below

```bash
address 0x627306090abaB3A6e1400e9345bC60c78a8BEf57
pkey 0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3
web3 provider http://host.docker.internal:7545 chain id 1234 connected True
amount in wei 10000000000000000
balance before 9990.161201740000000492 eth account 0x627306090abaB3A6e1400e9345bC60c78a8BEf57
contract object created: Faucet
contract address: 0x345cA3e014Aaf5dcA488057592ee47305D9B3e10
txn created {'value': 0, 'chainId': 1234, 'gas': 2000000, 'gasPrice': 20000000000, 'nonce': 35, 'to': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10', 'data': '0x2e1a7d4d000000000000000000000000000000000000000000000000002386f26fc10000'}
txn successfully sent. txn hash b'l\x8b6\xc7\x90_(x\x00 |\xb7o\xc7\xc3*N\x92a\x03\xc8\xf8\xab\x8f\xdc8\xbex\xcd\xb3\x15\xdc'
balance  after 9990.170622240000000492 eth account 0x627306090abaB3A6e1400e9345bC60c78a8BEf57
```
