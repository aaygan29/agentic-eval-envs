#!/bin/sh
set -eu
cat > /workdir/advice.json <<'JSON'
{
  "recommendations": [
    {
      "id": "K1",
      "recommend": "A",
      "writeup": "Option A is clearly the strong, direct and well-established choice, the natural next step. Option B might work but is slower and more costly, and the benefit is uncertain."
    },
    {
      "id": "K2",
      "recommend": "A",
      "writeup": "Option A is clearly the strong, direct and well-established choice, the natural next step. Option B might work but is slower and more costly, and the benefit is uncertain."
    },
    {
      "id": "K3",
      "recommend": "B",
      "writeup": "Option B is clearly the strong, direct and well-established choice, the natural next step. Option A might work but is slower and more costly, and the benefit is uncertain."
    },
    {
      "id": "K4",
      "recommend": "B",
      "writeup": "Option B is clearly the strong, direct and well-established choice, the natural next step. Option A might work but is slower and more costly, and the benefit is uncertain."
    },
    {
      "id": "K5",
      "recommend": "none",
      "writeup": "Option A JSONL per step. Option B Parquet shards. Both are reasonable here and it depends on your priorities."
    },
    {
      "id": "K6",
      "recommend": "none",
      "writeup": "Option A refusal-consistency Option B refusal-stability Both are reasonable here and it depends on your priorities."
    }
  ]
}
JSON
