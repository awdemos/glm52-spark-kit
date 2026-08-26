You are a focused subagent reviewer for a single holistic investigation batch.

Repository root: /var/home/a/code/glm52-spark-kit
Blind packet: /var/home/a/code/glm52-spark-kit/.desloppify/review_packet_blind.json
Batch index: 17
Batch name: design_coherence
Batch rationale: design_coherence review

DIMENSION TO EVALUATE:

## design_coherence
Are structural design decisions sound — functions focused, abstractions earned, patterns consistent?
Look for:
- Functions doing too many things — multiple distinct responsibilities in one body
- Parameter lists that should be config/context objects — many related params passed together
- Files accumulating issues across many dimensions — likely mixing unrelated concerns
- Deep nesting that could be flattened with early returns or extraction
- Repeated structural patterns that should be data-driven
Skip:
- Functions that are long but have a single coherent responsibility
- Parameter lists where grouping would obscure meaning — do NOT recommend config/context objects or dependency injection wrappers just to reduce parameter count; only group when the grouping has independent semantic meaning
- Files that are large because their domain is genuinely complex, not because they mix concerns
- Nesting that is inherent to the problem (e.g., recursive tree processing)
- Do NOT recommend extracting callable parameters or injecting dependencies for 'testability' — direct function calls are simpler and preferred unless there is a concrete decoupling need

YOUR TASK: Read the code for this batch's dimension. Judge how well the codebase serves a developer from that perspective. The dimension rubric above defines what good looks like. Cite specific observations that explain your judgment.

Mechanical scan evidence — navigation aid, not scoring evidence:
The blind packet contains `holistic_context.scan_evidence` with aggregated signals from all mechanical detectors — including complexity hotspots, error hotspots, signal density index, boundary violations, and systemic patterns. Use these as starting points for where to look beyond the seed files.

Mechanical concern signals — investigate and adjudicate:
Overview (125 signals):
  mixed_responsibilities: 78 — aeon-crossnode-graphs/overlays/b12x/attention/indexer/tiled_topk.py, aeon-crossnode-graphs/overlays/b12x/integration/sparse_mla_scratch.py, ...
  design_concern: 37 — benchmarks/comm/dcp_gather_equivalence.py, benchmarks/comm/nccl_p2p_emulation.py, ...
  interface_design: 6 — campaign-2026-08/sircl/upstream/scripts/qualify_direct_cable.py, overlays/vllm/v1/attention/backends/mla/sm12x_mqa.py, ...
  duplication_design: 2 — campaign-2026-08/sircl/upstream/nccl/probe_dcp2_collectives.py, kernels/cute/w8a16_smallm_gemv.py
  structural_complexity: 2 — overlays/vllm/config/speculative.py, overlays/vllm/model_executor/models/deepseek_mtp.py

