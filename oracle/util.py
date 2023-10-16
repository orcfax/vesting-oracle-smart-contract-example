"""Utility functions for the oracle example."""

import json

from config import (
    collateral_address_skey,
    context,
    contract_cbor,
    network,
    oracle_address_skey,
    tx_template,
)
from logger import logger
from pycardano import (
    Address,
    PaymentSigningKey,
    PaymentVerificationKey,
    PlutusV2Script,
    Transaction,
    plutus_script_hash,
)

with open(contract_cbor, "r", encoding="utf-8") as f:
    script_hex = f.read()

contract_script = PlutusV2Script(bytes.fromhex(script_hex))

script_hash = plutus_script_hash(contract_script)
script_address = Address(script_hash, network=network)

oracle_skey = PaymentSigningKey.load(oracle_address_skey)
oracle_vkey = PaymentVerificationKey.from_signing_key(oracle_skey)
oracle_address = Address(oracle_vkey.hash(), network=network)

collateral_skey = PaymentSigningKey.load(collateral_address_skey)
collateral_vkey = PaymentVerificationKey.from_signing_key(collateral_skey)
collateral_address = Address(collateral_vkey.hash(), network=network)


def save_transaction(trans: Transaction, file: str):
    """Save transaction helper function saves a Tx object to file."""
    logger.info(
        "saving Tx to: %s , inspect with: 'cardano-cli transaction view --tx-file %s'",
        file,
        file,
    )
    tx = tx_template.copy()
    tx["cborHex"] = trans.to_cbor().hex()
    with open(file, "w", encoding="utf-8") as tf:
        tf.write(json.dumps(tx, indent=4))


def cexplorer_url(addr: str) -> str:
    """Return a cexplorer URL to the caller."""
    return f"https://preprod.cexplorer.io/address/{addr}"


def cexplorer_tx_url(tx_id: str) -> str:
    """Return a transaction UL to the caller."""
    return f"https://preprod.cexplorer.io/tx/{tx_id}"


def submit_and_log_tx(signed_tx: Transaction):
    """Submit and log a signed transaction.

    E.g. provide information form the Tx that is generic to all.
    """
    context.submit_tx(signed_tx.to_cbor())
    logger.info(
        "fee %s ADA",
        int(signed_tx.transaction_body.fee) / 1000000,
    )
    logger.info(
        "output %s ADA",
        int(signed_tx.transaction_body.outputs[0].amount.coin) / 1000000,
    )
    logger.info("transaction submitted: %s", cexplorer_tx_url(signed_tx.id))
