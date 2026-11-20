from app.modules.knowledge.research_claims import (
    RESEARCH_CLAIMS,
    get_pending_critical_claims,
    get_research_claims,
    get_research_topics,
)


def test_all_claim_ids_are_unique():
    ids = [item.claim_id for item in RESEARCH_CLAIMS]

    assert len(ids) == len(set(ids))


def test_all_claims_start_unverified():
    assert RESEARCH_CLAIMS

    for item in RESEARCH_CLAIMS:
        assert item.verified is False
        assert item.source_url is None


def test_claims_have_review_questions():
    for item in RESEARCH_CLAIMS:
        assert item.text_bn.strip()
        assert item.verification_question.strip()


def test_birth_registration_has_age_specific_claims():
    claims = get_research_claims(
        "birth_registration"
    )

    assert len(claims) >= 6

    ids = {item.claim_id for item in claims}

    assert "BR-002" in ids
    assert "BR-003" in ids
    assert "BR-004" in ids


def test_parent_registration_rule_is_critical():
    claim = next(
        item
        for item in RESEARCH_CLAIMS
        if item.claim_id == "BR-005"
    )

    assert claim.risk == "critical"
    assert claim.verified is False


def test_gd_and_correction_limits_need_review():
    critical_ids = {
        item.claim_id
        for item in get_pending_critical_claims()
    }

    assert "BL-003" in critical_ids
    assert "BC-004" in critical_ids


def test_government_fees_need_verification():
    fee_claims = get_research_claims(
        "registration_fees"
    )

    assert len(fee_claims) == 2

    assert all(
        item.risk == "critical"
        for item in fee_claims
    )


def test_all_major_service_topics_exist():
    topics = set(get_research_topics())

    assert {
        "birth_registration",
        "birth_correction",
        "lost_birth_certificate",
        "registration_fees",
        "death_registration",
        "trade_license",
        "citizen_certificates",
        "holding_tax",
        "building_approval",
        "water_connection",
        "health_services",
        "complaint_routing",
    }.issubset(topics)


def test_unknown_topic_returns_no_claims():
    assert get_research_claims(
        "nonexistent_service"
    ) == ()


def test_critical_claims_are_not_approved():
    critical = get_pending_critical_claims()

    assert critical

    assert all(
        not item.verified
        for item in critical
    )
