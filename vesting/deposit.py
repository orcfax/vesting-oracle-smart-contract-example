"""Deposit some ADA for the beneficiary...

The smart contract allows the beneficiary of the money deposited here to
receive the funds if certain conditions are met.

Vesting params when they are deposited look as follows:

```text
    {
        "fields": [
            {
                "bytes": "2567d3e7ac827f0691ddb902ec1958a3068c8cede501a0ecd434dee4"
            },
            {
                "bytes": "7502f8ad62986262b7cea7f718671f092f538ec17a4b6400ad8ca60d"
            },
            {
                "bytes": "5423999dcaa32825469f897c1fffb1bcacacf5a5a61c6813770c66ba"
            },
            {
                "int": 2000000
            },
            {
                "int": 1695098035000
            },
            {
                "int": 10
            }
        ],
        "constructor": 0
    }
```

"""

import sys
from datetime import datetime
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
    beneficiary_address,
    beneficiary_vkey,
    fee_address,
    save_transaction,
    script_address,
    source_address,
    source_skey,
    source_vkey,
    submit_and_log_tx,
)

# Threshold, which if an Oracle publishes a higher value, will allow the
# beneficiary to claim the amount locked away.
THRESHOLD = 6

# 30 seconds?
VESTING_TIME = 30

# deposit 1.5 ada...
AMOUNT = 15000000

# fee to pay.... 2 ada....
FEE = 2000000


def deposit_script():
    """deposit money to a smart contract.

    A threshold has to be reached in the published Oracle data for the
    vesting contract to pay out. If the value isn't met, then the value
    deposited can be refunded, or continue to be waited for by the
    beneficiary.
    """

    source_addr = source_vkey.hash().to_primitive()
    beneficiary_addr = beneficiary_vkey.hash().to_primitive()
    fee_addr = fee_address.payment_part.to_primitive()
    fee = FEE

    # Deadline and amount...
    deadline = (int(time()) + VESTING_TIME) * 1000  # milliseconds
    deadline_human = datetime.utcfromtimestamp(int(deadline) / 1000).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    # amount that can be claimed...
    amount = Value(AMOUNT)

    logger.info("source: %s", source_address)
    logger.info("fee: %s", fee_address)
    logger.info("beneficiary: %s", beneficiary_address)
    logger.info("depositing amount: %s lovelace", AMOUNT)
    logger.info(
        "threshold value (claimant can only receive money if Oracle publishes a higher value): %s",
        THRESHOLD,
    )
    logger.info("timestamp: %s (%s)", deadline_human, deadline)

    # Vesting params... include LIMIT...
    datum = VestingParams(
        source=source_addr,
        beneficiary=beneficiary_addr,
        fee_address=fee_addr,
        fee=fee,
        deadline=deadline,
        threshold=THRESHOLD,
    )

    builder = TransactionBuilder(context)
    builder.add_input_address(source_address)
    builder.add_output(TransactionOutput(script_address, amount=amount, datum=datum))

    try:
        signed_tx = signed_tx = builder.build_and_sign(
            [source_skey], change_address=source_address
        )
    except TransactionFailedException as err:
        logger.error("error creating deploy Tx: %s", err)
        sys.exit(1)
    save_transaction(signed_tx, "transactions/tx_deposit.signed")
    submit_and_log_tx(signed_tx)


def main():
    """Primary entry point for this script..."""
    logger.info("running deposit script")
    deposit_script()


if __name__ == "__main__":
    main()
