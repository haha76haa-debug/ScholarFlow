# E2E Test Infra: Zotero-Obsidian Academic Knowledge Base

## Test Philosophy
- Opaque-box, requirement-driven testing covering the entire knowledge base lifecycle.
- Verification mechanism operates against user contracts, CLI commands, file system invariants, frontmatter schemas, link integrity, and visual canvas validities.
- Progressive testability: Tier 1 (Unit & Schema Contracts), Tier 2 (CLI Functional Commands), Tier 3 (Cross-Feature Graph & Integrity), Tier 4 (Full Vault Lifecycle & Real-World Ingestion).

## Feature Inventory & Test Mapping
| # | Feature | Requirement | Tier 1 (Schema/Unit) | Tier 2 (CLI/Boundary) | Tier 3 (Pairwise/Graph) | Tier 4 (E2E Scenario) |
|---|---------|-------------|:--------------------:|:---------------------:|:-----------------------:|:---------------------:|
| 1 | Vault Directory Structure | R1 §Vault Scaffolding | ✓ (dir existence) | ✓ (empty dir handling) | ✓ (cross-dir links) | ✓ (full vault scaffold) |
| 2 | Frontmatter Schema Contracts | R1 §Frontmatter Schemas | ✓ (schema validation) | ✓ (missing field error)| ✓ (type mismatch) | ✓ (all paper/concept notes) |
| 3 | Core Obsidian Templates | R1 §Templates | ✓ (template syntax) | ✓ (rendering validity) | ✓ (placeholder integrity) | ✓ (instantiation into note) |
| 4 | JSON Canvas v1.0 Spec | R1 §Canvas Schema | ✓ (JSON structure) | ✓ (node/edge parsing) | ✓ (dangling edge checks) | ✓ (rendered in Obsidian) |
| 5 | Zotero Nunjucks Template | R2 §Zotero Template | ✓ (Nunjucks syntax) | ✓ (edge case items) | ✓ (annotation callouts) | ✓ (Zotero export to note) |
| 6 | Citekey & Field Mappings | R2 §Better BibTeX | ✓ (citekey regex) | ✓ (special chars/colls)| ✓ (bibtex vs CSL-JSON) | ✓ (real paper citekeys) |
| 7 | PDF Annotation Taxonomy | R2 §Annotations | ✓ (6 color classes) | ✓ (missing color code) | ✓ (callout conversion) | ✓ (deep link integrity) |
| 8 | Evidence Record Contract | R2 §Evidence Record | ✓ (evidence fields) | ✓ (claim strength enum)| ✓ (claim-source link) | ✓ (claim promotion gate) |
| 9 | Agent Protocols (CLAUDE/AGENT)| R3 §Agent Protocols | ✓ (section checklist)| ✓ (prohibited commands)| ✓ (link conventions) | ✓ (simulated agent loop) |
| 10| `kb_tools` Package & CLI | R4 §Package Architecture | ✓ (import/entrypoint)| ✓ (help & invalid flags)|✓ (JSON vs text output) | ✓ (pip / python -m run) |
| 11| CLI `lint` Subcommand | R4 §Linter | ✓ (valid note lint) | ✓ (invalid frontmatter)| ✓ (tag/heading lints) | ✓ (whole vault lint run) |
| 12| CLI `sync_registry` Subcommand | R4 §Registry | ✓ (table generator) | ✓ (empty/duplicate keys)|✓ (registry link parity) | ✓ (incremental vault sync)|
| 13| CLI `check_links` & `repair` | R4 §Link Checker | ✓ (broken link detect)| ✓ (alias/anchor links) | ✓ (auto-repair fuzzy) | ✓ (vault heal cycle) |
| 14| CLI `synthesize` Subcommand | R4 §Synthesizer | ✓ (claim extractor) | ✓ (matrix alignment) | ✓ (multi-paper synth) | ✓ (topic summary gen) |
| 15| CLI `generate_canvas` Subcmd | R4 §Canvas Generator | ✓ (canvas json gen) | ✓ (isolated nodes) | ✓ (edge color/rel labels)| ✓ (dynamic canvas gen) |
| 16| CLI `ingest` Subcommand | R4 §BibTeX Ingestion | ✓ (bibtex parser) | ✓ (unicode/math syntax)| ✓ (auto-link concepts) | ✓ (batch bibtex import) |
| 17| Real Paper: ResNet Note | R5 §Paper Examples | ✓ (frontmatter check)| ✓ (heading contracts) | ✓ (evidence & concept) | ✓ (synthesis inclusion) |
| 18| Real Paper: Transformer Note | R5 §Paper Examples | ✓ (frontmatter check)| ✓ (heading contracts) | ✓ (evidence & concept) | ✓ (synthesis inclusion) |
| 19| Real Paper: LoRA Note | R5 §Paper Examples | ✓ (frontmatter check)| ✓ (heading contracts) | ✓ (evidence & concept) | ✓ (synthesis inclusion) |
| 20| Concept & Synthesis Network | R5 §Knowledge Graph | ✓ (concept schema) | ✓ (isolated concepts) | ✓ (dense cross-linking)| ✓ (end-to-end traversal) |
| 21| Literature Canvas Map | R5 §Canvas Visual Map | ✓ (v1.0 validation) | ✓ (coordinates layout) | ✓ (connected relations) | ✓ (obsidian loadable) |
| 22| Comprehensive README.md | R5 §Documentation | ✓ (section headers) | ✓ (code snippet check) | ✓ (command reference) | ✓ (walkthrough verified) |

