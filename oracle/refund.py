"""Refund the value deposited with the datum UTxO."""

import sys

from config import context
from contract import RefundRedeemer
from logger import logger
from pycardano import Redeemer, TransactionBuilder, TransactionFailedException
from util import (
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


def refund_utxo():
    """Refund the UTxO (providing the time has elapsed on-chain)."""

    logger.info("script address: %s", script_address)
    script_utxos = context.utxos(str(script_address))
    sc_utxo = []
    utxo_to_spend = []
    for item in script_utxos:
        if item.output.script:
            sc_utxo.append(item)
        elif item.output.datum:
            utxo_to_spend.append(item)

    if not sc_utxo:
        logger.info("smart contract UTxO not found!")
        sys.exit(1)

    if not utxo_to_spend:
        logger.info("no utxo to refund!")
        sys.exit(1)

    logger.info("UTxO with script: %s", len(sc_utxo))
    logger.info("UTxO with datum: %s", len(utxo_to_spend))

    for published_utxo in utxo_to_spend:
        collateral_utxo = context.utxos(str(collateral_address))[0]
        redeemer = Redeemer(RefundRedeemer())
        builder = TransactionBuilder(context)
        builder.reference_inputs.add(sc_utxo[0])
        builder.add_script_input(published_utxo, redeemer=redeemer)
        builder.collaterals.append(collateral_utxo)
        builder.required_signers = [oracle_vkey.hash(), collateral_vkey.hash()]
        builder.validity_start = context.last_block_slot
        builder.ttl = builder.validity_start + 3600
        try:
            signed_tx = builder.build_and_sign(
                [oracle_skey, collateral_skey], change_address=oracle_address
            )
        except TransactionFailedException as err:
            logger.error(
                "error creating refund Tx (see smart contract conditions): %s", err
            )
            continue
        save_transaction(signed_tx, "transactions/tx_refund.signed")
        submit_and_log_tx(signed_tx)


def main():
    """Primary entry point for this script..."""
    logger.info("refunding all utxo that published datum")
    refund_utxo()


if __name__ == "__main__":
    main()
