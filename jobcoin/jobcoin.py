import requests
import json

from time import sleep

from . import jobcoin_config

def get_balance_and_transactions(address):
	# Base endpoint utility

	# TO DO: CHECK VARIABLE TYPE
	# isinstance(address, str)

	"""
	address endpoint will never return 404 for an unused address, 
	it will return a balance of 0 and an empty list of transactions. 
	Numbers are returned as strings 
	No 'fromAddress' indicates the Jobcoins were created on the Jobcoin website 
	Returns type class dict
	""" 
	response = requests.get(jobcoin_config.API_ADDRESS_URL+'/{}'.format(address))
	balance_and_transactions = json.loads(response.text)
	return balance_and_transactions

def get_all_transactions_list():
	# Base endpoint utility


	"""
	Numbers are returned as strings 
	No 'fromAddress' indicates the Jobcoins were created on the Jobcoin website 
	Returns type class list
	"""
	response = requests.get(jobcoin_config.API_TRANSACTIONS_URL)
	all_transactions_list = json.loads(response.text)
	return all_transactions_list

def send_jobcoins(fromAddress, toAddress, amount):
	# Base endpoint utility

	# TO DO: CHECK VARIABLE TYPE
	# isinstance(fromAddress, str)
	# isinstance(toAddress, str)
	# isinstance(amount, str)

	"""
	<Response [200]> 'status': 'OK'
	<Response [422]> 'error': 'Insufficient Funds'
	"""
	data = {'fromAddress':fromAddress, 'toAddress':toAddress, 'amount':amount}
	
	response = requests.post(jobcoin_config.API_TRANSACTIONS_URL, data = data)
	return response.status_code 

class JobcoinClient(object):

	def poll_and_process_deposit(self, 
				depositAddress = None,
				expectedAmount = None,
				keeping_open = False,
				validate_address = False):
		# can be passed with only the validate_address param set to true before passing deposit address to user

		depositAddress_data = get_balance_and_transactions(depositAddress)
		depositAddress_balance = depositAddress_data['balance']
		if depositAddress_data['transactions'] != [] and keeping_open is False:
			return 'account_in_use'
		if validate_address is True:
			return 'account_empty'
		else:
			initial_depositAddress_balance = depositAddress_balance
			while initial_depositAddress_balance == depositAddress_balance:
				print('checking balance')
				depositAddress_balance = get_balance_and_transactions(depositAddress)['balance']
				sleep(10)
			if float(depositAddress_balance) - float(initial_depositAddress_balance) == float(expectedAmount):
				return {'expected_deposit_received':'true',
				'depositAddress_balance':depositAddress_balance,
				'expected':expectedAmount}
			else:
				delta = float(expectedAmount) - float(depositAddress_balance)
				return {'expected_deposit_received':'false',
				'depositAddress_balance':depositAddress_balance,
				'expected':expectedAmount,
				'still_awaiting':delta}



