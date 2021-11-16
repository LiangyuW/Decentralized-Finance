
import config
from web3 import Web3

w3=Web3(Web3.HTTPProvider(config.INFURA_URL))

print(w3.eth.block_number)

balance = w3.eth.get_balance("0x6a0CC826F8784Fa3f11E69CB53406464c1489194")
ether_balance=w3.fromWei(balance, 'ether')

print("my ethereum balance: ", ether_balance)
