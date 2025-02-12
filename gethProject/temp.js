personal.unlockAccount(eth.accounts[0], "1", 0); 
personal.unlockAccount(eth.accounts[1], "1", 0); 
personal.unlockAccount(eth.accounts[2], "1", 0); 
miner.setEtherbase(eth.accounts[0]); 
miner.start(3); 
