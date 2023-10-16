"""Deploy the vesting smart contract...."""


import sys
from time import time

from config import context
from contract import VestingParams
from logger import logger
from pycardano import (
    TransactionBuilder,
    TransactionFailedException,
    TransactionOutput,
    Value,
)
from util import (
    cexplorer_url,
    contract_script,
    save_transaction,
    script_address,
    source_address,
    source_skey,
    source_vkey,
    submit_and_log_tx,
)


def deploy_script():
    """Deploy smart contract."""
    deployer = source_vkey.hash().to_primitive()
    fee_address = source_address.payment_part.to_primitive()

    threshold = 0
    fee = 2000000
    deadline = int(time()) * 1000
    amount = Value(50000000)
    datum = VestingParams(
        source=deployer,
        beneficiary=deployer,
        fee_address=fee_address,
        fee=fee,
        deadline=deadline,
        threshold=threshold,
    )
    builder = TransactionBuilder(context)
    builder.add_input_address(source_address)
    logger.info("deploying to smart contract: %s", script_address)
    logger.info("cexplorer url: %s", cexplorer_url(script_address))
    builder.add_output(
        TransactionOutput(
            script_address, amount=amount, datum=datum, script=contract_script
        )
    )
    try:
        signed_tx = builder.build_and_sign([source_skey], change_address=source_address)
    except TransactionFailedException as err:
        logger.error("error creating deploy Tx: %s", err)
        sys.exit(1)
    save_transaction(signed_tx, "transactions/tx_deploy.signed")
    submit_and_log_tx(signed_tx)


def main():
    """Primary entry point for this script..."""
    logger.info("running deploy for vesting smart contract")
    deploy_script()


if __name__ == "__main__":
    main()
