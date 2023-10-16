#!/bin/bash

KEYS="oracle oracle-collateral vesting-collateral source beneficiary fee"
CARDANO_NET="--testnet-magic 1"

for ADDR in $KEYS
do
  if [ -f "wallets/${ADDR}.skey" ] ; then
    echo "Key already exists!"
  else
    cardano-cli address key-gen --verification-key-file "wallets/${ADDR}.vkey" --signing-key-file "wallets/${ADDR}.skey"
    cardano-cli address build --payment-verification-key-file "wallets/${ADDR}.vkey" --out-file "wallets/${ADDR}.addr" ${CARDANO_NET}
    echo "${ADDR} address: $(cat wallets/${ADDR}.addr)"
  fi
done
