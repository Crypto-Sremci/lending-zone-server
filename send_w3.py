from web3 import Web3
import json

usdc_address = "0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8"

def send_price(address, id, price):
    # Replace with your RPC address
    rpc_address = 'https://sepolia.drpc.org'

    # Connect to the node
    w3 = Web3(Web3.HTTPProvider(rpc_address))

    # Check if connected
    if not w3.is_connected():
        raise Exception("Could not connect to the Ethereum node")

    with open("NftOracle.json") as f:
        contract = json.load(f)
        contract_address = contract["address"]
        contract_abi = contract["abi"]

    # Initialize the contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Define the function you want to send
    function_name = 'setPrice'
    function_params = [usdc_address, address, int(id), price]  # Add the required parameters

    # Account details
    with open("credentials.json") as f:
        cred = json.load(f)
        sender_address = cred["public_key"]
        private_key = cred["private_key"]

    # Create the transaction
    transaction = contract.functions.setPrice(usdc_address, address, int(id), price).build_transaction({
        'from': sender_address,
        'nonce': w3.eth.get_transaction_count(sender_address),
        'gas': 2000000,  # Adjust as necessary
        'gasPrice': w3.to_wei('50', 'gwei')
    })

    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Send the transaction
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction receipt
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    # Print the transaction receipt
    print(f'Transaction receipt: {txn_receipt}')
