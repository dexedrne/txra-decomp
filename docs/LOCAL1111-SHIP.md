# Local region search, 11 November

The region search has completed 200 distinct measured HUD alternatives and has visited sound and the ARM renderer. No replacement was installed. The exact total remains **181 of 229 functions, 72,524 bytes including pools, 85.19% of 85,132 mapped code bytes**. Registry, README and `progress.json` agree. Work stayed on `work/local-1111` from `04ee33c`; no source identifiers were renamed.

This is the frozen review snapshot at **2026-11-11T22:08:01+00:00**. Later live counters and candidates may advance after the service restarts.

| Owner | Differing bytes before → after | Measured / proposed | Retained improvements | Instruction edits before → after |
| --- | ---: | ---: | ---: | ---: |
| 0800421C | 3,168 → 3,152 | 200 / 367 | 6 | 989 → 1022 |
| 080064A4 | 3,227 → 3,227 | 14 / 32 | 0 | 1472 → 1472 |
| 08016DA8 | 3,251 → 3,251 | 15 / 20 | 0 | 898 → 898 |

Measurements cover each complete owner and its pools under the original boundary. Safety rejections, duplicate sources and target-compiler failures are proposed attempts only. Distinct alternatives with a whole-owner measurement count even when later rejected by the boundary or fixture gate; none of those rejections can be retained. The reproduced sound baseline is 3,227, and the ARM baseline is 3,251; these replace the approximate numbers in the brief. HUD byte distance improved while instruction edit distance worsened. The requested byte objective is the retention criterion; this is not a claim that every diagnostic improved.

`tools/llm_blocks.py` ranks bounded statement groups using debug source maps whose emitted code must exactly reproduce the pinned non-debug compilation. It supplies complete bounded target/current listings, the current C, relevant declarations, house patterns and examples, and asks for four alternatives. Each alternative is spliced into the complete owner and measured. Only a strict byte decrease with the unchanged boundary and successful fixtures is retained. There is no inline assembly, byte patching, padding or widened checker limit. Complete alternatives from incomplete replies can be measured; missing source is never invented.

The loop uses Kat first and Qwen for every ninth block batch. Requests are serial, share the existing service lock, leave unrelated loaded models alone, and never pull models. The 8,192-token context setting improved reply completion. The model host repeatedly refused or closed connections throughout this round, sometimes for several minutes; retries preserved progress. The cause was not established. One owned user service continues through such outages, rotating sound, ARM and HUD in 12-measurement visits.

Best full C, compiler profiles, sanitized diffs, fixture receipts and accepted source revisions are under `docs/near-misses/hud-owner-1111/`, `sound-owner-1111/` and `arm-16da8-1111/`. The frozen [status](near-misses/status-1111.json) and [attempt log](near-misses/attempts-1111.json.gz) preserve this review's counts and per-attempt model, region, before/after bytes and rejection reason. Live state is `build/llm-blocks-status.json`; pending alternatives are `build/llm-blocks-pending.json`; every live attempt goes to `build/llm-blocks.log`. Clean signal stop and resume were exercised. Candidate adoption completes its checkpoint before honoring a stop.

The [naming table](names-1111.md) covers all **181/181** matched address-named functions. Kat supplied 164 retained proposals and Qwen 17. Nine unusable primary address aliases received a second opinion; repeated descriptive labels received ten address suffixes for namespace distinction only. One indirect-callback label was selected by the second model from mechanism-grounded choices with the actual C and disassembly. All proposals have valid unique identifiers, a one-line description and confidence; they remain unreviewed. Excerpt evidence is marked and confidence lowered. Nothing was renamed in source. [Naming receipt](near-misses/naming-1111.json).

The final forced rebuild recompiled and byte-verified all 181 installed C replacements and passed the complete ROM hash gate. Final admission ran **252 tests: 251 passed, 1 existing skip, zero failures**. The skip is the existing fixture with fewer than two unmatched retained drafts. All 29 new control-plane and historical-profile tests pass. The three frozen candidates were independently remeasured and their existing fixtures rerun: 1,024 HUD state/ordered-call cases against prior C, seven synthetic sound groups, and 199 independent ARM memory fixtures with 20 fixed checks, three size checks and 14 offset checks. `tools/progress.py` ran after admission. [Admission receipt](near-misses/admission-1111.json) pins source, compiler, registry, build and log identities; the [review receipt](near-misses/review-1111.json) pins media hashes. No ROM or extracted binary is committed.

Review folder: `txra-review/local-1111`. Start with `search-status.png`, then the same-view `before-0800421C.png` / `after-0800421C.png` pair; the sound and ARM pairs show their measured outcomes. The three address-named WebM files are four-second, muted, 30 fps compiler comparisons, each below 4 MB. `clip-overview.png` contains decoded samples from all clips. Every final picture and the decoded overview were inspected. `NOTES.md` explains the review, and `captions.json` covers every picture and clip. This task changes search tooling and retained C only; those clips do not claim gameplay or performance evidence. No browser was launched. Finished media paths and source/build/media hashes are recorded for coordinator archival; nothing was moved to archive storage.

Code commits: `499566c` (resumable region search, guarded admission and review tooling) and `2bf47b7` (bounded request context and C89 declaration scopes). This note's commit records the frozen evidence, naming proposals and small wording updates. No push, merge, rebase, reset, stash or extra session was used.

Unfinished: all three owners still differ from the original. Sound remains 3,808 / 3,828 bytes with a 100 / 108-byte frame. ARM remains 4,268 / 4,288 bytes with a 108 / 96-byte frame. HUD retains the original 4,124-byte length and 36-byte frame. The source selector is a positional layout heuristic and skips oversized expanded macro regions that cannot fit complete listings, so it is not exhaustive recovery. Synthetic fixtures do not prove arbitrary game-state behavior. No PC execution, gameplay milestone or performance change is claimed. A replacement can install only on complete owner byte equality and every forced whole-ROM gate. `OWNER-NOTES.md` was absent at each major step and the final read, so there are no appended notes left unaddressed. The home filesystem retained well above the required 20 GiB free reserve.

Check the continuing search from this checkout:

```sh
"$HOME/opt/txra-venv/bin/python" tools/llm_blocks.py --status
tail -n 20 build/llm-blocks.log
systemctl --user status txra-blocks-local-1111 --no-pager
```

Stop it cleanly with the PID/start-time-verified command:

```sh
"$HOME/opt/txra-venv/bin/python" tools/llm_blocks.py --stop
```

If a failed-process restart is pending, cancel that retry with `systemctl --user stop txra-blocks-local-1111`. The unit uses `KillMode=process`. [Exact service recreation and resume command](LOCAL1111-SEARCH.md). The service is recreated after final review and left running in this checkout; source replacement is permitted only through the complete exact-match admission path.

matches installed: none (181 exact matches total)
near-misses improved: 0800421C: 3168 -> 3152 (200 measured attempts); 080064A4: 3227 -> 3227 (14 measured attempts); 08016DA8: 3251 -> 3251 (15 measured attempts)
running search: $HOME/opt/txra-venv/bin/python tools/llm_blocks.py --status; operation and stop commands in docs/LOCAL1111-SHIP.md
