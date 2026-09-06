#!/usr/bin/env sh
set -eu

fairsem_bin=${FAIRSEM_BIN:-./bin/fairsem}
demo_state=$(mktemp -d)

cleanup() {
  rm -r -- "$demo_state"
}
trap cleanup EXIT HUP INT TERM

export FAIRSEM_STATE_DIR="$demo_state"

printf '\033c'
printf '%s\n' '$ # Five jobs compete for two safe slots.'
printf '%s\n\n' '$ for job in 1 2 3 4 5; do fairsem run --name demo --slots 2 -- COMMAND & done'

for job in 1 2 3 4 5; do
  # $1 is intentionally expanded by the child shell, not this recording script.
  # shellcheck disable=SC2016
  "$fairsem_bin" run --name demo --slots 2 -- \
    sh -c 'sleep "$1"' "job-$job" 3 &
  until "$fairsem_bin" status --name demo --json | python3 -c '
import json
import sys

snapshot = json.load(sys.stdin)
expected = int(sys.argv[1])
raise SystemExit(0 if snapshot["in_use"] + len(snapshot["waiters"]) == expected else 1)
' "$job"; do
    sleep 0.02
  done
done

printf '%s\n' '$ fairsem status --name demo'
"$fairsem_bin" status --name demo

sleep 3.1
printf '\n%s\n' '$ # The oldest waiting group takes the freed slots.'
"$fairsem_bin" status --name demo

sleep 3.1
printf '\n%s\n' '$ # The last waiter runs; capacity never exceeds two.'
"$fairsem_bin" status --name demo

wait
printf '\n%s\n' '$ # Queue drained.'
"$fairsem_bin" status --name demo
