# Before Writing

Fix these before drafting a single paragraph. Ambiguity here propagates into
every section.

| Item | Definition |
|---|---|
| Venue & track | Determines page limit, template, review criteria, expected rigour |
| Claim | One sentence: *"We show that X enables Y under conditions Z."* |
| Contributions | 3–4 items, each independently defensible |
| Evaluation plan | For each contribution, the evidence that supports it |
| Figure plan | 3–6 figures decided up front; the paper is written around them |

**Recommended drafting order** (not the reading order):
Architecture → Evaluation → Related Work → Introduction → Conclusion → Abstract → Title.
The introduction is written last because it must promise exactly what the body delivers.

**Claim–evidence traceability.** Maintain a private table mapping each claim in
the introduction to the section, figure, or table that substantiates it. Any
claim without a row is either removed or demoted to future work.

---

# Title and Abstract

**Title.** Descriptive over clever. It should encode the artifact class and the
capability, not a slogan.

**Abstract (150–250 words), six sentences:**

1. Context — the domain and why it matters.
2. Problem — what breaks in current practice.
3. Gap — what existing approaches do not address.
4. Approach — what was built, in one sentence, at system level.
5. Evaluation — how it was assessed (setting, baselines, scale).
6. Result — the headline quantitative or qualitative outcome.

Failure modes: no numbers; promises the body does not keep; describes the
domain for four sentences and the contribution for one.

---

# 1. Introduction

**Goal.** Establish the problem, show that current practice is fragmented or
insufficient, isolate the research gap, present the contribution at a high
level, and hand the reader a map. Target 1 to 1.25 pages, five paragraphs.
A reader who stops after this section must be able to state the contribution.

## Paragraph A: Landscape and problem statement

Describe the operational reality of the domain and the problem as practitioners
experience it, independent of any solution. Ground the claim in evidence:
published studies, standards, reported incidents, or measured practice — not
assertion. End on the concrete cost of the problem (effort, latency, coverage,
error rate).

*Avoid:* textbook definitions of well-known concepts; opening with a
dictionary-style sentence; naming any solution.

## Paragraph B: Why the required capabilities are jointly necessary

Decompose the problem into the capabilities any adequate solution must provide.
For each, state why it is necessary and why removing it leaves the problem
unsolved. This paragraph earns the right to a multi-component system later: it
establishes that scope is a requirement, not feature accumulation.

*Avoid:* listing features; describing capabilities in terms of a particular
implementation; asserting necessity without a consequence for its absence.

## Paragraph C: Integration and implementation gap

Concede what existing work does well, then show where it stops. Distinguish
three failure classes and name which apply:

- **Coverage** — a required capability is absent.
- **Integration** — capabilities exist but in disjoint systems, with manual
  glue, incompatible formats, or no shared data model.
- **Operationalisation** — capabilities exist as research prototypes but do not
  survive realistic scale, deployment, or automation constraints.

The gap statement is the pivot of the paper. Phrase it as an unmet requirement,
not as a deficiency of named competitors.

