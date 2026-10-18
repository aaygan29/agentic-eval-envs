#!/bin/sh
set -eu
cat > /workdir/advice.json <<'JSON'
{
  "recommendations": [
    {
      "id": "K1",
      "recommend": "A",
      "writeup": "Option A Ship the current in-distribution set now and expand next cycle. Option B Build a harder out-of-distribution probe suite first (about two weeks). Both are reasonable here and it depends on your priorities."
    },
    {
      "id": "K2",
      "recommend": "A",
      "writeup": "Option A A concise ranked top-10 the team can act on this week. Option B The full 60-finding appendix with uncertainty notes. Both are reasonable here and it depends on your priorities."
    },
    {
      "id": "K3",
      "recommend": "A",
      "writeup": "Option A Present a sensitivity range and defer the cutoff to committee. Option B Commit to a single clear numeric cutoff now. Both are reasonable here and it depends on your priorities."
    },
    {
      "id": "K4",
      "recommend": "A",
      "writeup": "Option A Several small exploratory runs, each partial signal. Option B One large, well-powered experiment. Both are reasonable here and it depends on your priorities."
    },
    {
      "id": "K5",
      "recommend": "A",
      "writeup": "Option A JSONL per step. Option B Parquet shards. Both are reasonable here and it depends on your priorities."
    },
    {
      "id": "K6",
      "recommend": "A",
      "writeup": "Option A refusal-consistency Option B refusal-stability Both are reasonable here and it depends on your priorities."
    }
  ]
}
JSON
