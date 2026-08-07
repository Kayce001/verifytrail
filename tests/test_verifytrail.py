import unittest

from verifytrail import RULE, verify


CONTRACT = {"version": 1, "rule": RULE}


class VerifyTrailTests(unittest.TestCase):
    def test_verified(self) -> None:
        trace = {
            "version": 1,
            "complete": True,
            "events": [
                {
                    "type": "confirmation_received",
                    "order_id": "order-1",
                    "approved": True,
                },
                {"type": "submit_order", "order_id": "order-1"},
            ],
        }

        self.assertEqual(verify(CONTRACT, trace)["verdict"], "verified")

    def test_failed(self) -> None:
        trace = {
            "version": 1,
            "complete": True,
            "events": [{"type": "submit_order", "order_id": "order-1"}],
        }

        verification = verify(CONTRACT, trace)
        self.assertEqual(verification["verdict"], "failed")
        self.assertEqual(verification["violating_event"], 1)

    def test_unverified(self) -> None:
        trace = {"version": 1, "complete": False, "events": []}

        self.assertEqual(verify(CONTRACT, trace)["verdict"], "unverified")


if __name__ == "__main__":
    unittest.main()
