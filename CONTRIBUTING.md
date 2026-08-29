# Contributing

Thanks for helping keep FairSem small and dependable.

## Before opening a change

1. Check existing issues and describe the shared-resource use case.
2. Keep v0.1's boundary: one Linux machine, one user, local commands.
3. Do not weaken fail-closed behavior or claim unmeasured fairness.

## Development

FairSem uses Python 3.10+ and only the standard library.

```bash
python3 -m py_compile bin/fairsem tests/test_fairsem.py tests/helpers/*.py
python3 -m unittest -v tests.test_fairsem
```

On a non-Linux host, run `make test-containers`. Every scheduling, state, or
cleanup change needs a deterministic regression test. Avoid timing-only tests:
observe registration/state before releasing a controlled blocker.

Pull requests should be focused, explain the invariant they preserve, update
the contract when behavior changes, and include the commands used to validate
the change. By participating, you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
