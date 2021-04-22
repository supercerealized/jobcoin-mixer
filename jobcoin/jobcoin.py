import requests
import datetime
import json
import uuid

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

def create_coins_and_address(toAddress):
	'''
	this is not functionality exposed/documented in the api.
	this is equivilent to interacting with the "Create 50 New Jobcoins" 
	button on the Jobcoin website
	CREATE_URL = 'https://jobcoin.gemini.com/undaunted-gossip/create?address=ADDRESS'
	'''
	data = {"address":toAddress}
	response = requests.post(jobcoin_config.CREATE_URL, data = data)
	return response

class JobcoinMixerClient(object):

	def poll_and_process_deposit(self, 
				depositAddress = None,
				expectedAmount = None,
				keeping_open = False,
				validate_address = False):
		# fn overloaded; can be passed with only the depositAddress and validate_address param set to true before passing deposit address to user

		depositAddress_data = get_balance_and_transactions(depositAddress)
		depositAddress_balance = depositAddress_data['balance']
		if depositAddress_data['transactions'] != [] and keeping_open is False:
			return 'account_in_use'
		if validate_address is True:
			return 'account_empty'

		initial_depositAddress_balance = depositAddress_balance
		while initial_depositAddress_balance == depositAddress_balance:
			print('Checking balance @ depositAddress: 'depositAddress)
			depositAddress_balance = get_balance_and_transactions(depositAddress)['balance']
			sleep(5)
		if expectedAmount != None:
		# amount specified - poll depositAccount until the expectedAmount is reached
			if float(depositAddress_balance) - float(initial_depositAddress_balance) == float(expectedAmount):
				return {'expected_deposit_received':'true',
				'depositAddress_balance':depositAddress_balance,
				'expectedAmount':expectedAmount}
			else:
				delta = float(expectedAmount) - float(depositAddress_balance)
				return {'expected_deposit_received':'false',
				'depositAddress_balance':depositAddress_balance,
				'expectedAmount':expectedAmount,
				'still_awaiting':delta}
		else:
		# poll and return after first transaction
			return {'expected_deposit_received':'true',
			'depositAddress_balance':depositAddress_balance,
			'expectedAmount':expectedAmount}

	def distribute_to_house_accounts(self, intakeAddress, amount, JCM_house_accounts):
		distribution_start_timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4]+'Z'
		house_account_distribution = float(amount) / len(JCM_house_accounts)

		for house_account in JCM_house_accounts:
			transaction_status = send_jobcoins(intakeAddress, house_account, str(house_account_distribution))
			print(str(transaction_status)) # DEBUG
			if transaction_status == 422:
				print('Insufficient funds') # DEBUG
				get_balance_and_transactions(house_account) # DEBUG
			else:
				if transaction_status == 200:
					print('successfully transfered {} to {}'.format(str(house_account_distribution), house_account))
					get_balance_and_transactions(house_account) # DEBUG
				else:
					get_balance_and_transactions(house_account) # DEBUG
		distribution_stop_timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4]+'Z'
		distribution_record = get_balance_and_transactions(intakeAddress)


	def mix_house_accounts(self, JCM_house_accounts):
		mix_house_accounts_start_timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4]+'Z'
		house_account_transaction_record = list()
		for house_account in JCM_house_accounts:
			house_account_record = get_balance_and_transactions(house_account)
			house_account_balance = house_account_record['balance']
			half_of_account_balance = int(float(house_account_balance) / 2)
			house_account_distribution = int(float(half_of_account_balance) / (len(JCM_house_accounts) - 1))
			
			print("Mixing...")
			for other_house_accounts in JCM_house_accounts:
				if house_account != other_house_accounts:
					transaction_status = send_jobcoins(house_account, other_house_accounts, str(house_account_distribution))
				else:
					pass
		transaction_record = get_all_transactions_list()
		for record in transaction_record:
			try:
				if 'JCM_HA' in record['fromAddress'] and record['timestamp'] > mix_house_accounts_start_timestamp:
					house_account_transaction_record.append(str(record))
				else:
					pass
			except KeyError as e:
				pass
		return house_account_transaction_record

	def create_accounts_to_proxy_distribution(self, number_of_accounts_to_create):
		
		distribution_accounts = list()
		for account in range(number_of_accounts_to_create):
			accountAddress = uuid.uuid4().hex
			response = create_coins_and_address(accountAddress)
			distribution_accounts.append(accountAddress)
			print('[-] distribution account created {}'.format(str(response)))
		return distribution_accounts

	def distribute_proxy_payments(self, JCM_accounts_payable, JCM_house_accounts, distribution_accounts, amount):
		# not utilizing JCM_accounts_payable here - going directly from house accounts to distribution accounts

		amount_distribution = float(amount) / len(distribution_accounts)
		amount_collection = amount_distribution / len(JCM_house_accounts)
		for distribution_account in distribution_accounts:
			print('[-] collecting funds for distribution_account: {}'.format(str(distribution_account)))
			for house_account in JCM_house_accounts:
				print('[-] collecting {} from {}'.format(str(amount_collection), house_account))
				send_jobcoins(house_account, distribution_account, str(amount_collection))
		distribution_account_data = {'amount_distribution': str(amount_distribution),'distribution_accounts': distribution_accounts}
		return distribution_account_data

	def send_proxy_payments_to_user_accounts(self, distribution_accounts, amount_distribution, user_accounts):
		
		for distribution_account in distribution_accounts:
			distribution_account_record = get_balance_and_transactions(distribution_account)
			distribution_account_balance = distribution_account_record['balance']

			if amount_distribution <= distribution_account_balance:
				amount_distribution_per_user_account = float(amount_distribution) / len(user_accounts)
				for user_account in user_accounts:
					print('[-] sending to user account {} from distribution account {}'.format(user_account,distribution_account))
					transaction_status = send_jobcoins(distribution_account, user_account, str(amount_distribution_per_user_account))
					if transaction_status == 422:
						return {'transaction_failed_insufficient_funds':str(distribution_account)}
					else:
						pass
		return
		