import json
from pathlib import Path
from web3 import Web3

# Connect to a local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

def get_contract_abi(name):
    certification_json_path = Path(f'../build/contracts/{name}.json')

    try:
        with open(certification_json_path, 'r') as json_file:
            certification_data = json.load(json_file)
            return certification_data.get('abi', [])
    except FileNotFoundError:
        print(f"Error: {certification_json_path} not found.")
        return []

deployment_config_fpath = Path("../deployment_config.json")
with open(deployment_config_fpath, 'r') as json_file:
    address_data = json.load(json_file)
    
basic_contract_address = address_data.get('BasicRecord')
lightweight_contract_address = address_data.get('LightweightRecord')

# Interact with the smart contract
basic_contract = w3.eth.contract(address=basic_contract_address, abi=get_contract_abi('BasicRecord'))
lightweight_contract = w3.eth.contract(address=lightweight_contract_address, abi=get_contract_abi('LightweightRecord'))
