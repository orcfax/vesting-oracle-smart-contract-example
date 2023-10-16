"""Deploy the oracle smart contract on-chain."""

import sys
from time import time
from typing import Final

from config import context
from contract import PublishParams
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
    oracle_address,
    oracle_skey,
    oracle_vkey,
    save_transaction,
    script_address,
    submit_and_log_tx,
)


def deploy_script():
    """Deploy a compiled smart-contract on-chain."""
    owner = oracle_vkey.hash().to_primitive()
    min_ada_requirement: Final[str] = 30000000
    hold_time = int(time()) * 1000  # milliseconds.
    amount = Value(min_ada_requirement)
    # pylint: disable=E1123, E1120
    datum = PublishParams(owner=owner, hold_time=hold_time, threshold=0)
    builder = TransactionBuilder(context)
    builder.add_input_address(oracle_address)
    logger.info("deploying to smart contract: %s", script_address)
    logger.info("cexplorer url: %s", cexplorer_url(script_address))
    builder.add_output(
        TransactionOutput(
            script_address, amount=amount, datum=datum, script=contract_script
        )
    )
    try:
        signed_tx = builder.build_and_sign([oracle_skey], change_address=oracle_address)
    except TransactionFailedException as err:
        logger.error("error creating deploy Tx: %s", err)
        sys.exit(1)
    save_transaction(signed_tx, "transactions/tx_deploy.signed")
    submit_and_log_tx(signed_tx)


def main():
    """Primary entry point for this script..."""
    logger.info("running deploy for oracle smart contract")
    deploy_script()


if __name__ == "__main__":
    main()
