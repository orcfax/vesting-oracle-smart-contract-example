"""Distribute funds between addresses."""

import logging
import os
from typing import Final

from pycardano import (
    Address,
    PaymentSigningKey,
    PaymentVerificationKey,
    TransactionBuilder,
    TransactionOutput,
)

from vesting.config import context, network

logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)-15s %(levelname)s :: %(filename)s:%(lineno)s:%(funcName)s() :: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    level="INFO",
)


def distribute_script():
    """Distribute funds."""

    # pylint: disable=R0914     # Too many local variables.

    oracle_address_skey: Final[str] = os.path.join("wallets", "oracle.skey")
    source_address_skey: Final[str] = os.path.join("wallets", "source.skey")
    beneficiary_address_skey: Final[str] = os.path.join("wallets", "beneficiary.skey")
    oracle_collateral_address_skey: Final[str] = os.path.join(
        "wallets", "oracle-collateral.skey"
    )
    vesting_collateral_address_skey: Final[str] = os.path.join(
        "wallets", "vesting-collateral.skey"
    )

    oracle_skey = PaymentSigningKey.load(oracle_address_skey)
    oracle_vkey = PaymentVerificationKey.from_signing_key(oracle_skey)
    oracle_address = Address(oracle_vkey.hash(), network=network)

    logging.info("oracle addr: %s", oracle_address)

    oracle_collateral_skey = PaymentSigningKey.load(oracle_collateral_address_skey)
    oracle_collateral_vkey = PaymentVerificationKey.from_signing_key(
        oracle_collateral_skey
    )
    oracle_collateral_address = Address(oracle_collateral_vkey.hash(), network=network)

    logging.info("oracle collateral addr: %s", oracle_collateral_address)

    source_skey = PaymentSigningKey.load(source_address_skey)
    source_vkey = PaymentVerificationKey.from_signing_key(source_skey)
    source_address = Address(source_vkey.hash(), network=network)

    logging.info("source addr: %s", source_address)

    beneficiary_skey = PaymentSigningKey.load(beneficiary_address_skey)
    beneficiary_vkey = PaymentVerificationKey.from_signing_key(beneficiary_skey)
    beneficiary_address = Address(beneficiary_vkey.hash(), network=network)

    logging.info("beneficiary addr: %s", beneficiary_address)

    vesting_collateral_skey = PaymentSigningKey.load(vesting_collateral_address_skey)
    vesting_collateral_vkey = PaymentVerificationKey.from_signing_key(
        vesting_collateral_skey
    )
    vesting_collateral_address = Address(
        vesting_collateral_vkey.hash(), network=network
    )

    logging.info("vesting addr: %s", vesting_collateral_address)

    logger.info("building transaction... source_address input")

    builder = TransactionBuilder(context)
    builder.add_input_address(source_address)

    FIVE_ADA: Final[str] = 5000000
    HUNDRED_ADA: Final[str] = 100000000

    logger.info("adding output: oracle_collateral_address %s", FIVE_ADA)
    builder.add_output(
        TransactionOutput.from_primitive([oracle_collateral_address.encode(), FIVE_ADA])
    )

    logger.info("adding output: vesting_collateral_address %s", FIVE_ADA)
    builder.add_output(
        TransactionOutput.from_primitive(
            [vesting_collateral_address.encode(), FIVE_ADA]
        )
    )

    logger.info("adding output: oracle_address_address %s", HUNDRED_ADA)
    builder.add_output(
        TransactionOutput.from_primitive([oracle_address.encode(), HUNDRED_ADA])
    )

    logger.info("adding output: beneficiary_address_address %s", HUNDRED_ADA)
    builder.add_output(
        TransactionOutput.from_primitive([beneficiary_address.encode(), HUNDRED_ADA])
    )

    signed_tx = builder.build_and_sign([source_skey], change_address=source_address)
    context.submit_tx(signed_tx.to_cbor())


def main():
    """Primary entry point for this script..."""
    logger.info("distributing funds to configured wallets")
    distribute_script()


if __name__ == "__main__":
    main()
