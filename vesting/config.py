"""Condiguration options for this set of scripts..."""

import os

from pycardano import Network, OgmiosChainContext

# Context for running PyCardano.
OGMIOS_URL = "ws://ogmios.preprod.orcfax.io:1337"
network = Network.TESTNET
context = OgmiosChainContext(ws_url=OGMIOS_URL, network=network)

# Misc.
contract_cbor = "build/contract/script.cbor"
oracle_address = "addr_test1wz6mfpvyu7d4m9xxpkrc2wm8nel0htmjvsafpntlwpr7ggqnan7e6"  # default: "addr_test1wz6mfpvyu7d4m9xxpkrc2wm8nel0htmjvsafpntlwpr7ggqnan7e6"
tx_template = {
    "type": "Witnessed Tx BabbageEra",
    "description": "Ledger Cddl Format",
    "cborHex": "",
}
transactions_path = "transactions"
oracle_address_file = "../oracle/build/contract/testnet.addr"

# wallet paths.
source_address_skey = os.path.join("..", "wallets", "source.skey")
beneficiary_address_skey = os.path.join("..", "wallets", "beneficiary.skey")
fee_address_skey = os.path.join("..", "wallets", "fee.skey")
collateral_address_skey = os.path.join("..", "wallets", "vesting-collateral.skey")
