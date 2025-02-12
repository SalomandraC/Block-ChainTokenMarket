// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 < 0.8.19;
//import "@openzeppelin";

import {ERC20} from "./ERC20.sol";

contract Practick is ERC20 {

    address user;
    address token;

   constructor() ERC20("Dollar", "Doll"){
        _mint(msg.sender, 100);
   }

   struct TokenSTR {
        uint cost;
        uint count;
        string name;
        string shortName;
   }

    struct USRTokenSTR {
        uint balance;
        StatusVisiable Vis;
    }

    struct ReturnValues {
          address userAddress;
          uint QuequeValue;
          uint product;
     }

    enum StatusVisiable {Visiable, NonVisiable}

   event TokenInfo(address userAddress, uint cost, uint count, string name, string shortName);
   event BalanceCheck(address userAddress);

   mapping (address => bool) public accountsInSysystem;
   mapping (address => bytes32) public accountsInsert;
   mapping (address => bool) currentTokens; 
   mapping (address => mapping(address => bool)) public currentTokensForUser;
   mapping (address => mapping(address => USRTokenSTR)) public currentTokenBalance;
   mapping (address => address[]) public currentTokenAddress;
   mapping (address => TokenSTR) tokenStorage;
   mapping (address => mapping(address => uint)) public cellQueque;
   mapping (address => address[]) public keysByAddress;

   modifier isToken(){
        require(user != msg.sender, "User can't use token function");
        _;
   }

   modifier isOwner(){
        require(token != msg.sender, "Token can't use user function");
        _;
   }

   modifier tokenExist(address _token){
        require(currentTokens[_token], "No exist this token");
        _;
   }

   modifier tokenExistForUser(address _token) {
        require(currentTokensForUser[user][_token], "No exist this token");
        _;
   }

   function userToken() public isToken { 
        token = msg.sender;
   }

   function userUser() public isOwner {
        user = msg.sender;
   }

   function registration (address testyAddress, string memory str) public returns (bool result) {
        if (accountsInSysystem[testyAddress] == false){
           accountsInSysystem[testyAddress] = true;
           accountsInsert[testyAddress] = keccak256(abi.encodePacked(str));
           result = true;
           return result;
        }
        else{
            bytes32 hashedPassword = keccak256(abi.encodePacked(str));
            if (accountsInsert[testyAddress] == hashedPassword){
               result = true;
               return result;
            }
            else{
               result = false;
               return result;
            }
        }
   } 

   //for create normal balance 
   function addMoney(uint _money) public {
        _mint(msg.sender, _money);
   }

   function getBalanceToken() 
   public view returns(uint balance){
     balance = balanceOf(msg.sender);
   }

//_____________Token Functions______________

    

    //for basic stats of token
   function createToken(uint _cost, uint _count, string memory _name, string memory _shortname) 
   public 
   isToken 
   {
        require(currentTokens[token] == false, "Token with this address was created");
        TokenSTR memory newToken = TokenSTR({
            cost: _cost,
            count: _count,
            name: _name,
            shortName: _shortname
        });
        tokenStorage[token] = newToken;
        currentTokens[token] = true;
   }

    //for change token stats
   function changeToken(uint _cost, uint _count, string memory _shortname) 
   public 
   isToken 
   tokenExist (token) 
   {
        tokenStorage[token].count = _count;
        tokenStorage[token].cost = _cost;
        tokenStorage[token].shortName = _shortname;
   }

   //For sell token
   function approveCell()
     payable public 
     isToken
     tokenExist(token) 
     {
          uint i = keysByAddress[token].length - 1;
          if (i >= 0){
               address userAddress = keysByAddress[token][i];
               uint QuequeValue = cellQueque[token][userAddress];
               if (QuequeValue > 0 && (QuequeValue * tokenStorage[token].cost) <= balanceOf(token)){
                    approve(token, QuequeValue * tokenStorage[token].cost);
                    transferFrom(token, userAddress, QuequeValue * tokenStorage[token].cost);
                    tokenStorage[token].count += QuequeValue;
                    cellQueque[token][userAddress] = 0;
                    keysByAddress[token].pop();
               }
          }
     }

     //Steck of call
     function SteckInfo()
    public
    view
    isToken
    tokenExist(token)
    returns (ReturnValues[] memory)
     {
          address[] memory userAddresses = keysByAddress[token];
          uint length = userAddresses.length;
          ReturnValues[] memory result = new ReturnValues[](length);

          for (uint i = 0; i < length; i++) {
               address userAddress = userAddresses[i];
               uint QuequeValue = cellQueque[token][userAddress];
               uint cost = tokenStorage[token].cost;
               uint product = QuequeValue * cost;

               result[i] = ReturnValues({
                    userAddress: userAddress,
                    QuequeValue: QuequeValue,
                    product: product
               });
          }

          return result;
     }

   //Info about Token
   function infoToken() 
   public  
   view
   isToken 
   tokenExist(token) 
   returns (address, uint, uint, string memory, string memory)
     {
          return (token, tokenStorage[token].cost, tokenStorage[token].count, tokenStorage[token].name, tokenStorage[token].shortName);
     }

//_____________User Functions______________

    //Add token to User story
    function addToken (address _tokenAddress) 
    public 
    isOwner 
    tokenExist(_tokenAddress)
    {
        if (currentTokensForUser[user][_tokenAddress] == false){
            currentTokensForUser[user][_tokenAddress] = true;
            currentTokenBalance[user][_tokenAddress].balance = 0;
            currentTokenBalance[user][_tokenAddress].Vis = StatusVisiable.Visiable;
            currentTokenAddress[user].push(_tokenAddress);
        }
        else if (currentTokensForUser[user][_tokenAddress] == true && currentTokenBalance[user][_tokenAddress].Vis == StatusVisiable.NonVisiable){
            currentTokenBalance[user][_tokenAddress].Vis = StatusVisiable.Visiable;
        }
    }

    //Buy token to User
    function buyToken(address _tokenAddress, uint _count)
    payable public 
    isOwner 
    tokenExistForUser(_tokenAddress)
    {
        require(tokenStorage[_tokenAddress].cost * _count < balanceOf(user), "Maney ne ma");
        require(tokenStorage[_tokenAddress].count >= _count, "Tokens ne ma");
        approve(user, tokenStorage[_tokenAddress].cost * _count);
        transferFrom(user, _tokenAddress, tokenStorage[_tokenAddress].cost * _count);
        currentTokenBalance[user][_tokenAddress].balance += _count;
        tokenStorage[token].count = tokenStorage[token].count - _count;
    }

    //Sell token to User
    function sellToken(address _tokenAddress, uint _count)  
    payable public 
    isOwner 
    tokenExistForUser(_tokenAddress)
    {
        require(tokenStorage[_tokenAddress].cost * _count < balanceOf(_tokenAddress), "Maney u token ne ma");
        require(currentTokenBalance[user][_tokenAddress].balance >= _count, "Tokens u user ne ma");
        currentTokenBalance[user][_tokenAddress].balance -= _count;
        cellQueque[_tokenAddress][user] = _count;
        keysByAddress[_tokenAddress].push(user);
    }

    function hideToken(address _tokenAddress)
    public
    isOwner
    tokenExistForUser(_tokenAddress)
    {
        currentTokenBalance[user][_tokenAddress].Vis = StatusVisiable.NonVisiable;
    }

     function getCurrentBalanceToken() 
     isOwner
    public view returns(TokenSTR[] memory TokenBalance, uint balances)
     {
          uint count;
          for (uint i = 0; i < currentTokenAddress[user].length; i++) {
               if (currentTokenBalance[user][currentTokenAddress[user][i]].Vis == StatusVisiable.Visiable) {
                    count++;
               }
          }
          
          TokenSTR[] memory myTokenBalance = new TokenSTR[](count);
          
          uint index;
          for (uint i = 0; i < currentTokenAddress[user].length; i++) {
               if (currentTokenBalance[user][currentTokenAddress[user][i]].Vis == StatusVisiable.Visiable) {
                    address searchAddress = currentTokenAddress[user][i];
                    myTokenBalance[index] = tokenStorage[searchAddress];
                    balances = currentTokenBalance[user][searchAddress].balance;
                    index++;
               }
          }
           return (myTokenBalance, balances);
     }

}