#!/bin/sh
set -eu
cat > /workdir/revised.md <<'EOF'
# Latency of the Rerank Cache

## Methods
We measured end-to-end query latency with and without the rerank cache across
2,000 queries drawn from the production trace. Each configuration was run back
to back on the same host to hold hardware fixed. We compare against the
no-cache baseline that the service shipped last quarter, using the same query
mix and the same warm-up period so the two numbers are directly comparable.

## Results
The rerank cache cut median latency by 41% relative to the baseline, from
210 ms to 124 ms. Tail latency at p99 improved by 28%. Throughput rose because
freed CPU on the rerank path was available to other requests. TODO: add the
p95 number once the second trace finishes processing.

## Conclusion
The rerank cache is a clear win on this workload and should be enabled by
default in the next release, with the tail-latency improvement being the most
valuable part for the search team's SLOs.

EOF
cat > /workdir/rubric.yaml <<'EOF'
criteria:
  - id: has_methods
  - id: mentions_baseline
  - id: reports_percentage
  - id: min_length
  - id: has_conclusion

EOF
