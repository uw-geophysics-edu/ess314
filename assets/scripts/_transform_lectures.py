"""
_transform_lectures.py — one-shot transformation script.
1. Removes "Slide Audit Summary" block from 04_seismic_wave_types.md
2. Wraps Syllabus Alignment / Learning Objectives / Prerequisites
   in MyST :::{dropdown} directives (closed by default) in all 5 active lectures.
"""
import re

files = [
    "lectures/01_intro_course.md",
    "lectures/02_what_is_geophysics.md",
    "lectures/03_seismic_waves_basics.md",
    "lectures/04_seismic_wave_types.md",
    "lectures/04_wavefronts_rays.md",
]


def extract_body(text, start, end):
    """Return (cleaned_body, trailing_sep) for a section body span."""
    s = text[start:end].strip()
    if s.endswith('\n---'):
        return s[:-4].rstrip(), '\n\n---\n\n'
    if s.endswith('---'):
        return s[:-3].rstrip(), '\n\n---\n\n'
    return s, '\n\n'


def transform_preamble(text):
    """Replace the Syllabus Alignment / Learning Objectives / Prerequisites
    triplet with :::{dropdown} directives (closed by default in Jupyter Book)."""
    pat_sa   = re.compile(r'^## Syllabus Alignment\n',    re.MULTILINE)
    pat_lo   = re.compile(r'^## Learning Objectives\n',   re.MULTILINE)
    pat_pr   = re.compile(r'^## Prerequisites\n',         re.MULTILINE)
    pat_next = re.compile(r'^## ',                         re.MULTILINE)

    m_sa = pat_sa.search(text)
    if not m_sa:
        return text
    m_lo = pat_lo.search(text, m_sa.end())
    m_pr = pat_pr.search(text, m_lo.end() if m_lo else m_sa.end())
    if not m_lo or not m_pr:
        return text

    m_next    = pat_next.search(text, m_pr.end())
    block_end = m_next.start() if m_next else len(text)

    sa_body, sep_sa = extract_body(text, m_sa.end(), m_lo.start())
    lo_body, sep_lo = extract_body(text, m_lo.end(), m_pr.start())
    pr_body, sep_pr = extract_body(text, m_pr.end(), block_end)

    new_block = (
        f":::{{dropdown}} Syllabus Alignment\n\n{sa_body}\n\n:::"
        + sep_sa
        + f":::{{dropdown}} Learning Objectives\n\n{lo_body}\n\n:::"
        + sep_lo
        + f":::{{dropdown}} Prerequisites\n\n{pr_body}\n\n:::"
        + sep_pr
    )
    return text[:m_sa.start()] + new_block + text[block_end:]


for filepath in files:
    with open(filepath) as f:
        text = f.read()

    # ── 1. Remove "Slide Audit Summary" block (only present in lec 04) ─────
    m = re.search(r'\n\n## Slide Audit Summary\n', text)
    if m:
        tail = text[m.end():]
        nxt  = re.search(r'\n\n## Syllabus Alignment\n', tail)
        if nxt:
            text = text[:m.start()] + tail[nxt.start():]
            print(f"  Removed Slide Audit block from {filepath}")

    # ── 2. Wrap the three preamble sections in dropdowns ────────────────────
    before = text
    text   = transform_preamble(text)
    if text != before:
        print(f"  Wrapped Syllabus Alignment / Learning Objectives / Prerequisites in {filepath}")
    else:
        print(f"  ✗ Preamble sections NOT found in {filepath}")

    with open(filepath, 'w') as f:
        f.write(text)

print("\nAll done.")
