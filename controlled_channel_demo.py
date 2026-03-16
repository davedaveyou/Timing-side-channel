#!/usr/bin/env python3
"""
controlled_channel_demo.py

Simple simulation of the paper:
"Controlled-Channel Attacks: Deterministic Side Channels for Untrusted Operating Systems"

This is NOT a real SGX or kernel-level page fault attack.
It is a teaching/demo simulation that shows the core idea:

secret -> different page accesses -> attacker observes page sequence -> attacker recovers secret
"""

from __future__ import annotations
import argparse
import time
from typing import List, Tuple

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


PAGE_SIZE = 4096


def text_to_bits(text: str) -> str:
    return "".join(f"{ord(c):08b}" for c in text)


def bits_to_text(bits: str) -> str:
    chars = []
    for i in range(0, len(bits), 8):
        chunk = bits[i:i + 8]
        if len(chunk) == 8:
            chars.append(chr(int(chunk, 2)))
    return "".join(chars)


class Victim:
    """
    Victim simulates secret-dependent control flow.
    Each secret bit chooses one of two pages:
      pair (0,1) for first bit
      pair (2,3) for second bit
      pair (4,5) for third bit
      ...
    If bit == 0 -> first page in pair
    If bit == 1 -> second page in pair
    """

    def __init__(self, secret_text: str, delay: float = 0.20) -> None:
        self.secret_text = secret_text
        self.secret_bits = text_to_bits(secret_text)
        self.pages = [bytearray(PAGE_SIZE) for _ in range(len(self.secret_bits) * 2)]
        self.delay = delay

    def run(self, verbose: bool = True) -> List[int]:
        observed_pages: List[int] = []

        if verbose:
            print("=" * 70)
            print("[Victim] Starting secret-dependent execution")
            print(f"[Victim] Secret text length: {len(self.secret_text)} char(s)")
            print(f"[Victim] Secret bit length : {len(self.secret_bits)} bit(s)")
            print("=" * 70)

        for i, bit in enumerate(self.secret_bits):
            page_zero = 2 * i
            page_one = 2 * i + 1
            chosen_page = page_zero if bit == "0" else page_one

            # Simulate page access by touching memory on that page
            self.pages[chosen_page][0] = (self.pages[chosen_page][0] + 1) % 256

            observed_pages.append(chosen_page)

            if verbose:
                print(
                    f"[Victim] Step {i:02d}: bit={bit} -> accessed page {chosen_page} "
                    f"(pair {page_zero}/{page_one})"
                )

            time.sleep(self.delay)

        if verbose:
            print("=" * 70)
            print("[Victim] Execution complete")
            print("=" * 70)

        return observed_pages


class Attacker:
    """
    Attacker observes which page was accessed at each step and reconstructs bits.
    For each pair:
      even page in pair  -> bit 0
      odd page in pair   -> bit 1
    """

    def recover_bits(self, observed_pages: List[int], verbose: bool = True) -> str:
        recovered_bits = []

        if verbose:
            print("=" * 70)
            print("[Attacker] Observing page accesses and reconstructing secret bits")
            print("=" * 70)

        for step, page in enumerate(observed_pages):
            bit = "0" if page % 2 == 0 else "1"
            recovered_bits.append(bit)

            if verbose:
                print(f"[Attacker] Step {step:02d}: saw page {page} -> recovered bit {bit}")

        return "".join(recovered_bits)

    def recover_text(self, observed_pages: List[int], verbose: bool = True) -> Tuple[str, str]:
        bits = self.recover_bits(observed_pages, verbose=verbose)
        text = bits_to_text(bits)

        if verbose:
            print("=" * 70)
            print(f"[Attacker] Recovered bits : {bits}")
            print(f"[Attacker] Recovered text : {text!r}")
            print("=" * 70)

        return bits, text


def plot_trace(observed_pages: List[int], output_file: str = "page_trace.png") -> None:
    if plt is None:
        print("[Plot] matplotlib is not installed, skipping plot.")
        return

    x = list(range(len(observed_pages)))
    y = observed_pages

    plt.figure(figsize=(11, 4))
    plt.plot(x, y, marker="o")
    plt.xlabel("Execution step")
    plt.ylabel("Observed page number")
    plt.title("Observed Page Access Trace")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    print(f"[Plot] Saved trace figure to {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Controlled-channel / page-fault side-channel demo"
    )
    parser.add_argument(
        "--secret",
        type=str,
        default="HI",
        help="Short secret text to encode and recover (default: HI)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.15,
        help="Delay between steps for video visibility (default: 0.15)"
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Disable plot generation"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce terminal output"
    )
    args = parser.parse_args()

    print("\nControlled-Channel Attack Demo")
    print("Paper concept: page access patterns leak secret-dependent execution\n")
    print("Important: this is a simulation of the leakage principle, not a real SGX exploit.\n")

    victim = Victim(secret_text=args.secret, delay=args.delay)
    attacker = Attacker()

    observed_pages = victim.run(verbose=not args.quiet)
    recovered_bits, recovered_text = attacker.recover_text(observed_pages, verbose=not args.quiet)

    print("\nSummary")
    print("-" * 70)
    print(f"Original secret text : {args.secret!r}")
    print(f"Recovered secret text: {recovered_text!r}")
    print(f"Match                : {args.secret == recovered_text}")
    print("-" * 70)

    if not args.no_plot:
        plot_trace(observed_pages)


if __name__ == "__main__":
    main()
