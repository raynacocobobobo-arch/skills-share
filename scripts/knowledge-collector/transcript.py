"""Hermes transcript collection interface.

Platform implementations:
- youtube transcript
- bilibili subtitle

This module only acquires source text.
"""


def normalize_transcript(text, metadata=None):
    return {
        "metadata": metadata or {},
        "transcript": text.strip(),
        "status": "normalized",
    }


def save_transcript(asset, text):
    return normalize_transcript(text, asset)
