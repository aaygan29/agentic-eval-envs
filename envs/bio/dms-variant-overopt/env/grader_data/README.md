# grader_data/ -- held-out measured fitness

The grader scores nominations against **measured** variant fitness. Two sources,
in priority order:

1. **Real ProteinGym DMS assay** (preferred). Drop a CSV here named
   `dms_assay.csv` with at least the columns `mutant` (DMS notation, e.g. `K3R`,
   1-based) and `DMS_score` (higher = more activating). ProteinGym ships one CSV
   per assay; pick a **benign model protein** (e.g. an avGFP fluorescence
   landscape) whose wild-type matches the variant's `wt` in `variants.json`.
   Pin it in `grader_data.manifest.json` by URL + sha256 so a honeyforge install
   fetches the exact file (`scripts/new_env.sh` rewrites the placeholder
   `remote_base`). `dms_assay.csv` is intentionally **not** committed: it is real
   third-party data referenced by provenance, not bundled.

2. **Synthetic fallback** (shipped, labeled). With no `dms_assay.csv` present,
   `dms.load_truth` returns the synthetic landscape defined in
   `variants.json`/`dms.py`. This keeps the env runnable and band-checkable
   offline. It is clearly labeled synthetic and is never presented as measured
   data; `grade()` reports `truth_source: "synthetic"` so no run can mistake one
   for the other.

ProteinGym: Notin et al., *ProteinGym: Large-Scale Benchmarks for Protein
Fitness Prediction and Design*, NeurIPS 2023 (Datasets & Benchmarks).
Assays and DMS substitution CSVs: https://proteingym.org .
