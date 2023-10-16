"""Undeploy the oracle smart contract."""

import sys

from config import context
from contract import RefundRedeemer
from logger import logger
from pycardano import Redeemer, TransactionBuilder, TransactionFailedException
from util import (
    cexplorer_url,
    collateral_address,
    collateral_skey,
    collateral_vkey,
    oracle_address,
    oracle_skey,
    oracle_vkey,
    save_transaction,
    script_address,
    submit_and_log_tx,
)


def undeploy_script():
    """Undeploy the oracle smart contract.

    NB. if the smart contract has been deployed multiple times, the
    script will continue to decrement the number on chain each
    subsequent run, and return the spent UTxO to the source wallet.
    """
    logger.info("looking for script UTxOs at %s", script_address)
    script_utxos = context.utxos(script_address)
    sc_utxo = ""
    utxo_to_spend = ""
    logger.info("script UTxOs: %s", len(script_utxos))
    for item in script_utxos:
        if item.output.script:
            sc_utxo = item
            utxo_to_spend = item
            break
    if not sc_utxo or not utxo_to_spend:
        logger.info("no script input or not utxo to spend!")
        sys.exit(1)
    logger.info("finding collateral utxo and creating Tx")
    logger.error("collateral address: %s", cexplorer_url(collateral_address))
    logger.error("oracle address: %s", cexplorer_url(oracle_address))
    collateral_utxo = context.utxos(collateral_address)[0]
    redeemer = Redeemer(RefundRedeemer())
    builder = TransactionBuilder(context)
    builder.add_script_input(sc_utxo, redeemer=redeemer)
    builder.collaterals.append(collateral_utxo)
    builder.validity_start = context.last_block_slot
    builder.ttl = builder.validity_start + 3600
    builder.required_signers = [oracle_vkey.hash(), collateral_vkey.hash()]
    try:
        signed_tx = builder.build_and_sign(
            [oracle_skey, collateral_skey], change_address=oracle_address
        )
    except TransactionFailedException as err:
        logger.error(
            "error creating undeploy Tx (see smart contract conditions): %s", err
        )
        sys.exit(1)
    save_transaction(signed_tx, "transactions/tx_undeploy.signed")
    submit_and_log_tx(signed_tx)


def main():
    """Primary entry point for this script..."""
    logger.info("running undeploy for oracle smart contract")
    undeploy_script()


if __name__ == "__main__":
    main()
