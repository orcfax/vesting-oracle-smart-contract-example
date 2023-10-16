"""Vesting smart contract..."""

from opshin.ledger.interval import *  # noqa: required import by OpShin.


@dataclass
class VestingParams(PlutusData):
    """Vesting Params datum structure."""

    # the published, who can also reclaim the UTxO anytime (refund).
    source: PubKeyHash

    # the vesting beneficiary, who can claim the UTxO after the deadline if
    # they pays the fee to the fee_address and the datum value ("info") is
    # greater than the limit.
    beneficiary: PubKeyHash

    # the address where the fee must be paid.
    fee_address: bytes

    # the fee amount which must be paid
    fee: int

    # the vesting deadline.
    deadline: POSIXTime

    # the minimum threshold for the datum value which allows the UTxO to
    # be claimed by the beneficiary
    threshold: int


@dataclass
class PublishParams(PlutusData):
    """Oracle datum structure."""

    # publisher of the datum, who can also reclaim the UTxO after the deadline
    # (refund).
    owner: PubKeyHash

    # the deadline after which the datum UTxO can be refunded.
    deadline: POSIXTime

    # the threshold value published by the datum for which the vesting
    # Tx must meet.
    threshold: int


@dataclass
class ClaimRedeemer(PlutusData):
    """ClaimRedeemer object."""

    CONSTR_ID = 0


@dataclass
class RefundRedeemer(PlutusData):
    """RefundRedeemer object."""

    CONSTR_ID = 1


def validator(
    datum: VestingParams,
    redeemer: Union[ClaimRedeemer, RefundRedeemer],
    context: ScriptContext,
) -> None:
    """Validation for the vesting contract."""

    salt = "(1YfcE)"  # make the contract unique under tutorial circumstances.

    if isinstance(redeemer, ClaimRedeemer):
        # first check if the beneficiary signed the transaction and if
        # the transaction was submitted after the deadline.
        assert (
            datum.beneficiary in context.tx_info.signatories
        ), "Collect signature missing!"
        assert contains(make_from(datum.deadline), context.tx_info.valid_range), (
            "TX submitted too early! " + salt
        )
        # check if the fee has been paid to the fee address
        fee_found = False  # fee address found
        fee_paid = False  # fee paid
        for item in context.tx_info.outputs:
            if datum.fee_address == item.address.payment_credential.credential_hash:
                fee_found = True
                if item.value.get(b"", {b"": 0}).get(b"", 0) >= datum.fee:
                    fee_paid = True
        assert fee_found, "Fee address not found in outputs!"
        assert fee_paid, "Fee too small!"
        # Construct the the failure text preemptively so that we can return
        # something meaningful as the contract validates.
        failure_text = ""
        datum_condition = False  # datum condition
        for reference_input in context.tx_info.reference_inputs:
            reference_script = reference_input.resolved.reference_script
            if isinstance(reference_script, NoScriptHash):
                failure_text = "NoScriptHash: False, script associated with output -- checking datum in output"
                reference_datum = reference_input.resolved.datum
                if isinstance(reference_datum, SomeOutputDatum):
                    data_from_oracle: PublishParams = (
                        reference_datum.datum
                    )  # oracle info
                    # failure text cannot be constructed using an f-string
                    # using OpShin.
                    failure_text = (
                        "SomeOutputDatum: True, datum in output -- checking ig value in Oracle: "
                        + str(data_from_oracle.threshold)
                        + " is greater than donor threshold: "
                        + str(datum.threshold)
                        + " to be able to claim"
                    )
                    if data_from_oracle.threshold > datum.threshold:
                        datum_condition = True
        assert datum_condition, failure_text
    elif isinstance(redeemer, RefundRedeemer):
        assert datum.source in context.tx_info.signatories, "refund signature missing!"
    else:
        assert False, "wrong redeemer"
