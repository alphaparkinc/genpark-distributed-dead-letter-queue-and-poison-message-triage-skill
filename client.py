"""Distributed Dead-Letter Queue & Poison Message Triage.
100% Python Standard Library.
"""

class DeadLetterQueueTriager:
    """Categorizes failed poison messages and assigns retry backoff strategies."""

    @staticmethod
    def triage_dead_letter(error_reason: str, attempts: int, max_attempts: int = 3) -> dict:
        if attempts >= max_attempts:
            disposition = "PERMANENT_POISON_QUARANTINE"
            backoff_sec = 0
        elif "timeout" in error_reason.lower() or "503" in error_reason:
            disposition = "EXPONENTIAL_BACKOFF_RETRY"
            backoff_sec = 2 ** attempts * 5
        elif "malformed" in error_reason.lower() or "syntax" in error_reason.lower():
            disposition = "DISCARD_UNPARSEABLE_PAYLOAD"
            backoff_sec = 0
        else:
            disposition = "LINEAR_RETRY"
            backoff_sec = 10

        return {
            "error_reason": error_reason,
            "attempts": attempts,
            "triage_disposition": disposition,
            "retry_backoff_sec": backoff_sec
        }
