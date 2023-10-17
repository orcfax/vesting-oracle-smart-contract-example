# Vesting with fee and Oracle Datum condition

[![Awesome OpShin Badge][awesome-opshin-img]][awesome-opshin]

[awesome-opshin]: https://github.com/OpShin/awesome-opshin
[awesome-opshin-img]: https://img.shields.io/badge/awesome-opshin-blue?logo=data:image/png;base64,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

This example has two Opshin smart contracts that work in concert with
one-another. A vesting contract allows a user to deposit ADA to be claimed by
a beneficiary when certain other conditions are met. An oracle contract
publishes values on chain. When the beneficiary seeks to claim the deposit, the
oracle has to have published a value that is above the threshold set in the
claim contract.

This work is a modified version of cardano-apexpool's examples [here][apex-1].
Many of the mechanics have been kept with terminology modified slightly and
additional logging added to aid usabiility.

Readers and those modifying this code will want to refer to the documentation
and examples for OpShin, and the PyCardano manual. OpShin provides the mechanism
to put smart contracts on-chain and necessary validation machinery. PyCardano
enables us to interact with Cardano off-chain, e.g. allowing us to build the
all important transactions and submit those.

* [OpShin][links-1].
* [PyCardano][links-2].

## Contents

- [Oracle contract](#oracle-contract)
- [Vesting contract](#vesting-contract)
- [Worked example](#worked-example)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Tutorial steps](#tutorial-steps)
    - [Tutorial](#tutorial)
      - [Build and deploy the smart contracts](#build-and-deploy-the-smart-contracts)
      - [Deposit funds](#deposit-funds)
      - [Publish a value from the oracle](#publish-a-value-from-the-oracle)
      - [Attempt to claim the deposit](#attempt-to-claim-the-deposit)
      - [Publish a larger oracle value](#publish-a-larger-oracle-value)
      - [Claim the deposit](#claim-the-deposit)
        - [Notes on claiming](#notes-on-claiming)
      - [Refunding the ADA](#refunding-the-ada)
      - [Undeploy the scripts](#undeploy-the-scripts)

[apex-1]: https://github.com/cardano-apexpool/opshin-smart-contract-examples
[links-1]: https://github.com/OpShin/opshin
[links-2]: https://pycardano.readthedocs.io/en/latest/tutorial.html

## Oracle contract

This smart contract is a simple Oracle publishing an integer in a Datum
on-chain.

Other smart contracts can use this integer and take decisions depending on its
value.

## Vesting contract

Vesting is the process of claiming value from something after certain
conditions are met.

The vesting smart contract in this repository is a more complex example than
the oexample. In order to unlock and claim funds, it checks if:

* the transaction is signed by its beneficiary (a key defined in the Datum when
locking the funds)
* the vesting period has passed (also declared in the Datum when locking the
funds)
* has a fee been paid to an address (the fee address and fee amount are also
declared in the Datum when locking the funds)
* if the `threshold` declared in the vesting datum is lower than the `threshold`
published in the oracle's datum.

## Worked example

This is only presented as an example, anyone can publish an UTxO at the Oracle
address with a different integer which may allow unlocking the funds. There is
no check implemented regarding who published the Oracle Datum.

### Requirements

* `cardano-cli`
* `make`
* `python3`

### Setup

1. Clone the repository and create a virtual environment:

```sh
git clone <this repository>
cd <this repository name>
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements/requirements.txt
```

2. Create the wallets:

From this directory run:

```sh
./wallets.sh
```

The wallet addresses including the `source` address will be output. Note down
the `source` address.

3. fund the `source` address from the Cardano [preprod faucet][faucet-1] on the
preprod network. We will use the ADA in the `source` wallet to distribute funds
to the collateral addresses, to the oracle address, and to the vesting
beneficiary address.

[faucet-1]: https://docs.cardano.org/cardano-testnet/tools/faucet/

4. From this directory fund all addresses:

```sh
python3 distribute_funds.py
```

### Tutorial steps

The tutorial will go  through the following steps:

1. Deploy the oracle and vesting smart contracts.
1. Deposit some funds.
1. Publish a value from an oracle.
1. Attempt to claim the vested funds.
1. Publish another oracle value.
1. Successfully claim the vested funds.
1. Refund any remaining value in either contracts.
1. Undeploy the smart contracts.

It is recommended after working through the different steps that you then play
around with the different deposit options in the Python scripts as well as
those in the oracle scripts to get an idea how the different pieces of this
tutorial work together.

#### Tutorial

##### Build and deploy the smart contracts

We will now enter the oracle and vesting directories separately to deploy their
associated smart contracts.

In the `oracle` directory:

```sh
make build-contract
make deploy-contract
```

In the `vesting` directory:

```sh
make build-contract
make deploy-contract
```

You can see the addresses and transactions on the [blockchain explorer][ex-1].

[ex-1]: https://preprod.cexplorer.io/

##### Deposit funds

Deposit some ADA for the beneficiary on the Vesting smart contract address.

In the example, in order to claim the deposit the beneficiary will have to pay
a fee to a fee address,

they will only be able to claim the deposit if the oracle publishes a Datum
which is higher than the `VestingParams` `threshold` in the deposit.

The `VestingParams` class is the Datum format declared in `contract.py`.

In the default example, the vesting time is set to 30 seconds, the `threshold`
is set to 6 and the `fee` is 2 ADA.

In the `vesting` folder:

```sh
python3 deposit.py
```

Publish a Datum with a threshold value on the Oracle smart contract address.

The threshold in this example is set to the number 7. This will allow the
beneficiary to claim the deposit, because the smart contract checks if the
integer published by the Oracle is greater than the `threshold` in the
deposit's datum.

##### Publish a value from the oracle

In the `oracle` folder:

```sh
python3 publish.py
```

##### Attempt to claim the deposit

In the `vesting` folder:

```sh
python3 claim.py
```

The claim will not work the first time around. You will need to wait for the
oracle to publish a value that is higher than the claim threshold. This might
simulate an activity that will be performed by a smart contract when a
currency value is published beyond a certain threshold, e.g. a liquidation
event.

##### Publish a larger oracle value

Try setting a `threshold` higher than 7 in the oracle folder then run it again:

In the oracle folder:

```sh
python3 publish.py --value 7
```

##### Claim the deposit

In the vesting folder:

```sh
python3 claim.py
```

###### Notes on claiming

Claiming before the vesting period expires will throw the error
`'TX submitted too early!'`, and after the vesting period, the error will be
`'Claim condition not met!'`. If the beneficiary signature is missing from the
claim transaction, the error will be
`{'missingRequiredSignatures': ['<beneficiary_public_key_hash>']}`. If the fee
is not paid, the error will be `'Fee address not found in outputs!'`,
and if the fee amount is too low, the error will be `'Fee too small!'`.

Play around with the deposit script and oracle script to attempt to trigger
these errors. Try adding checks to the `contract.py` scripts and building and
redeploying to see how the smart contract process works.

##### Refunding the ADA

Users of these scripts should become comfortable with the flow of ADA through
the process, and at any time, ADA can be refunded using the repository's
refund scripts.

The deposit can be refunded anytime by running the `refund.py` script in the
`vesting` folder:

```sh
python3 refund.py
```

The Oracle Datum UTxO can also be refunded when it is no longer required by
running the `refund.py` script in the `oracle` folder:

```sh
python3 refund.py
```

##### Undeploy the scripts

The the vested value return (if it wasn't claimed) and the minimum ADA value
reclaimed from the racle datum, we can undeploy the smart contracts. Undeploy
spends the smart contract UTxOs. From the oracle and vesting folders run:

```sh
python3 undeploy.py
```
