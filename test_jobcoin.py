#!/usr/bin/env python
import pytest
import re
from click.testing import CliRunner


from jobcoin import jobcoin_config
import cli


@pytest.fixture
def response():
    import requests
    return requests.get('https://jobcoin.gemini.com/')


def test_content(response):
    assert 'Hello!' in response.text


def test_cli_basic():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Welcome to the Jobcoin mixer' in result.output


def test_cli_creates_address():
    runner = CliRunner()
    address_create_output = runner.invoke(cli.main, input='1234,5678\nno\n').output
    address_re = re.compile(
        r'You may now send Jobcoins to address [0-9a-zA-Z]{32}. '
        'They will be mixed and sent to your destination addresses.'
    )
    assert address_re.search(address_create_output) is not None


# fn unit tests todo with static implementation:
# fn: poll_and_process_deposit -- assertions on return dict {'expected_deposit_received':'true', 'depositAddress_balance':depositAddress_balance, 'expectedAmount':expectedAmount}
# fn: create_coins_and_address(toAddress) -- assertions on response: response = requests.post(jobcoin_config.CREATE_URL, data = data)
# fn: mix_house_accounts(self, JCM_house_accounts) -- assertion on house_account_transaction_record
# fn: create_accounts_to_proxy_distribution(self, number_of_accounts_to_create) -- validates on response
# fn: distribute_proxy_payments(self, JCM_accounts_payable, JCM_house_accounts, distribution_accounts, amount) -- assertions on distribution_account_data
# fn: send_proxy_payments_to_user_accounts(self, distribution_accounts, user_accounts) -- validates on response

# val unit tests to do with static implementation:
# val: number_of_accounts_to_create from jobcoin.jobcoin_config