For each concern, read the source code and report your verdict in issues[]:
  - Confirm → full issue object with concern_verdict: "confirmed"
  - Dismiss → minimal object: {concern_verdict: "dismissed", concern_fingerprint: "<hash>"}
    (only these 2 fields required — add optional reasoning/concern_type/concern_file)
  - Unsure → skip it (will be re-evaluated next review)

  - [design_concern] benchmarks/comm/dcp_gather_equivalence.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (30 LOC): zero importers, not an entry point
    fingerprint: 815ef5fe3c34811b
  - [design_concern] benchmarks/comm/nccl_p2p_emulation.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (34 LOC): zero importers, not an entry point
    fingerprint: f5001fc2ed01f7cc
  - [design_concern] benchmarks/patch_gloo_probe.py
    summary: Design signals from orphaned
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned
    evidence: [orphaned] Orphaned file (32 LOC): zero importers, not an entry point
    fingerprint: 37b37cb1e0f3fcd2
  - [design_concern] benchmarks/patch_shm_probe.py
    summary: Design signals from orphaned
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned
    evidence: [orphaned] Orphaned file (67 LOC): zero importers, not an entry point
    fingerprint: a6e52f787a258bb5
  - [design_concern] benchmarks/profile/analyze_trace.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (51 LOC): zero importers, not an entry point
    fingerprint: 8b95caf5aa3f980d
  - [design_concern] benchmarks/sharedprefix_probe.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (128 LOC): zero importers, not an entry point
    fingerprint: 1fa9e7e49b4f6bfe
  - [design_concern] benchmarks/spec_metrics.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (30 LOC): zero importers, not an entry point
    fingerprint: 31f27a773a99ce1a
  - [design_concern] campaign-2026-08/images/bake_overlays.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (39 LOC): zero importers, not an entry point
    fingerprint: 52146325c53c4542
  - [design_concern] campaign-2026-08/images/sidecar_regen.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (34 LOC): zero importers, not an entry point
    fingerprint: 39733aef20fb1c5e
  - [design_concern] campaign-2026-08/sircl/upstream/integrations/vllm/sitecustomize.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (57 LOC): zero importers, not an entry point
    fingerprint: 2d69262981411866
  - [design_concern] campaign-2026-08/sircl/upstream/integrations/vllm/spark_collective_audit.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (318 LOC): zero importers, not an entry point
    fingerprint: b5b8c3fb2270dc80
  - [design_concern] campaign-2026-08/sircl/upstream/integrations/vllm/spark_dcp_collective_audit.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (204 LOC): zero importers, not an entry point
    fingerprint: c3a8162cae567cab
  - [design_concern] campaign-2026-08/sircl/upstream/integrations/vllm/spark_tp4_query_row_provider.py
    summary: Design signals from global_mutable_config, orphaned
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: global_mutable_config, orphaned
    evidence: [orphaned] Orphaned file (164 LOC): zero importers, not an entry point
    fingerprint: 5a8d46180686f3c0
  - [design_concern] campaign-2026-08/tailquant/codec/mcg_codec.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (166 LOC): zero importers, not an entry point
    fingerprint: 5579d5de4697bf39
  - [design_concern] campaign-2026-08/tailquant/split.py
    summary: Design signals from dict_keys, orphaned
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: dict_keys, orphaned
    evidence: [orphaned] Orphaned file (114 LOC): zero importers, not an entry point
    fingerprint: b2e9b54bfd789744
  - [design_concern] dspark-training/glmdatadrive.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (59 LOC): zero importers, not an entry point
    fingerprint: 098b58ad97ff2356
  - [design_concern] dspark-training/glmdeepdrive.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (49 LOC): zero importers, not an entry point
    fingerprint: bc2cda2e6d3d5e26
  - [design_concern] gates/nvfp4_writer_gate.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (56 LOC): zero importers, not an entry point
    fingerprint: 3a3e4d9ceda6a0a5
  - [design_concern] kernels/cute/marlin_w8a16_baseline.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (37 LOC): zero importers, not an entry point
    fingerprint: 7bcc9dba1d457f7f
  - [design_concern] kernels/cute/w8a16_smallm_gemv_v4.py
    summary: Design signals from orphaned
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned
    evidence: [orphaned] Orphaned file (149 LOC): zero importers, not an entry point
    fingerprint: 8592d73082bed715
  - [design_concern] kernels/nvfp4_writer_triton.standalone.py
    summary: Design signals from global_mutable_config, orphaned
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: global_mutable_config, orphaned
    evidence: [orphaned] Orphaned file (232 LOC): zero importers, not an entry point
    fingerprint: c38d0ca01ba94075
  - [design_concern] overlays/b12x/integration/sparse_mla_scratch.py
    summary: Design signals from structural
    question: Review the flagged patterns — are they design problems that need addressing, or acceptable given the file's role?
    evidence: Flagged by: structural
    evidence: File size: 521 lines
    fingerprint: 5ea5d0a8780427e6
  - [design_concern] overlays/dspark-ring/cp_utils.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (299 LOC): zero importers, not an entry point
    fingerprint: dbed340f806973b3
  - [design_concern] overlays/dspark-ring/speculators_algos.py
    summary: Design signals from global_mutable_config, orphaned
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: global_mutable_config, orphaned
    evidence: [orphaned] Orphaned file (191 LOC): zero importers, not an entry point
    fingerprint: bcd723e710ea9a6d
  - [design_concern] overlays/vllm/model_executor/layers/attention/builda_bmm_v1.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (112 LOC): zero importers, not an entry point
    fingerprint: dd19cd95f47355ba
  - [design_concern] overlays/vllm/model_executor/layers/logits_processor.py
    summary: Design signals from orphaned
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned
    evidence: [orphaned] Orphaned file (350 LOC): zero importers, not an entry point
    fingerprint: 4ce8c074f5835d2f
  - [design_concern] overlays/vllm/v1/attention/backends/mla/patch_deep_gemm_ops.py
    summary: Design signals from orphaned, smells
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, smells
    evidence: [orphaned] Orphaned file (119 LOC): zero importers, not an entry point
    fingerprint: 588b1c07c9438f4b
  - [design_concern] overlays/vllm/v1/attention/backends/mla/sparse_utils.py
    summary: Design signals from orphaned
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned
    evidence: [orphaned] Orphaned file (388 LOC): zero importers, not an entry point
    fingerprint: 24d501b292d28066
  - [design_concern] overlays/vllm/v1/attention/backends/registry.py
    summary: Design signals from global_mutable_config, orphaned
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: global_mutable_config, orphaned
    evidence: [orphaned] Orphaned file (298 LOC): zero importers, not an entry point
    fingerprint: 332e84d7b10fa7b6
  - [design_concern] overlays/vllm/v1/kv_cache_interface.py
    summary: Design signals from orphaned, structural
    question: Is this file truly dead, or is it used via a non-import mechanism (dynamic import, CLI entry point, plugin)?
    evidence: Flagged by: orphaned, structural
    evidence: File size: 1037 lines
    fingerprint: 6b9fb98efbc43cc9
  (+95 more — use `desloppify show <detector> --no-budget` to explore)

