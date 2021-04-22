# Replace the URL below
API_BASE_URL = 'http://jobcoin.gemini.com/undaunted-gossip/api'
API_ADDRESS_URL = '{}/addresses'.format(API_BASE_URL)
API_TRANSACTIONS_URL = '{}/transactions'.format(API_BASE_URL)

CREATE_URL = 'https://jobcoin.gemini.com/undaunted-gossip/create'
# *not an api endpoint

# when looking for house accounts
# dependency on naming convention: 'JCM_HA*'
JCM_HOUSE_ACCOUNTS = [
'JCM_HA0',
'JCM_HA1',
'JCM_HA2',
'JCM_HA3',
'JCM_HA4',
'JCM_HA5',
'JCM_HA6',
'JCM_HA7',
'JCM_HA8',
'JCM_HA9'
]

# distribution accounts
# dynamic generation of accounts to proxy distribution
number_of_accounts_to_create = 3
