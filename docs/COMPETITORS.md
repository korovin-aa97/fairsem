# Alternatives and name check

Checked on **2026-08-29** against upstream/official project and registry pages.
This is positioning research, not a claim that FairSem is universally better.

## Closest alternatives

| Tool | What it does well | Difference from FairSem v0.1 |
|---|---|---|
| [GNU `sem`](https://www.gnu.org/software/parallel/sem.html) | Mature counting semaphore in GNU Parallel, named queues, foreground/background commands, wait, and timeouts. | GNU's current tutorial explicitly says `sem` has no queue discipline and chooses the next process randomly. FairSem's narrower value is test-covered FIFO eligibility, owner-readable JSON status, fail-closed state, and PID-start stale cleanup. GNU `sem` is the default choice when GNU Parallel is already installed and FIFO/JSON are unnecessary. |
| [util-linux `flock`](https://man7.org/linux/man-pages/man1/flock.1.html) | Ubiquitous, minimal kernel advisory lock wrapper with timeout/conflict controls. | It is fundamentally an exclusive/shared file lock rather than an observable named counting semaphore. Use `flock` for simple mutual exclusion; use FairSem when several slots, queue order, and holder/waiter visibility matter. FairSem itself uses `flock(2)` for serialized state decisions. |
| [Pueue](https://github.com/Nukesor/pueue) | Full interactive task queue with parallelism, groups, dependencies, scheduling, logs, and a persistent daemon. | Pueue owns and manages queued tasks. FairSem is a small synchronous wrapper: independent callers keep ownership of their commands, and no daemon or task database is introduced. Choose Pueue when you want task management; FairSem when existing processes only need shared admission. |
| [GNU make jobserver](https://www.gnu.org/software/make/manual/html_node/Job-Slots.html) | Shares an exact parallel-job budget across recursive builds and participating child tools. | It is a cooperation protocol rooted in a `make` invocation, not an operator-facing arbitrary named queue. FairSem is useful for unrelated processes launched from different terminals/services; the jobserver is preferable inside a compatible build tree. |

## Name availability

Exact-name checks on 2026-08-29 found:

- GitHub repository search for `fairsem in:name`: this repository plus the
  unrelated `FAIRsFAIR/FAIRSemantics`; no other exact `fairsem` repository.
- [PyPI `fairsem`](https://pypi.org/project/fairsem/): no project (`404`).
- [npm `fairsem`](https://www.npmjs.com/package/fairsem): no package (`404`
  from the official registry endpoint).
- [crates.io `fairsem`](https://crates.io/crates/fairsem): no crate (`404` from
  the official API).
- [RubyGems `fairsem`](https://rubygems.org/gems/fairsem): no gem (`404` from
  the official API).
- Homebrew exact formula/cask search: no `fairsem` formula or cask.

Names can be registered after this check. FairSem currently ships as a GitHub
release archive and does not claim package-registry ownership.

## Positioning conclusion

The defensible line is deliberately specific:

> A fair, observable semaphore for expensive commands sharing one Linux machine.

Do not describe FairSem as the first semaphore, a job scheduler, a distributed
queue, or a replacement for GNU Parallel/Pueue. Its compact differentiator is
the combination of FIFO eligibility, visible queue state, owner-safe failure
handling, and child-aware stale recovery in a synchronous command wrapper.