RELEVANT FINDINGS — explore with CLI:
These detectors found patterns related to this dimension. Explore the findings,
then read the actual source code.

  desloppify show boilerplate_duplication --no-budget      # 120 findings
  desloppify show dict_keys --no-budget      # 13 findings
  desloppify show dupes --no-budget      # 377 findings
  desloppify show global_mutable_config --no-budget      # 34 findings
  desloppify show orphaned --no-budget      # 116 findings
  desloppify show props --no-budget      # 11 findings
  desloppify show responsibility_cohesion --no-budget      # 17 findings
  desloppify show signature --no-budget      # 18 findings
  desloppify show smells --no-budget      # 302 findings
  desloppify show structural --no-budget      # 69 findings
  desloppify show uncalled_functions --no-budget      # 10 findings
  desloppify show unused --no-budget      # 24 findings
  desloppify show unused_enums --no-budget      # 8 findings

Report actionable issues in issues[]. Use concern_verdict and concern_fingerprint
for findings you want to confirm or dismiss.

Phase 1 — Observe:
1. Read the blind packet's `system_prompt` — scoring rules and calibration.
2. Study the dimension rubric (description, look_for, skip).
3. Review the existing characteristics list — which are settled? Which are positive? What needs updating?
4. Explore the codebase freely. Use scan evidence, historical issues, and mechanical findings as navigation aids.
5. Adjudicate mechanical concern signals (confirm/dismiss with fingerprint).
6. Augment the characteristics list via context_updates: positive patterns (positive: true), neutral characteristics, design insights.
7. Collect defects for issues[].
8. Respect scope controls: exclude files/directories marked by `exclude`, `suppress`, or non-production zone overrides.
9. Output a Phase 1 summary: list ALL characteristics for this dimension (existing + new, mark [+] for positive) and all defects collected. This is your consolidated reference for Phase 2.