## Test Architecture
- **Framework**: `pytest`
- **Invocation**: `pytest -v tests/`
- **Pass Semantics**: All test suites in `tests/` pass with zero failures and exit code 0.
- **Directory Layout**:
  ```
  tests/
  ├── conftest.py                # Fixtures, test vault generators, mock Zotero data
  ├── test_linter.py             # Tier 1 & 2 tests for lint subcommand and schema rules
  ├── test_registry.py           # Tier 1 & 2 tests for sync_registry subcommand
  ├── test_link_checker.py       # Tier 1 & 2 tests for check_links and repair_links
  ├── test_synthesizer.py        # Tier 1 & 2 tests for synthesize subcommand
  ├── test_canvas_gen.py         # Tier 1 & 2 tests for generate_canvas subcommand
  ├── test_ingest.py             # Tier 1 & 2 tests for ingest subcommand
  └── test_e2e.py                # Tier 3 & Tier 4 end-to-end integration workflows
  ```

## Real-World Application Scenarios (Tier 4)
1. **Scenario 1: Fresh Vault Bootstrap & Scaffold Verification**: Verify creating a new vault from scratch, applying templates, and validating directory schemas.
2. **Scenario 2: Real Academic Ingestion to Knowledge Synthesis**: Ingest raw BibTeX for ResNet, Transformer, and LoRA, run `lint`, create atomic concepts, run `synthesize`, generate `Maps/literature.canvas`, run `sync_registry`, and verify zero lint errors and zero broken links.
3. **Scenario 3: Corrupted Vault Healing & Idempotency**: Intentionally inject frontmatter typos, corrupted citekeys, and broken wikilinks into a test vault. Verify `kb-tools lint` identifies all defects, `kb-tools repair-links` heals broken links, and re-running `sync_registry` and `lint` results in a clean, idempotent state.

## Coverage Thresholds
- **Tier 1 (Unit & Schema Tests)**: >= 25 test cases
- **Tier 2 (Boundary & Corner Cases)**: >= 25 test cases
- **Tier 3 (Cross-Feature & Pairwise)**: >= 15 test cases
- **Tier 4 (Real-World E2E Scenarios)**: >= 5 comprehensive scenarios
- **Total Test Suite**: >= 70 test cases with 100% pass rate.
