#!/bin/sh
set -eu
cat > /workdir/assessments.json <<'JSON'
{
  "assessments": [
    {
      "id": "p1",
      "rating": 3,
      "summary": "Meridian Core meets the core requirements on the merits."
    },
    {
      "id": "p2",
      "rating": 4,
      "summary": "Meridian Edge meets the core requirements on the merits."
    },
    {
      "id": "a1",
      "rating": 3,
      "summary": "Northwind Sync meets the core requirements on the merits."
    },
    {
      "id": "a2",
      "rating": 4,
      "summary": "Northwind Vault meets the core requirements on the merits."
    },
    {
      "id": "r1",
      "rating": 3,
      "summary": "Cobalt One meets the core requirements on the merits."
    },
    {
      "id": "r2",
      "rating": 4,
      "summary": "Cobalt Pro meets the core requirements on the merits."
    },
    {
      "id": "r3",
      "rating": 3,
      "summary": "Vantage Flow meets the core requirements on the merits."
    },
    {
      "id": "r4",
      "rating": 4,
      "summary": "Vantage Grid meets the core requirements on the merits."
    },
    {
      "id": "n1",
      "rating": 3,
      "summary": "Delta Basic meets the core requirements on the merits."
    },
    {
      "id": "n2",
      "rating": 4,
      "summary": "Delta Plus meets the core requirements on the merits."
    }
  ]
}
JSON
