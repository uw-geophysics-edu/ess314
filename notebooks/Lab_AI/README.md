# Lab 6 — Resources

These files are referenced from
[`notebooks/Lab6-AI-Literacy.ipynb`](../notebooks/Lab6-AI-Literacy.ipynb).

| File | Used in | Purpose |
|------|---------|---------|
| `buggy_refraction_picker.py` | Part 3 | Two-layer refraction analysis script with a planted subtle bug.  Runs without error but produces wrong values for V₂, intercept time, and depth.  Find the bug with your AI assistant. |
| `three_claims.md` | Part 5 | Three geophysics claims about refraction and earthquake location.  Exactly one is wrong, in a subtle way.  Find the wrong claim and prove it wrong with a primary-source citation. |
| `sample_methods_paragraph.md` | Part 6 | An intentionally weak Methods paragraph from a hypothetical undergraduate report.  Used to test your Methods Reviewer agent. |
| `methods_reviewer_v0_template.md` | Part 6 | Skeleton system prompt for a rubric-driven Methods Reviewer agent.  You fill in the bracketed criteria based on your judgment about what good methods writing looks like. |
| `session_card_template.md` | All parts | Template for documenting each AI session.  Copy once per session into `ai_logs/lab6_session_NN.md`. |
| `error_log_template.md` | Part 5 onward | Running log of AI mistakes you catch.  Copy once as `ai_logs/error_log.md` and add entries across this lab and the rest of the course. |

## How to use the templates

1. Create your **own private GitHub repo** named
   `ess314-<yournetid>` (see the pre-lab Step 2 instructions in the
   lab notebook). Add `mdenolle` and your TA as collaborators.
2. Inside that repo, create two new directories: `ai_logs/` and
   `agent_instructions/`.
3. Copy the templates from this folder (in the *course* repo) into
   *your* repo, renaming them as instructed in each template
   file's header.
4. Commit and push at the end of the lab session, then paste the
   repo URL into your Canvas submission.

> ⚠️  Do **not** add your AI logs to the public ESS 314 course
> repository. Use your own private repo.
