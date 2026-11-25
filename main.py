"""Fortune Cookie for the Liquidated Trader — entry program.

The program writes exactly one original fortune-cookie line for a
crypto trader who has just been liquidated to /output/entry.txt and
nothing else. The fortune is a fixed string, so the program is fully
deterministic: every run produces the same entry the judge reads,
byte for byte. No network, no randomness, no input files.
"""

import os

# The entry itself: one line, at most 20 words, at most 160 characters.
# Oracular opening in the fortune voice, then the punchline breaks it
# with a double meaning: luck "turning" — once already, at the price
# where the trader's position was liquidated.
FORTUNE = (
    "The fates say your luck is about to turn. "
    "It turned once already, at your liquidation price."
)

# Where the judge looks for the entry. Override with ENTRY_OUTPUT.
OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")

# The competition gate: UTF-8 text of 1 to 160 characters, one line,
# at most 20 words of plain text.
CHAR_LIMIT = 160
WORD_LIMIT = 20


def validate_fortune(fortune):
    """Reject anything the gate or the brief would refuse: blank text,
    more than one line, over the word limit, over the char limit, or
    not valid UTF-8. Returns the fortune unchanged when it passes."""
    if not fortune.strip():
        raise ValueError("fortune is blank")
    if "\n" in fortune or "\r" in fortune:
        raise ValueError("fortune must be a single line")
    words = fortune.split()
    if len(words) > WORD_LIMIT:
        raise ValueError(
            "fortune is %d words, over the %d limit" % (len(words), WORD_LIMIT)
        )
    if len(fortune) > CHAR_LIMIT:
        raise ValueError(
            "fortune is %d chars, over the %d limit" % (len(fortune), CHAR_LIMIT)
        )
    fortune.encode("utf-8")
    return fortune


def write_entry(text, path):
    """Write the text to path atomically, then read it straight back:
    a reader must never see a half-written entry, and what landed on
    disk must be exactly the fortune that was validated."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.replace(tmp_path, path)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("entry on disk does not match the fortune")
    return len(written)


def run():
    """Validate the fortune, then write it. Returns (chars, path)."""
    fortune = validate_fortune(FORTUNE)
    count = write_entry(fortune, OUTPUT_PATH)
    return count, OUTPUT_PATH


def main():
    count, path = run()
    print("Wrote %d chars to %s" % (count, path))


if __name__ == "__main__":
    main()
