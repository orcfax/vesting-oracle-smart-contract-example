"""Publish a simple value to an Oracle on-chain."""

import argparse
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
    oracle_address,
    oracle_skey,
    oracle_vkey,
    save_transaction,
    script_address,
    submit_and_log_tx,
)

THRESHOLD: Final[str] = 6
AMOUNT: Final[str] = 2000000
VALIDITY_TIME: Final[str] = 300


def publish_datum(threshold: int):
    """Publish a datum on-chain."""

    logger.info("oracle address: %s", cexplorer_url(oracle_address))
    logger.info("script address: %s", cexplorer_url(script_address))

    owner = oracle_vkey.hash().to_primitive()
    hold_time = int(time() + VALIDITY_TIME) * 1000  # milliseconds.
    amount = Value(AMOUNT)

    logger.info(
        "publisher: %s :: hold time (ms): %s :: threshold: %s",
        oracle_address,
        hold_time,
        threshold,
    )
    # pylint: disable=E1123, E1120
    datum = PublishParams(owner=owner, hold_time=hold_time, threshold=threshold)

    builder = TransactionBuilder(context)
    builder.add_input_address(oracle_address)
    builder.add_output(TransactionOutput(script_address, amount=amount, datum=datum))
    try:
        signed_tx = builder.build_and_sign([oracle_skey], change_address=oracle_address)
    except TransactionFailedException as err:
        logger.error("error creating publish datum Tx: %s", err)
        sys.exit(1)

    save_transaction(signed_tx, "transactions/tx_deposit.signed")
    submit_and_log_tx(signed_tx)


def main():
    """Primary entry point for this script..."""

    parser = argparse.ArgumentParser(
        prog="OpShin oracle demo",
        description="creates an non-Orcfax Oracle smart contract using OpShin",
        epilog="for more information about Orcfax visit https://orcfax.io",
    )

    parser.add_argument(
        "--value",
        help="value to be published by the oracle (int)",
        required=False,
        default=THRESHOLD,
    )

    args = parser.parse_args()
    value = None
    try:
        value = int(args.value)
    except ValueError as err:
        logger.error(
            "ensure that the value submitted to the Oracle is a single integer: %s", err
        )
        sys.exit(1)
    logger.info("publishing a datum on-chain with value: %s", value)
    publish_datum(threshold=value)


if __name__ == "__main__":
    main()
