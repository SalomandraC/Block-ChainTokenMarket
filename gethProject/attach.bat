@echo off
echo personal.unlockAccount(eth.accounts[0], "1", 0); > temp.js
echo personal.unlockAccount(eth.accounts[1], "1", 0); >> temp.js
echo personal.unlockAccount(eth.accounts[2], "1", 0); >> temp.js
echo miner.setEtherbase(eth.accounts[0]); >> temp.js
echo miner.start(3); >> temp.js
geth attach "http://127.0.0.1:8584" < temp.js
del temp.js
pause
