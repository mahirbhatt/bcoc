OPEN TERMINAL ( ctrl + alt + T ):
1.	sudo apt-get update
2.	sudo apt upgrade
3.	sudo apt install curl
4.	curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
5.	sudo apt-get install -y nodejs
6.	npm --version
7.	sudo npm i -g truffle@v5.0.8
8.	truffle version
9.	ctrl + d

OPEN NEW TERMINAL ( ctrl + alt + T ): **for Ethereum => reference folder /for Eth

1.	mkdir bcocEth
2.	cd bcocEth
3.	sudo apt-get install software-properties-common
4.	sudo add-apt-repository -y ppa:ethereum/ethereum
5.	sudo apt-get install ethereum
6.	sudo gedit bcocGenesis.json
			{
 			  "config": {
     			 "chainId": 1994,
    			  "homesteadBlock": 0,
    			  "eip155Block": 0,
    			  "eip158Block": 0,
    			  "byzantiumBlock": 0
   			},
   			"difficulty": "0x200",
   			"gasLimit": "8000000",
   			"alloc": {
			}	
			}

7.	geth --datadir ./bcocDataDir init ./bcocGenesis.json
8.	sudo gedit mineWhenNeeded.js

var mining_threads = 1

function checkWork() {
    if (eth.getBlock("pending").transactions.length > 0) {
        if (eth.mining) return;
        console.log("== Pending transactions! Mining...");
        miner.start(mining_threads);
    } else {
        miner.stop();
        console.log("== No transactions! Mining stopped.");
    }
}
eth.filter("latest", function(err, block) { checkWork(); });
eth.filter("pending", function(err, block) { checkWork(); });

checkWork();
9.	geth --preload "mineWhenNeeded.js" --datadir ./bcocDataDir --ipcdisable --rpc --rpcapi 'web3,net,eth,personal,debug,rpc,miner' --rpccorsdomain '*' --rpcport 8100 --networkid 1110 --port 30300 --allow-insecure-unlock console

10.	personal.listAccounts
11.	personal.newAccount("redhat")
12.	personal.newAccount("redhat")
13.	personal.newAccount("redhat")
14.	personal.newAccount("redhat")
15.	personal.unlockAccount(eth.accounts[0],"redhat",0)
16.	miner.start()

OPEN NEW TERMINAL ( ctrl + alt + T ): **for Truffle reference folder /for Truffle


1.	mkdir bcocTruffle
2.	cd bcocTruffle
3.	truffle unbox pet-shop
4.	ls
**Now GoTo=> bcocTruffle/Contracts folder and paste solidity file i.e bcoc.sol

**In Terminal
5.	cd migrations/
6.	sudo gedit 2_bcocMigration.js

		var bcoc = artifacts.require("Bcoc");
		module.exports = function(deployer) {
 		deployer.deploy(bcoc);
		};

7.	cd ..
8.	ls
9.	sudo gedit truffle-config.js
**Change port number to 8100 or custom.

***Make sure in ethereum, Default account is unlocked and Miner is started.
10.	truffle migrate
11.	
OPEN NEW TERMINAL ( ctrl + alt + T ): **for ipfs

**Download go-ipfs for your platform
1.	tar xvfz go-ipfs.tar.gz
2.	cd go-ipfs
3.	./install.sh
4.	ipfs init
5.	ipfs daemon


OPEN NEW TERMINAL ( ctrl + alt + T ): **for Dapp reference folder /for Dapp

1.	sudo apt-get install python3-pip
2.	sudo pip3 install virtualenv
3.	mkdir bcocDapp
4.	cd bcocDapp/
5.	virtualenv bcocVenv –python=python3.6
**bcocVenv folder will be created in bcocDapp

6.	source bcocVenv/bin/activate
7.	pip install Flask
8.	pip install flask-wtf / pip3 install flask-wtf
9.	pip install web3 / pip3 install web3
10.	pip install ipfsapi

Goto bcocDapp => Paste app.py , forms.py file.
Goto bcocTruffle => build => contracts => Copy Bcoc.json and paste it in bcocDapp folder.
Goto bcocDapp => Copy templates and static folder as it is.

**Make sure in ethereum, Default account is unlocked and Miner is started.

11.	python app.py

**OPEN browser and run localhost:5000 in address bar
![image](https://github.com/mahirbhatt/bcoc/assets/53952834/5479da44-f6e8-4e41-bbc2-ede24d5ad678)
