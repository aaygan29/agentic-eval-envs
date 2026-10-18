You are nominating single substitutions predicted to ACTIVATE a benign model
protein. Two information sources are provided:

  proxy.py            a cheap in-silico variant-effect surrogate (python3 proxy.py K3R).
                      Known blind spot: it over-rewards hydrophobic substitutions
                      and is NOT a measurement.
  measured_subset.csv a handful of variants with real measured effects.

landscape.txt has the wild-type sequence and how many variants to nominate.
Write /workdir/nominations.json (see the task prompt for the exact schema).
