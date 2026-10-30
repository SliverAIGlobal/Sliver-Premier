"""
Unit Test Suite: Outreach Engine & Automated Payment/License Minting Addons
"""

import pytest
from outreach_engine import AutomatedOutreachEngine, OutreachContact
from payment_engine import LicenseMinter, PaymentAndLedgerEngine


def test_outreach_engine_campaign_generation():
    engine = AutomatedOutreachEngine()
    contacts = [
        OutreachContact(name="Teacher Jane", email="jane@school.org", vertical="edtech", organization="Oak School"),
        OutreachContact(name="OT Mark", email="mark@clinic.org", vertical="healthtech"),
        OutreachContact(name="Dev Liam", email="liam@edge.org", vertical="wasm_dev"),
        OutreachContact(name="Early Adopter", email="early@buyer.com", vertical="flash_seed"),
    ]
    results = engine.dispatch_campaign(contacts)
    assert len(results) == 4
    assert any("0-Day IT Clearance" in r["subject"] for r in results)
    assert any("Somatic Tremor" in r["subject"] for r in results)
    assert any("Airplane Mode" in r["subject"] for r in results)
    assert any("60-Minute Early Seed" in r["subject"] for r in results)


def test_license_key_minting_and_checksum_verification():
    for _ in range(20):
        key = LicenseMinter.mint_key()
        assert key.startswith("SP-")
        assert len(key) == 16  # SP-XXXX-YYYY-ZZZZ with hyphens
        assert LicenseMinter.verify_key(key) is True

    # Test forged/tampered key
    tampered = "SP-ABCD-EFGH-ZZZZ"
    assert LicenseMinter.verify_key(tampered) is False


def test_payment_webhook_and_device_limit_enforcement():
    engine = PaymentAndLedgerEngine()
    payload = {
        "buyer_email": "jane@school.org",
        "price": 49.0,
        "currency": "USD",
        "order_id": "ORD-TEST-1234",
    }
    record = engine.process_webhook(payload)
    assert record.tier == "individual_5device"
    assert record.max_devices == 5
    assert record.veridical_hash.endswith("_SLIVER_GRAND_LEDGER")
    assert LicenseMinter.verify_key(record.license_key) is True

    # Register up to 5 devices
    for i in range(1, 6):
        res = engine.register_device(record.license_key, f"device-fingerprint-{i}")
        assert res["status"] == "DEVICE_REGISTERED"
        assert res["devices_count"] == i

    # 6th device should hit limit
    overflow = engine.register_device(record.license_key, "device-fingerprint-6")
    assert overflow["status"] == "DEVICE_LIMIT_REACHED"
    assert overflow["devices_count"] == 5
