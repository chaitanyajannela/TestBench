from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator


# -----------------------------------------
# 1. CONTRACT TYPE
# -----------------------------------------

class ContractType(str, Enum):
    MUST = "MUST"
    MUST_NOT = "MUST_NOT"
    SHOULD = "SHOULD"
    SHOULD_NOT = "SHOULD_NOT"
    CONDITIONAL = "CONDITIONAL"


# -----------------------------------------
# 2. CONTRACT CATEGORY
# -----------------------------------------

class ContractCategory(str, Enum):
    PRIVACY = "PRIVACY"
    SECURITY = "SECURITY"
    ACCURACY = "ACCURACY"
    BUSINESS_POLICY = "BUSINESS_POLICY"
    COMMUNICATION = "COMMUNICATION"
    FORMATTING = "FORMATTING"
    QUALITY = "QUALITY"
    OTHER = "OTHER"


# -----------------------------------------
# 3. SEVERITY
# -----------------------------------------

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# -----------------------------------------
# 4. EVALUATION METHOD
# -----------------------------------------

class EvaluationMethod(str, Enum):
    RULE_BASED = "RULE_BASED"
    SEMANTIC = "SEMANTIC"
    LLM_JUDGE = "LLM_JUDGE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    HYBRID = "HYBRID"


# -----------------------------------------
# 5. CONTRACT STATUS
# -----------------------------------------

class ContractStatus(str, Enum):
    DRAFT = "DRAFT"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"


# -----------------------------------------
# 6. BEHAVIOR CONTRACT
# -----------------------------------------

class BehaviorContract(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    # Identification
    contract_id: UUID = Field(
        default_factory=uuid4
    )

    version: int = Field(
        default=1,
        ge=1
    )

    name: str = Field(
        min_length=3,
        max_length=150
    )

    # Requirement traceability
    original_requirement: str = Field(
        min_length=10,
        max_length=2000
    )

    normalized_requirement: str = Field(
        min_length=10,
        max_length=2000
    )

    # Contract classification
    contract_type: ContractType

    category: ContractCategory

    severity: Severity

    # Behavioral specification
    preconditions: list[str] = Field(
        default_factory=list
    )

    expected_behavior: list[str] = Field(
        default_factory=list
    )

    prohibited_behavior: list[str] = Field(
        default_factory=list
    )

    # Evaluation configuration
    evaluation_method: EvaluationMethod

    evaluation_criteria: list[str] = Field(
        default_factory=list
    )

    # Compiler metadata
    ambiguities: list[str] = Field(
        default_factory=list
    )

    confidence_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    # Lifecycle
    status: ContractStatus = ContractStatus.DRAFT

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @model_validator(mode="after")
    def validate_behavior(self):

        if not self.expected_behavior and not self.prohibited_behavior:
            raise ValueError(
                "A contract must define expected or prohibited behavior."
            )

        if self.contract_type == ContractType.MUST_NOT:
            if not self.prohibited_behavior:
                raise ValueError(
                    "MUST_NOT contracts require prohibited behavior."
                )

        return self