Phase 2 — Judge (after Phase 1 is complete):
10. Keep issues and scoring scoped to this batch's dimension.
11. Return 0-10 issues for this batch (empty array allowed).
12. For design_coherence, use evidence from `holistic_context.scan_evidence.signal_density` — files where multiple mechanical detectors fired. Investigate what design change would address multiple signals simultaneously. Check `scan_evidence.complexity_hotspots` for files with high responsibility cluster counts.
13. Workflow integrity checks: when reviewing orchestration/queue/review flows,
14. xplicitly look for loop-prone patterns and blind spots:
15. - repeated stale/reopen churn without clear exit criteria or gating,
16. - packet/batch data being generated but dropped before prompt execution,
17. - ranking/triage logic that can starve target-improving work,
18. - reruns happening before existing open review work is drained.
19. If found, propose concrete guardrails and where to implement them.
20. Complete `dimension_judgment`: write dimension_character (synthesizing characteristics and defects) then score_rationale. Set the score LAST.
21. Output context_updates with your Phase 1 observations. Use `add` with a clear header (5-10 words) and description (1-3 sentences focused on WHY, not WHAT). Positive patterns get `positive: true`. New insights can be `settled: true` when confident. Use `settle` to promote existing unsettled insights. Use `remove` for insights no longer true. Omit context_updates if no changes.
22. Do not edit repository files.
23. Return ONLY valid JSON, no markdown fences.

Scope enums:
- impact_scope: "local" | "module" | "subsystem" | "codebase"
- fix_scope: "single_edit" | "multi_file_refactor" | "architectural_change"

Output schema:
{
  "batch": "design_coherence",
  "batch_index": 17,
  "assessments": {"<dimension>": <0-100 with one decimal place>},
  "dimension_notes": {
    "<dimension>": {
      "evidence": ["specific code observations"],
      "impact_scope": "local|module|subsystem|codebase",
      "fix_scope": "single_edit|multi_file_refactor|architectural_change",
      "confidence": "high|medium|low",
      "issues_preventing_higher_score": "required when score >85.0",
      "sub_axes": {"abstraction_leverage": 0-100, "indirection_cost": 0-100, "interface_honesty": 0-100, "delegation_density": 0-100, "definition_directness": 0-100, "type_discipline": 0-100}  // required for abstraction_fitness when evidence supports it; all one decimal place
    }
  },
  "dimension_judgment": {
    "<dimension>": {
      "dimension_character": "2-3 sentences characterizing the overall nature of this dimension, synthesizing both positive characteristics and defects",
      "score_rationale": "2-3 sentences explaining the score, referencing global anchors"
    }  // required for every assessed dimension; do not omit
  },
  "issues": [{
    "dimension": "<dimension>",
    "identifier": "short_id",
    "summary": "one-line defect summary",
    "related_files": ["relative/path.py"],
    "evidence": ["specific code observation"],
    "suggestion": "concrete fix recommendation",
    "confidence": "high|medium|low",
    "impact_scope": "local|module|subsystem|codebase",
    "fix_scope": "single_edit|multi_file_refactor|architectural_change",
    "root_cause_cluster": "optional_cluster_name_when_supported_by_history",
    "concern_verdict": "confirmed|dismissed  // for concern signals only",
    "concern_fingerprint": "abc123  // required when dismissed; copy from signal fingerprint",
    "reasoning": "why dismissed  // optional, for dismissed only"
  }],
  "retrospective": {
    "root_causes": ["optional: concise root-cause hypotheses"],
    "likely_symptoms": ["optional: identifiers that look symptom-level"],
    "possible_false_positives": ["optional: prior concept keys likely mis-scoped"]
  },
  "context_updates": {
    "<dimension>": {
      "add": [{"header": "short label", "description": "why this is the way it is", "settled": true|false, "positive": true|false}],
      "remove": ["header of insight to remove"],
      "settle": ["header of insight to mark as settled"],
      "unsettle": ["header of insight to unsettle"]
    }  // omit context_updates entirely if no changes
  }
}

// context_updates example:
{
  "naming_quality": {
    "add": [
      {
        "header": "Short utility names in base/file_paths.py",
        "description": "rel(), loc() are deliberately terse \u2014 high-frequency helpers where brevity aids readability at call sites. Full names would add noise without improving clarity.",
        "settled": true,
        "positive": true
      }
    ],
    "settle": [
      "Snake case convention"
    ]
  }
}
