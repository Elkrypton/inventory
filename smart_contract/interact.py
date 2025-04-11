address = "0x54ad847e02b5f2b433ceee9f7faf60c87fd6e2d9"
abi = ""

contract_instance = w3.eth.contract(address=, abi=abi)

contract_instance.functions.storedValue().call()




