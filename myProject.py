import web3
import json

class API:
    def __init__(self, account_address):
        self.w3 = web3.Web3(web3.HTTPProvider("HTTP://127.0.0.1:8584"))
        print("Connection to Ethereum:", self.w3.is_connected())
        self.account = web3.Web3.to_checksum_address(account_address)

        self.contract_address = web3.Web3.to_checksum_address('0x91236502dBF1dec271066B96258F7DB396ed164e')

        with open('abi.json', 'r') as f:
            abi = json.load(f)
        
        # Initialize the contract
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=abi)
    
    def user_user(self):
        try:
            tx_hash = self.contract.functions.userUser().transact({
                'from': self.account,
                'gas': 2000000,
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt['status'] == 1:
                return "Transaction successful"
            else:
                return "Transaction failed"
        except Exception as e:
            print("Error in user_user:", e)
            return None
    
    def user_token(self, token_address):
        #token_address_checksum = web3.Web3.to_checksum_address(token_address)
        try:
            tx_hash = self.contract.functions.userToken().transact({
                'from': self.account,
                'gas': 2000000,
                'nonce': self.w3.eth.get_transaction_count(self.account),
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt['status'] == 1:
                return "Transaction successful"
            else:
                return "Transaction failed"
        except Exception as e:
            print("Error in user_token:", e)
            return None
    
    def create_token(self, cost, count, name, short_name):
        try:
            tx_hash = self.contract.functions.createToken(cost, count, name, short_name).transact({
                'from': self.account,
                'gas': 2000000,
                'nonce': self.w3.eth.get_transaction_count(self.account),
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt['status'] == 1:
                return "Transaction successful"
            else:
                return "Transaction failed"
        except Exception as e:
            print("Error in create_token:", e)
            return None
        
    def change_token(self, cost, count, short_name):
        try:
            tx_hash = self.contract.functions.changeToken(cost, count, short_name).transact({
                'from': self.account,
                'gas': 2000000,
                'nonce': self.w3.eth.get_transaction_count(self.account),
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt['status'] == 1:
                return "Transaction successful"
            else:
                return "Transaction failed"
        except Exception as e:
            print("Error in change_token", e)
            return None
            
    def get_balance_token(self):
        try:
            balance = self.contract.functions.getBalanceToken().call({
                'from': self.account,
            })
            return balance
        except Exception as e:
            print("Error in get_balance_token", e)
            return None
    
    
    
    def add_token(self, token_address):
        token_address_checksum = web3.Web3.to_checksum_address(token_address)
        try:
            tx_hash = self.contract.functions.addToken(token_address_checksum).transact({
                'from': self.account,
                'gas': 2000000,
                'nonce': self.w3.eth.get_transaction_count(self.account),
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt['status'] == 1:
                return "Transaction successful"
            else:
                return "Transaction failed"
        except Exception as e:
            print("Error in add_token:", e)
            return None
    
    def buy_token(self, token_address, count):
        token_address_checksum = web3.Web3.to_checksum_address(token_address)
        try:
            tx_hash = self.contract.functions.buyToken(token_address_checksum, count).transact({
                'from': self.account,
                'gas': 2000000,
                'nonce': self.w3.eth.get_transaction_count(self.account),
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt['status'] == 1:
                return "Transaction successful"
            else:
                return "Transaction failed"
        except Exception as e:
            print("Error in buy_token:", e)
            return None
        
    def sell_token(self, token_address, count):
        token_address_checksum = web3.Web3.to_checksum_address(token_address)
        try:
            tx_hash = self.contract.functions.sellToken(token_address_checksum, count).transact({
                'from': self.account,
                'gas': 2000000,                
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt['status'] == 1:
                return "Transaction successful"
            else:
                return "Transaction failed"
        except Exception as e:
            print("Error in buy_token:", e)
            return  None
        
    
    def approve_cell(self):
        try:
            tx_hash = self.contract.functions.approveCell().transact({
                'from': self.account,
                'gas': 2000000,
                'nonce': self.w3.eth.get_transaction_count(self.account),
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt['status'] == 1:
                return "Transaction successful"
            else:
                return "Transaction failed"
        except Exception as e:
            print("Error in approve_cell:", e)
            return None
    
    def get_current_balance_token(self):
        try:
            # Вызываем функцию getCurrentBalanceToken из контракта
            result = self.contract.functions.getCurrentBalanceToken().call({
                'from': self.account,
            })
            
            token_balance_array = result[0] 
            balances = result[1]  
            
            token_balance_list = []
            for token in token_balance_array:
                token_balance_list.append({
                    'cost': token[0],  
                    'count': token[1], 
                    'name': token[2], 
                    'shortName': token[3] 
                })
            
            return {
                'tokenBalance': token_balance_list,
                'balances': balances
            }
        except Exception as e:
            print("Error in get_current_balance_token:", e)
            return None
        
        
    def reg_function(self, address, password):
        token_address_checksum = web3.Web3.to_checksum_address(address)
        try:
            flag = self.contract.functions.reg_function(address, password).transact({
                'from': self.account,
                'gas': 2000000,
            })      
            return flag
        except Exception as e:
            return False
        
        
    def add_money(self, amount):
        try:
            tx_hash = self.contract.functions.addMoney(amount).transact({
                'from': self.account,
                'gas': 2000000,
                'nonce': self.w3.eth.get_transaction_count(self.account),
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            # Проверяем статус транзакции
            if receipt['status'] == 1:
                return "Transaction successful"
            else:
                return "Transaction failed"
        except Exception as e:
            print("Error in add_money:", e)
            return "Transaction failed"
        
    def steck_info(self):
        try:
            result = self.contract.functions.SteckInfo().call({'from': self.account})

            if result is not None:
                token_stack_list = []
                for token in result:
                    token_stack_list.append({
                        'userAddress': token[0],
                        'QuequeValue': token[1],
                        'product': token[2],
                    })

                return {'tokenBalance': token_stack_list}
        except Exception as e:
            print("Error in steck_info:", e)
            return None
        
    def info_token(self):
        try:
            result = self.contract.functions.infoToken().call({
                'from': self.account,
            })
            
            info_token_dict = {
                'tokenAddress': result[0],
                'cost': result[1],
                'count': result[2],
                'name': result[3],
                'shortName': result[4]
            }
            
            return info_token_dict
        except Exception as e:
            print("Error in info_token:", e)
            return None
        
    def hide_token(self, token_address):
        token_address_checksum = web3.Web3.to_checksum_address(token_address)
        try:
            tx_hash = self.contract.functions.hideToken(token_address_checksum).transact({
                'from': self.account,
                'gas': 2000000
            })
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt['status'] == 0:
                return "Trunsaction successful"
            else:
                return "Trunsaction failed"
        except Exception as e:
            print("Error in hide_token", e)
            return None
      
if __name__ == "__main__":
    api_user = API('0x8DBd788b136827BEA4AcF036E95D911fd6e4b341')
    api_token_creator = API('0xF87Ae16806b3a0e702A08C183d1d6B899e7Ef46B')

    token_creator_receipt = api_token_creator.user_token(api_token_creator.account)
    print("UserToken receipt:", token_creator_receipt)
    
    token_reg = api_token_creator.reg_function(api_token_creator.account, "123")
    print(token_reg)

    token_reg_1 = api_token_creator.reg_function(api_token_creator.account, "1234")
    print(token_reg_1)
    
    token_reg_2 = api_token_creator.reg_function(api_token_creator.account, "123")
    print(token_reg_2)

    create_token_receipt = api_token_creator.create_token(10, 1000, "Test", "TT")
    print("CreateToken receipt:", create_token_receipt)



    change_token_receipt = api_token_creator.change_token(10, 1000, "SAS")
    print("ChangeToken receipt:", change_token_receipt)

    user_receipt = api_user.user_user()
    print("UserUser receipt:", user_receipt)

    add_token_receipt = api_user.add_token(api_token_creator.account)
    print("AddToken receipt:", add_token_receipt)

    give_money_user = api_user.add_money(100)
    print("Add_money receipt:", give_money_user)

    give_balance_token = api_user.get_balance_token()
    print("Give_balance_token:", give_balance_token)

    buy_token_receipt = api_user.buy_token(api_token_creator.account, 3)
    print("BuyToken receipt:", buy_token_receipt)

    current_balance_after_sale = api_user.get_current_balance_token()
    print("Current token balance after buy:", current_balance_after_sale)

    cell_token_receipt = api_user.sell_token(api_token_creator.account, 2)
    print("BuyToken receipt:", buy_token_receipt)

    steck_info_receipt = api_token_creator.steck_info()
    print("Steck info:", steck_info_receipt)

    approve_cell_receipt = api_token_creator.approve_cell()
    print("ApproveCell receipt:", approve_cell_receipt)

    current_balance_after_sale = api_user.get_current_balance_token()
    print("Current token balance after sale:", current_balance_after_sale)