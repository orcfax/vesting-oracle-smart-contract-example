"""Configuration options for this set of scripts..."""

import os

from pycardano import Network, OgmiosChainContext

# Context for running Pycardano.
OGMIOS_URL = "ws://ogmios.preprod.orcfax.io:1337"
network = Network.TESTNET
context = OgmiosChainContext(ws_url=OGMIOS_URL, network=network)

# Misc.
contract_cbor = "build/contract/script.cbor"
tx_template = {
    "type": "Witnessed Tx BabbageEra",
    "description": "Ledger Cddl Format",
    "cborHex": "",
}
transactions_path = "transactions"

# wallet paths.
oracle_address_skey = os.path.join("..", "wallets", "oracle.skey")
collateral_address_skey = os.path.join("..", "wallets", "oracle-collateral.skey")
