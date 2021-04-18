import requests
import json

from . import jobcoin_config

class JobcoinClient(object):

	def get_balance_and_transactions(address):

		# TO DO: CHECK VARIABLE TYPE LOGIC
		# isinstance(address, str)

		"""
		address endpoint will never return 404 for an unused address, 
		it will return a balance of 0 and an empty list of transactions. 
		Numbers are returned as strings 
		No "fromAddress" indicates the Jobcoins were created on the Jobcoin website 
		Returns type class dict
		""" 

		response = requests.get(jobcoin_config.API_ADDRESS_URL+'/{}'.format(address))
		balance_and_transactions = json.loads(response.text)
		return balance_and_transactions

	def get_all_transactions_list():


		"""
		Numbers are returned as strings 
		No "fromAddress" indicates the Jobcoins were created on the Jobcoin website 
		Returns type class list
		"""

		response = requests.get(jobcoin_config.API_TRANSACTIONS_URL)
		all_transactions_list = json.loads(response.text)
		return all_transactions_list

	def send_jobcoins(fromAddress, toAddress, amount):

		# TO DO: CHECK VARIABLE TYPE LOGIC
		# isinstance(fromAddress, str)
		# isinstance(toAddress, str)
		# isinstance(amount, str)

		"""
		<Response [200]> "status": "OK"
		<Response [422]> "error": "Insufficient Funds"
		"""
		data = {'fromAddress':fromAddress, 'toAddress':toAddress, 'amount':amount}
		
		response = requests.post(jobcoin_config.API_TRANSACTIONS_URL, data = data)
		return response.status_code 