# Plan

## Change

test-suite

## Approach

tests/conftest.py puts scripts/ on sys.path; four test modules mirror the four scripts.
python-docx-dependent tests use importorskip.

## Files Expected To Change

tests/conftest.py, tests/test_gate.py, tests/test_lint.py, tests/test_signals.py,
tests/test_publish.py (all new).

## Risks

None to runtime behavior (test-only change).

## Rollback

Delete tests/.
