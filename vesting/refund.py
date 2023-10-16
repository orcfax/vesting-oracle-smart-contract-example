"""Return minimum ada value."""

import logging
import sys

from config import context
from contract import RefundRedeemer
from pycardano import Redeemer, TransactionBuilder, TransactionFailedException
from util import (
    collateral_address,
    collateral_skey,
    collateral_vkey,
    save_transaction,
    script_address,
    source_address,
    source_skey,
    source_vkey,
    submit_and_log_tx,
)

logger = logging.getLogger(__name__)


def refund_script():
    """Refund the deposited value for the local smart contract."""

    script_utxos = context.utxos(str(script_address))
    sc_utxo = ""
    utxo_to_spend = []
    for item in script_utxos:
        if item.output.script:
            sc_utxo = item
        elif item.output.datum:
            utxo_to_spend.append(item)

    if not sc_utxo:
        logger.info("smart contract UTxO not found!")
        sys.exit(0)

    if not utxo_to_spend:
        logger.info("no utxo to refund!")
        sys.exit(0)

    for claim_utxo in utxo_to_spend:
        collateral_utxo = context.utxos(str(collateral_address))[0]
        redeemer = Redeemer(RefundRedeemer())
        builder = TransactionBuilder(context)
        builder.reference_inputs.add(sc_utxo)
        builder.add_script_input(claim_utxo, redeemer=redeemer)
        builder.collaterals.append(collateral_utxo)
        builder.required_signers = [source_vkey.hash(), collateral_vkey.hash()]
        builder.validity_start = context.last_block_slot
        builder.ttl = builder.validity_start + 3600
        try:
            signed_tx = builder.build_and_sign(
                [source_skey, collateral_skey], change_address=source_address
            )
        except TransactionFailedException as err:
            logger.error("error creating deploy Tx: %s", err)
            continue
        save_transaction(signed_tx, "transactions/tx_refund.signed")
        submit_and_log_tx(signed_tx)


def main():
    """Primary entry point for this script..."""
    logger.info("returning all remaining deposits via refund script")
    refund_script()


if __name__ == "__main__":
    main()
