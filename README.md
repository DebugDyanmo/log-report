# log-report — Fixed Harbor Task

A Terminal-Bench 2 (Harbor) task: parse an Apache-style access log into a
small JSON summary report. This repo contains the corrected version of a
task that was originally broken across several axes of Harbor authoring.

## What was broken

**Format (`task.toml`)**
`artifacts` was a bare string instead of a top-level array, and it pointed
to `/app/out.json` — a path the solution never actually wrote to.

**Environment (`environment/Dockerfile`)**
- Used `FROM python:latest`, an unpinned floating tag — not reproducible.
- `COPY solution_hint.py /app/solution_hint.py` leaked the reference
  solution directly into the agent's own working directory.

**Verifier (`tests/`)**
- Only checked that `/app/report.json` existed and was non-empty — never
  parsed the JSON or validated any field. Garbage text or wildly wrong
  values would pass.
- `test.sh` wrote the reward to `/app/reward.txt` instead of the required
  `/logs/verifier/reward.txt`, and never produced `/logs/verifier/ctrf.json`
  despite `pytest-json-ctrf` being installed.

**Instruction (`instruction.md`)**
Vague prose with no numbered success criteria, no defined output path, and
no JSON schema — inconsistent with what a correct verifier should check.

## What was fixed

- `task.toml`: `artifacts` is now `["/app/report.json"]`, matching the
  solution's actual output path.
- `environment/Dockerfile`: base image pinned by digest
  `solution_hint.py` removed entirely from the build context.
- `tests/test_outputs.py`: rewritten to independently recompute the
  expected `total_requests`, `unique_ips`, and `top_path` from
  `access.log`, and assert the report matches — one test per
  `instruction.md` criterion, each with a docstring naming which
  criterion it verifies.
- `tests/test.sh`: writes `reward.txt` and `ctrf.json` to the correct
  `/logs/verifier/` path.
- `instruction.md`: rewritten with four explicit, numbered success
  criteria matching the verifier exactly.

## Verification evidence

Run both of the following from the task root with Harbor installed:

```bash
harbor run -p . -a oracle       # reference solution → reward 1
harbor run -p . --agent nop     # no-op agent        → reward 0
```

Results obtained:

| Run                    | Reward | Tests             |
|-------------------------|--------|-------------------|
| `-a oracle`             | 1.0    | 4/4 passed        |
| `--agent nop`           | 0.0    | 4/4 failed (file not found) |
| oracle w/ injected bug (`total_requests: total + 999`) | 0.0 | verifier correctly rejects wrong values |

The third row confirms the verifier checks actual computed values, not
just file existence — a deliberately wrong `solve.py` (inflating
`total_requests` by 999) was correctly scored 0.

## Structure

```
task.toml              # Harbor task definition
instruction.md          # Numbered, verifier-consistent instructions
environment/
  Dockerfile             # Reproducible, pinned, no leaked solution
  access.log             # Sample input log
solution/
  solve.py               # Reference solution
  solve.sh                # Oracle entrypoint
tests/
  test.sh                 # Verifier entrypoint (writes reward.txt + ctrf.json)
  test_outputs.py          # Per-criterion correctness checks
```
