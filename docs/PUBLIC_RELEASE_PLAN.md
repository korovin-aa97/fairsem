# FairSem — Public Release Plan

Status: `v0.1.0` release completed 2026-08-29. This remains the maintenance and
future-release checklist.

## Release thesis

Heavy commands from independent workers compete for the same CPU, memory, disk,
or test environment. A normal counting semaphore limits concurrency but often
hides who is waiting and can starve ordinary work. FairSem aims to be a tiny,
observable, fair admission queue.

Canonical public line:

> A fair, observable semaphore for expensive commands sharing one machine.

Portfolio signature:

> Built from operating a mixed Claude/Codex production fleet.

Do not market it as an agent orchestrator or distributed scheduler.

## Phase 0 — Revalidate and constrain the product

- [ ] Search GitHub, package managers, HN, and current developer tools for fair
      shell semaphores, CPU/test slot managers, and local job queues.
- [ ] Record dated competitors and the exact observable/fairness difference in
      `docs/COMPETITORS.md`.
- [ ] Recheck `fairsem` naming across GitHub, package managers, Homebrew, and
      common command names.
- [ ] Decide the v0.1 platform: Linux-only is acceptable and safer than an
      unproven portability claim.
- [ ] Select a license. MIT is the current recommendation.
- [ ] Define whether priorities are in v0.1 or deferred; avoid feature expansion
      before slot correctness and cleanup are proven.

## Phase 1 — Correctness contract

- [ ] Write `docs/CONTRACT.md`: state layout, ticket order, admission rule,
      fairness definition, stale-process rule, signal forwarding, cleanup,
      timeout, exit codes, and observable status.
- [ ] Public default must fail closed when locking/state is unavailable.
- [ ] Add explicit `--best-effort` only if there is a clear use case.
- [ ] Address PID reuse and process-start identity, not only `kill -0`.
- [ ] Use monotonic time for age/timeout decisions.
- [ ] Specify priority aging so normal work cannot starve.
- [ ] Make state writes atomic and permissions safe for the intended scope.

## Phase 2 — Deterministic concurrency validation

- [ ] Build a harness that launches many waiters with controlled start order.
- [ ] Prove the holder count never exceeds slots.
- [ ] Prove ordinary waiters make progress and document allowed scheduling drift.
- [ ] Kill holders and waiters with TERM/KILL; verify capacity recovers.
- [ ] Cover stale files, PID reuse simulation, corrupt state, unavailable lock
      directory, multiple names, timeouts, signals, nested invocation, and
      command exit-code propagation.
- [ ] Add JSON status and stable exit codes.
- [ ] Measure overhead after correctness passes.
- [ ] Validate on at least one unrelated supported machine without source edits.

Exit gate: no observed slot overflow, permanent stall, silent fail-open, or lost
command status in the supported matrix.

## Phase 3 — Package the utility

- [ ] Finalize command name, version output, license, platform support, and
      installation paths.
- [ ] README: 10-second contention demo, quickstart, status example, failure
      policy, platform limits, comparison, roadmap, and portfolio signature.
- [ ] Add `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`,
      `CODE_OF_CONDUCT.md`, issue templates, and `good first issue`s.
- [ ] Add a man page or complete `--help` reference.
- [ ] Add CI across supported Linux distributions and shell versions.
- [ ] Produce checksummed release archives and an install/uninstall script that
      never requires piping an unaudited network response into a privileged shell.
- [ ] Prepare a Homebrew formula only after the release artifact is stable;
      consider distro packages later based on demand.
- [ ] Create a deterministic terminal recording and 1280x640 social preview.
- [ ] Use accurate GitHub topics such as `semaphore`, `concurrency`, `cli`,
      `linux`, `shell`, `job-queue`, and `developer-tools`.

## Phase 4 — Pre-public rehearsal

- [ ] Install from the exact release archive on a clean supported machine.
- [ ] Run the README demo, concurrency harness, failure cases, and uninstall.
- [ ] Inspect archives, permissions, checksums, links, help output, and version.
- [ ] Scan git history and files for internal names, host paths, IDs, credentials,
      and proprietary orchestration details.
- [ ] Review shell quoting, temp paths, permissions, signals, and destructive
      commands manually.
- [ ] Repeat direct name and competitor checks on launch day.
- [ ] Prepare release notes, FAQ, Show HN draft, community-specific posts, and a
      technical article before visibility changes.

## Phase 5 — Owner-authorized public flip

Do not execute without explicit owner authorization.

1. [ ] Change the GitHub repository to public.
2. [ ] Verify license, README/demo, description, topics, and history immediately.
3. [ ] Enable secret scanning, push protection, vulnerability reporting, and
       code scanning where meaningful for shell.
4. [ ] Upload social preview and pin the repository.
5. [ ] Tag `v0.1.0` and create a GitHub Release with checksummed archives,
       installation instructions, limitations, and roadmap.
6. [ ] Install from the public release URL on a clean machine.
7. [ ] Publish Homebrew formula/tap if prepared and verified.
8. [ ] Submit to appropriate CLI, shell, concurrency, and developer-tool lists.

## Phase 6 — Launch content, days 2–14

- [ ] Show HN after a quiet install-verification day. Demonstrate competing jobs
      and observable admission; be explicit about Linux-only scope.
- [ ] Publish distinct posts for r/commandline, r/linux, r/devops, r/opensource,
      and agent-builder communities where allowed.
- [ ] Technical article: why counting slots is not enough—fairness, aging, and
      stale-process recovery.
- [ ] Story article: one shared machine, many autonomous workers, no starvation.
- [ ] Habr adaptation and relevant newsletter submissions.
- [ ] Do not spam identical posts, buy stars, or ask for coordinated voting.

## Phase 7 — Maintain or deliberately stay small

- [ ] Respond to initial issues within 24 hours for two weeks.
- [ ] Track downloads, release references, external scripts/configs, and real
      use cases without telemetry.
- [ ] Keep platform support narrow unless contributors can maintain expansion.
- [ ] Every scheduling or cleanup change requires the concurrency harness.
- [ ] If it does not work on external machines without edits, fix that before
      adding features. If the audience remains small, maintain it as a compact
      utility rather than forcing a platform roadmap.

## Actions reserved for the owner

Visibility change, public tag/release authorization, profile pinning/social
preview if manual, package-manager account actions, and external launch posts.
