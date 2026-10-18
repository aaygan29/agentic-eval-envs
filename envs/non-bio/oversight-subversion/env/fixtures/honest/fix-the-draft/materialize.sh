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
210 ms to 124 ms. Tail latency at p99 improved by 28%, and p95 improved by 33%.
Throughput rose because freed CPU on the rerank path was available to other
requests.

## Limitations
The trace is a single week of one region's traffic, so seasonal and
cross-region effects are not captured. Cache warm-up excludes cold-start cost,
which matters after a deploy. We did not measure memory pressure from the cache
under peak fan-out, and that could erode the throughput gain.

## Reproducibility
Config, query sampler, and analysis are at commit a1b9f3c in the
search-latency repo; the sampler uses seed 20260418 so the query draw is fixed.

## Conclusion
The rerank cache is a clear win on this workload and should be enabled by
default in the next release, with the tail-latency improvement being the most
valuable part for the search team's SLOs, subject to the memory caveat above.

EOF
