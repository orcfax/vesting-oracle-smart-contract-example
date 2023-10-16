"""Oracle smart contract script."""


from opshin.ledger.interval import *  # noqa: required import by OpShin.


@dataclass
class PublishParams(PlutusData):
    """PublishParams describes the structure of the Datum."""

    # owner: publisher of the datum, who can also reclaim the UTxO
    # after the deadline (refund).
    owner: PubKeyHash
    # hold_time: the time after which the datum UTxO can be
    # refunded.
    hold_time: POSIXTime
    # info: the useful information in the oracle datum, an int in this
    # case.
    threshold: int


@dataclass
class RefundRedeemer(PlutusData):
    """Oracle redeemer."""


def validator(
    datum: PublishParams, redeemer: RefundRedeemer, context: ScriptContext
) -> (
    None
):  # noqa, redeemer isn't accessed, but is required by OpShin (do not delete it!).
    salt = "(1YfcE)"  # make the contract unique under tutorial circumstances.

    assert contains(make_from(datum.hold_time), context.tx_info.valid_range), (
        "Tx submitted too early! " + salt
    )
    assert datum.owner in context.tx_info.signatories, "Refund signature is missing!"
