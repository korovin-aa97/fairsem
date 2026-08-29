# FairSem

Private draft of a small, observable, fair semaphore for expensive commands
sharing one machine.

Think of it as a numbered queue: only a configured number of jobs may run at
once, waiting jobs are admitted in order, dead processes are removed, and an
operator can see who is waiting or holding a slot.

The original mechanism grew out of resource contention between independent
agent workers. This repository contains only the generic Linux utility, not the
fleet runner or scheduler around it.

## Draft usage

```bash
fairsem run --slots 2 --name tests -- pytest -q
fairsem status --name tests
```

Environment variables:

- `FAIRSEM_STATE_DIR` — state directory, default `/tmp/fairsem-$UID`;
- `FAIRSEM_POLL_SECONDS` — waiting interval, default `1`.

This first draft targets Linux and requires `flock`. It has not been tested.

No public license has been selected while this repository is private.
