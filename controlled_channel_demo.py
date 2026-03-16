from __future__ import annotations
import argparse
import time
from typing import List, Tuple
import matplotlib.pyplot as plt

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
    def __init__(self, secret_text: str, delay: float = 0.05) -> None:
        self.secret_text = secret_text
        self.secret_bits = text_to_bits(secret_text)
        self.pages = [bytearray(PAGE_SIZE) for _ in range(len(self.secret_bits) * 2)]
        self.delay = delay

    def run(self) -> List[int]:
        observed_pages: List[int] = []

        print("\n[Victim] Running secret-dependent execution")

        for i, bit in enumerate(self.secret_bits):
            page_zero = 2 * i
            page_one = 2 * i + 1
            chosen_page = page_zero if bit == "0" else page_one

            self.pages[chosen_page][0] ^= 1
            observed_pages.append(chosen_page)

            print(f"Step {i}: bit={bit} → page {chosen_page}")

            time.sleep(self.delay)

        return observed_pages


class Attacker:
    def recover_bits(self, observed_pages: List[int]) -> str:
        recovered_bits = []

        print("\n[Attacker] Reconstructing secret")

        for page in observed_pages:
            bit = "0" if page % 2 == 0 else "1"
            recovered_bits.append(bit)

        return "".join(recovered_bits)

    def recover_text(self, observed_pages: List[int]) -> Tuple[str, str]:
        bits = self.recover_bits(observed_pages)
        text = bits_to_text(bits)

        print(f"Recovered bits: {bits}")
        print(f"Recovered text: {text}")

        return bits, text


def plot_trace(observed_pages: List[int]) -> None:
    plt.figure(figsize=(10, 4))
    plt.plot(observed_pages, marker="o")
    plt.xlabel("Execution Step")
    plt.ylabel("Page Accessed")
    plt.title("Controlled-Channel Page Access Trace")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("page_trace.png", dpi=150)
    plt.close()

    print("\nSaved page_trace.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--secret", type=str, default="HI")
    args = parser.parse_args()

    victim = Victim(secret_text=args.secret)
    attacker = Attacker()

    observed = victim.run()
    attacker.recover_text(observed)
    plot_trace(observed)


if __name__ == "__main__":
    main()
