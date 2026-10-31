import pytest

from pydantic import ValidationError

from app.schemas.contract import (
    BehaviorContract,
    ContractType,
    ContractCategory,
    Severity,
    EvaluationMethod,
    ContractStatus
)


def create_valid_contract():

    return BehaviorContract(
        name="Password Protection",
        original_requirement=(
            "The chatbot must never reveal customer passwords."
        ),
        normalized_requirement=(
            "The chatbot must not disclose customer passwords."
        ),
        contract_type=ContractType.MUST_NOT,
        category=ContractCategory.PRIVACY,
        severity=Severity.CRITICAL,
        prohibited_behavior=[
            "Revealing customer passwords."
        ],
        expected_behavior=[
            "Refusing password disclosure."
        ],
        evaluation_method=EvaluationMethod.RULE_BASED
    )


def test_valid_contract_creation():

    contract = create_valid_contract()

    assert contract.name == "Password Protection"
    assert contract.severity == Severity.CRITICAL
    assert contract.status == ContractStatus.DRAFT


def test_contract_generates_unique_ids():

    contract_one = create_valid_contract()
    contract_two = create_valid_contract()

    assert contract_one.contract_id != contract_two.contract_id


def test_must_not_requires_prohibited_behavior():

    with pytest.raises(ValidationError):

        BehaviorContract(
            name="Password Protection",
            original_requirement="Never reveal customer passwords.",
            normalized_requirement="Do not disclose passwords.",
            contract_type=ContractType.MUST_NOT,
            category=ContractCategory.PRIVACY,
            severity=Severity.CRITICAL,
            expected_behavior=["Refuse disclosure."],
            evaluation_method=EvaluationMethod.RULE_BASED
        )


def test_contract_requires_behavior():

    with pytest.raises(ValidationError):

        BehaviorContract(
            name="Password Protection",
            original_requirement="Never reveal customer passwords.",
            normalized_requirement="Do not disclose passwords.",
            contract_type=ContractType.MUST,
            category=ContractCategory.PRIVACY,
            severity=Severity.CRITICAL,
            evaluation_method=EvaluationMethod.RULE_BASED
        )


def test_confidence_score_validation():

    with pytest.raises(ValidationError):

        BehaviorContract(
            name="Password Protection",
            original_requirement="Never reveal customer passwords.",
            normalized_requirement="Do not disclose passwords.",
            contract_type=ContractType.MUST_NOT,
            category=ContractCategory.PRIVACY,
            severity=Severity.CRITICAL,
            prohibited_behavior=["Reveal passwords."],
            evaluation_method=EvaluationMethod.RULE_BASED,
            confidence_score=1.5
        )