"""Claim the value from a smart contract when certain conditions are
met.
"""
import sys

import cbor2
from config import context, network, oracle_address
from contract import ClaimRedeemer, PublishParams, VestingParams
from logger import logger
from pycardano import (
    Address,
    Redeemer,
    TransactionBuilder,
    TransactionFailedException,
    TransactionOutput,
    VerificationKeyHash,
)
from util import (
    beneficiary_address,
    beneficiary_skey,
    beneficiary_vkey,
    collateral_address,
    collateral_skey,
    collateral_vkey,
    save_transaction,
    script_address,
    submit_and_log_tx,
)


def get_datum(utxo):
    """Get the datum from a UTxO."""
    return cbor2.loads(utxo.output.datum.cbor)


def get_utxo_timestamp(utxo):
    """Get the utxo timestamp."""
    datum = get_datum(utxo)
    try:
        timestamp = datum.value[1]
        if not isinstance(timestamp, int):
            return 0
        return timestamp
    except IndexError:
        pass
    return 0


def get_oracle_utxo():
    """Retrieve oracle UTxOs from on-chain."""
    # Look for UTxO that has a datum attached that can be used by the
    # claim script.
    oracle_utxos = context.utxos(oracle_address)
    oracle_utxo = None
    valid_utxos = []
    for utxo in oracle_utxos:
        if utxo.output.datum and not utxo.output.script:
            datum = get_datum(utxo)
            if len(datum.value) != 3:
                # Datum must have three fields, and a valid timestamp.
                # This is not the most sophisticated approach but it
                # works for a demo.
                continue
            valid_utxos.append((get_utxo_timestamp(utxo), utxo))
    if not valid_utxos:
        return None
    sorted(valid_utxos)
    oracle_utxo = valid_utxos[0][1]
    oracle_datum = cbor2.loads(oracle_utxo.output.datum.cbor)
    # pylint: disable=E1123, E1120
    PublishParams(
        owner=oracle_datum.value[0],
        deadline=oracle_datum.value[1],
        threshold=oracle_datum.value[2],
    )
    return oracle_utxo


def get_smart_contract_utxo():
    """Retrieve the UTxO containing the smart contract."""
    logger.info("looking for smart contract UTxO at: %s", script_address)
    script_utxos = context.utxos(str(script_address))
    sc_utxo = None
    for item in script_utxos:
        if item.output.script:
            logger.info("script utxo")
            sc_utxo = item
    return sc_utxo


def get_claimable_utxos():
    """Retrieve UTxOs that can be claimed by a beneficiary."""
    script_utxos = context.utxos(str(script_address))
    claimable_utxos = []
    for item in script_utxos:
        if item.output.script:
            continue
        if item.output.datum:
            logger.info("script datum")
            datum = cbor2.loads(item.output.datum.cbor)
            deposit_datum_obj = VestingParams(
                source=datum.value[0],
                beneficiary=datum.value[1],
                fee_address=datum.value[2],
                fee=datum.value[3],
                deadline=datum.value[4],
                threshold=datum.value[5],
            )
            logger.info("script_datum value: %s", deposit_datum_obj.threshold)
            if str(deposit_datum_obj.beneficiary.hex()) == str(beneficiary_vkey.hash()):
                Address(
                    VerificationKeyHash.from_primitive(deposit_datum_obj.beneficiary),
                    network=network,
                )
                fee_address = Address(
                    VerificationKeyHash.from_primitive(deposit_datum_obj.fee_address),
                    network=network,
                )
                claimable_utxos.append(
                    {
                        "fee_address": str(fee_address),
                        "fee": deposit_datum_obj.fee,
                        "utxo": item,
                    }
                )
    return claimable_utxos


def claim_script():
    """claim money as a beneificary from a vesting script."""

    logger.info("network: %s", network)

    oracle_utxo = get_oracle_utxo()
    if not oracle_utxo:
        logger.info("oracle Datum UTxO not found!")
        sys.exit(0)

    sc_utxo = get_smart_contract_utxo()
    if not sc_utxo:
        logger.info("smart contract UTxO not found!")
        sys.exit(0)
    else:
        logger.info("smart contract utxo: %s", sc_utxo.output.address)

    claimable_utxos = get_claimable_utxos()
    if not claimable_utxos:
        logger.info("no utxo to claim!")
        sys.exit(0)

    logger.info("claiming: %s UTxOs", len(claimable_utxos))

    collateral_utxo = context.utxos(str(collateral_address))[0]
    logger.info(
        "claiming: %s, smart contract: %s",
        collateral_utxo.input.transaction_id,
        collateral_utxo.output.address,
    )

    builder = TransactionBuilder(context)
    builder.reference_inputs.add(sc_utxo)
    builder.reference_inputs.add(oracle_utxo)
    for utxo_to_spend in claimable_utxos:
        builder.add_script_input(
            utxo_to_spend["utxo"], redeemer=Redeemer(ClaimRedeemer())
        )
        builder.add_output(
            TransactionOutput.from_primitive(
                [utxo_to_spend["fee_address"], utxo_to_spend["fee"]]
            )
        )

    builder.collaterals.append(collateral_utxo)
    builder.required_signers = [beneficiary_vkey.hash(), collateral_vkey.hash()]
    builder.validity_start = context.last_block_slot
    builder.ttl = builder.validity_start + 3600

    try:
        # Here the transaction will be created where the smart contract
        # parameters will be validated.
        signed_tx = builder.build_and_sign(
            [beneficiary_skey, collateral_skey], change_address=beneficiary_address
        )
    except TransactionFailedException as err:
        # NB. in the current script, all claimable deposits may fail
        # even if one doesn't meet the threshold but two others do.
        logger.info("failed to build Tx (all claimables will fail): %s", err)
        sys.exit(1)

    save_transaction(signed_tx, "transactions/tx_claim.signed")
    submit_and_log_tx(signed_tx)


def main():
    """Primary entry point for this script..."""
    logger.info("running claim script")
    claim_script()


if __name__ == "__main__":
    main()
