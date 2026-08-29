# FairSem v0.1 contract

This document defines behavior users and automation may rely on in `0.1.x`.

## Scope

FairSem is a local, owner-scoped admission semaphore for Linux with `/proc`.
Python 3.10+ is required. It is not a distributed lock and does not isolate
mutually untrusted processes sharing one Unix account.

## State and locking

- State defaults to `/tmp/fairsem-$UID`; `FAIRSEM_STATE_DIR` overrides it.
- The state root and each named directory must be real directories, owned by
  the effective user, with mode `0700`. The lock must be owner-owned `0600`.
- All admission, configuration, cleanup, and snapshot decisions happen under
  an exclusive `flock(2)` lock for that semaphore name.
- JSON records are written to a same-directory temporary file, flushed, and
  atomically renamed. Counter updates are also atomic under the lock.
- Names match `[A-Za-z0-9][A-Za-z0-9._-]{0,63}` and cannot traverse paths.
- State/config corruption causes exit `70` and does not run a requested
  command. `repair` explicitly quarantines malformed holder/waiter records;
  config/counter repair remains a manual, inspect-first operation.

## Tickets and admission

Registration increments a persistent integer while holding the kernel lock.
The zero-padded counter is the ticket's ordering key.

For one slot, the oldest live waiter is the only eligible waiter. For `N`
slots, the oldest `available = N - holders` waiters are eligible. Kernel
scheduling may reorder command start within that eligible group, so the bound
on overtaking is `N - 1`. A continuous stream of newer work cannot prevent an
older live waiter from becoming eligible.

Priorities are not supported in v0.1. This intentionally makes starvation
freedom testable without an aging policy.

The first caller configures a named semaphore. A matching count is accepted.
A different count exits `65` while there are records and atomically replaces
the config only when the semaphore is idle.

## Process identity and stale cleanup

New records contain the Linux boot ID plus PID and `/proc/PID/stat` start
ticks. A PID is live only when the available identity fields still match and
its process is not a zombie. This handles PID reuse and persistent custom state
across reboots while remaining compatible with v0.1.0 records.

- Waiting records track the FairSem wrapper.
- A newly admitted record briefly tracks the wrapper while a child waits on a
  one-byte launch gate. The child cannot execute the requested command until
  its durable PID/start identity is stored.
- Once admitted through that gate, a holder tracks the command child. If the wrapper receives
  `SIGKILL`, a live child continues consuming its slot.
- Every operation removes demonstrably dead waiters/holders under the lock.
- Failure to persist a launched child's identity terminates that child before
  releasing capacity.

If the wrapper dies before opening the launch gate, pipe EOF makes the child
exit without executing the command. If it dies after opening the gate, the
durable child record preserves capacity. This closes the userspace
spawn/accounting gap even for wrapper `SIGKILL`.

## Time, timeout, and cancellation

Wait deadlines and displayed wait duration use `time.monotonic`; wall-clock
changes do not extend or shorten timeout decisions. The deadline includes
waiting for the state lock as well as waiting for capacity. `--timeout 0`
performs one immediate lock/admission attempt. A timeout removes the ticket
when possible and exits `75` without launching the command. State-lock waits
without a user deadline fail closed after five seconds instead of hanging.

`INT`, `TERM`, and `HUP` while waiting cancel and remove the waiter, returning
`128 + signal`. While holding, they are forwarded to the command's new process
group. Commands that daemonize or escape that group are outside this contract.

Nested acquisition of the same name is rejected with `65`, preventing the
common one-slot self-deadlock. Nested acquisition of a different name is
allowed; cross-name lock-order deadlocks remain the caller's responsibility.

## Fail-closed and best-effort behavior

Default setup, ownership, permission, or lock failure exits `73` without
running the command. Unreadable/corrupt state exits `70`. Configuration errors
exit `65`.

`--best-effort` applies only when secure state setup or locking is unavailable
during initial registration. It prints `WARNING` to stderr and runs the command
without admission, while preserving signal forwarding and command exit status.
It never bypasses corrupt records or slot mismatch.

## Status schema

`status --json` emits one compact JSON object with these stable `0.1.x`
top-level keys:

```json
{"available":2,"cleanup":{"removed_holders":0,"removed_waiters":0},"holders":[],"in_use":0,"name":"build","schema":1,"slots":2,"waiters":[]}
```

An unseen name has `slots: null` and `available: null`. Holder/waiter entries
contain `ticket`, wrapper `pid`, optional `command_pid`, `argv`, `enqueued_at`,
and monotonic-derived `wait_ms`. Additive entry fields may appear in `0.1.x`;
the top-level schema number changes for incompatible formats.

Status performs visible stale cleanup and reports counts in `cleanup`. Human
status is intended for people; scripts should use JSON.

## Exit codes

| Code | Meaning |
|---:|---|
| `0–255` | A launched command's status is preserved. |
| `64` | CLI usage error before launch. |
| `65` | Invalid name/config, slot mismatch, or same-name nesting. |
| `69` | Unsupported platform or missing `/proc` identity. |
| `70` | Unreadable, corrupt, or inconsistent state. |
| `73` | State directory or lock unavailable/unsafe. |
| `75` | Wait timeout; command was not launched. |
| `126` | Command could not be executed. |
| `128+N` | Wrapper/command terminated by signal `N`. |

Because a launched command's exit code is preserved, it may coincide with a
FairSem-reserved code. Diagnostics on stderr distinguish pre-launch failures.
