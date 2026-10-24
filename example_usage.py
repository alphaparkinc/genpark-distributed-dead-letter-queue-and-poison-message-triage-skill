"""Example usage for Dead Letter Queue Triager."""
from client import DeadLetterQueueTriager

if __name__ == "__main__":
    res = DeadLetterQueueTriager.triage_dead_letter("Gateway 503 Service Unavailable", attempts=2)
    print("Disposition:", res["triage_disposition"], "Backoff Sec:", res["retry_backoff_sec"])
