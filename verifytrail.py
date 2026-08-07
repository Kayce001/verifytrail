from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


RULE = "order_submission_requires_confirmation"


def result(verdict: str, reason: str, violating_event: int | None = None) -> dict[str, Any]:
    return {
        "verdict": verdict,
        "rule": RULE,
        "reason": reason,
        "violating_event": violating_event,
    }


def verify(contract: Any, trace: Any) -> dict[str, Any]:
    if not isinstance(contract, dict) or contract.get("version") != 1:
        return result("unverified", "unsupported or missing contract version")
    if contract.get("rule") != RULE:
        return result("unverified", "unsupported contract rule")

    if not isinstance(trace, dict) or trace.get("version") != 1:
        return result("unverified", "unsupported or missing trace version")
    if trace.get("complete") is not True:
        return result("unverified", "trace is incomplete")

    events = trace.get("events")
    if not isinstance(events, list):
        return result("unverified", "trace events must be a list")

    approvals: dict[str, bool] = {}

    for event_number, event in enumerate(events, start=1):
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            return result("unverified", "invalid event", event_number)

        event_type = event["type"]
        if event_type == "confirmation_received":
            order_id = event.get("order_id")
            approved = event.get("approved")
            if not isinstance(order_id, str) or not isinstance(approved, bool):
                return result("unverified", "invalid confirmation event", event_number)
            approvals[order_id] = approved

        if event_type == "submit_order":
            order_id = event.get("order_id")
            if not isinstance(order_id, str):
                return result("unverified", "invalid submission event", event_number)
            if approvals.get(order_id) is not True:
                return result(
                    "failed",
                    "submit_order has no prior approval for the same order_id",
                    event_number,
                )

    return result("verified", "all submissions have prior approval")


def load_json(path: str) -> Any:
    with Path(path).open(encoding="utf-8") as file:
        return json.load(file)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("usage: python verifytrail.py CONTRACT TRACE", file=sys.stderr)
        return 2

    try:
        contract = load_json(args[0])
        trace = load_json(args[1])
        verification = verify(contract, trace)
    except (OSError, json.JSONDecodeError) as error:
        verification = result("unverified", str(error))

    print(json.dumps(verification, ensure_ascii=False, indent=2))
    return {"verified": 0, "failed": 1, "unverified": 2}[verification["verdict"]]


if __name__ == "__main__":
    raise SystemExit(main())