*Avoid:* dismissing prior work; claiming novelty by omission ("to the best of
our knowledge, no work exists") without having demonstrated a search.

## Paragraph D: Contribution and novelty

State what was built, at what level of abstraction, and what is new. Novelty is
one of: a new mechanism, a new composition of known mechanisms that removes
manual steps, a new dataset or schema, or evidence that changes what the
community believes. Say explicitly which kind applies.

Close with an enumerated contribution list:

```
Concretely, this paper contributes:
  (i)   a <design/architecture> that <resolves which part of the gap>;
  (ii)  an implementation providing <capability>, supporting <interfaces>;
  (iii) a <dataset/schema/model> enabling <what it enables>;
  (iv)  an evaluation on <setting/scale> showing <measured outcome>.
```

Each item must be traceable to a later section. Nothing appears here that the
body does not deliver.

## Paragraph E: Paper Organisation

Two to four sentences mapping sections to content. Informative, not mechanical:
say what each section establishes, not merely that it exists.

---

# 2. Related Work

**Goal.** Demonstrate command of the field and convert the gap from Paragraph C
into a positioned, defensible claim.

**Organisation.** Thematic clusters, one per capability or approach family,
matching the decomposition of Paragraph B. Never chronological, never
one-paragraph-per-paper.

**Per cluster:**

1. Characterise the approach family and its shared assumptions.
2. Cite representative and recent work (reviewers check whether the last two to
   three years are present).
3. Close with an explicit **delta sentence**: what this family cannot do that
   the present work does, and why that limitation is structural rather than
   incidental.

**Comparison table.** For tool papers, a table with approaches as rows and the
Paragraph B capabilities as columns is the highest-value object in the section.
Criteria must be objective and verifiable from the cited sources; the final row
is the present work. If every column is a checkmark only for your row, the
criteria are probably reverse-engineered — reviewers notice.

*Avoid:* an annotated bibliography; strawmen; comparing against abandoned
baselines; a section that could be deleted without weakening the paper.

---

# 3. Architecture and Workflow

**Goal.** Let a competent reader understand the design well enough to reason
about, critique, and conceptually reimplement it.

**Suggested order:**

1. **Requirements** — restate the Paragraph B capabilities as design
   requirements, labelled (R1…Rn) for later reference.
2. **Design overview** — one architectural figure and the paragraph that walks
   it. Reader must reach a mental model here; the rest is refinement.
3. **Components** — one subsection each: responsibility, inputs, outputs,
   internal approach, and the requirement it satisfies.
4. **Data model** — the representation shared across components. In integrated
   systems this is often the real contribution; give it space.
5. **Workflow** — the end-to-end path of a unit of work through the system,
   including control flow, concurrency, and failure handling.
6. **Implementation notes** — languages, frameworks, interfaces, deployment
   form, scale limits. Brief; enough for credibility and reproduction.

**Level of abstraction.** Describe decisions and their rationale, not code.
Every non-obvious choice needs a *because*: the alternative considered and the
reason it was rejected. Rationale is what distinguishes a paper from
documentation.

**Running example.** A single realistic scenario threaded through the section
does more for comprehension than any amount of prose.

*Avoid:* a component-by-component tour with no integrating narrative;
reproducing configuration files or API listings; explaining standard technology
as if novel.

---

# 4. Experimental Results

**Goal.** Provide evidence for each contribution claimed in Paragraph D. The
evaluation is judged on whether it *could have falsified* the claims.

**Structure:**

1. **Research questions** — two to four, each mapped to a contribution and each
   answerable by a specific experiment. State them explicitly (RQ1…RQn) and
   answer them explicitly later.
2. **Setup** — environment, hardware, versions, parameters, data. Sufficient
   for independent repetition.
3. **Datasets / subjects** — provenance, size, selection criteria, and why they
   are representative. Justify exclusions.
4. **Baselines** — the strongest available comparators, configured fairly.
   If no baseline exists, justify that and substitute ablations.
5. **Metrics** — defined before results are shown, with the reason each metric
   answers its RQ.
6. **Results** — figures and tables first, prose interpreting them second.
   Never make the reader infer the conclusion from a table.
7. **Ablations** — remove each major component and measure the loss. This is
   what substantiates the "all capabilities are necessary" argument of
   Paragraph B.
8. **Discussion** — what the results mean, where the approach underperforms,
   and under what conditions it does not apply.
9. **Threats to validity** — internal, external, and construct. A candid,
   specific list increases credibility; a generic one wastes space.
10. **Reproducibility** — artifact availability, licence, and what is withheld
    and why.

*Avoid:* reporting only favourable configurations; single-run measurements of
variable quantities; conflating "our system is fast" with "our system is
correct"; tables without units, baselines, or variance; results that answer no
stated RQ.

---

# 5. Conclusion and Future Work

Half a page. Restate the problem in one sentence, the approach in one, and the
principal evidence in one — with the number. Then state what remains: known
limitations promoted into concrete next steps, not vague ambition. Introduce no
new claims and no new citations.

---

# References

Consistent style, complete metadata, DOIs where available. Prefer peer-reviewed
and primary sources; cite standards and specifications rather than blog
summaries of them. Verify every citation says what it is cited for.

---

# General Rules

- **One idea per paragraph**, stated in the first sentence.
- **Terminology is fixed on first use** and never varied for stylistic
  relief — synonym drift is a common source of reviewer confusion.
- **Figures and tables are self-contained**: readable from caption alone, with
  units, axes, and legends. Every one is referenced from the text.
- **Forward references** only for orientation, never to defer an explanation
  the reader needs immediately.
- **Numbers over adjectives**: "reduces manual steps from 12 to 2", not
  "greatly reduces manual effort".
- **Hedge accurately**: claim what was measured, in the conditions measured.
- **Passive/active voice** consistent with venue convention; prefer active.

---

# Pre-Submission Checklist

- [ ] Abstract and introduction promise exactly what the body delivers
- [ ] Each contribution maps to a section and to evidence
- [ ] Each RQ is stated, addressed, and explicitly answered
- [ ] Each requirement (R1…Rn) is traceable to a component and an experiment
- [ ] Related work includes the last two to three years
- [ ] Every figure and table is referenced and interpreted in the text
- [ ] Ablations justify every major component
- [ ] Threats to validity are specific, not generic
- [ ] Limitations stated in the paper, not only conceded in rebuttal
- [ ] Page limit, template, anonymisation, and formatting comply with the call
- [ ] References complete, consistent, and verified
- [ ] Read once end-to-end for terminology drift and unsupported claims
