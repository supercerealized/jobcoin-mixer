#!/usr/bin/env python
import uuid
import sys

import click

from jobcoin import jobcoin
client = jobcoin.JobcoinClient()


@click.command()
# option for sending set ammount from multiple places or in multiple transactions
def main(args=None):
    
    print('Welcome to the Jobcoin mixer!\n')
    while True:
        addresses = click.prompt(
            'Please enter a comma-separated list of new, unused Jobcoin '
            'addresses where your mixed Jobcoins will be sent.',
            prompt_suffix='\n[blank to quit] > ',
            default='',
            show_default=False)
        if addresses.strip() == '':
            sys.exit(0) # use click
        partial_deposits = click.prompt(
            '\nRun in partial deposit mode?: ',
            prompt_suffix=' > ',
            default='no',
            show_default=True)
        if partial_deposits != 'no':
            expectedAmount = click.prompt(
                '\nEnter the total amount of Jobcoins you will be mixing: ')
        else:
            expectedAmount = None

        depositAddress = uuid.uuid4().hex
        depositAddress_status = client.poll_and_process_deposit(validate_address = True)
        if depositAddress_status == 'account_in_use':
            while depositAddress_status == 'account_in_use':
                depositAddress = uuid.uuid4().hex
                depositAddress_status = client.poll_and_process_deposit(validate_address = True)

        click.echo(
            '\nYou may now send Jobcoins to address {depositAddress}. They '
            'will be mixed and sent to your destination addresses.\n'
              .format(depositAddress=depositAddress))

        depositAddress_transaction = client.poll_and_process_deposit(
            depositAddress = depositAddress,
            expectedAmount = expectedAmount,
            keeping_open = False,
            validate_address = False)
        print(depositAddress_transaction) # DEBUG
        
        if depositAddress_transaction['expected_deposit_received'] == 'false':
            click.echo(
                '\n - Partial deposit received! Still awaiting: '
                + str(depositAddress_transaction['still_awaiting'])
                + ' of '
                + str(depositAddress_transaction['expectedAmount']))
            
            while depositAddress_transaction['expected_deposit_received'] == 'false':
                        depositAddress_transaction = \
                        client.poll_and_process_deposit(
                        depositAddress = depositAddress,
                        expectedAmount = expectedAmount,
                        keeping_open = True,
                        validate_address = False)
                        print(depositAddress_transaction) # DEBUG
        if depositAddress_transaction['expected_deposit_received'] == 'true':
            click.echo(
                '\n - Jobcoins received! They will be mixed and sent to your destination address(es)')
            # send to mixer
        send_to_house_account_status = jobcoin.send_jobcoins(depositAddress, 'JCM_intake', depositAddress_transaction['depositAddress_balance'] )

if __name__ == '__main__':
    sys.exit(main())



