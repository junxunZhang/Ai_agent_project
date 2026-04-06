# Detailed Speaker Notes

## Total slides
17

---

## Slide 1 — Title / Project Overview

### What to say
- This project started as an interview homework focused on hemodialysis toxin prediction from optoelectronic signals.
- It evolved into a full reproducible workflow with debugging, methodological correction, audit reports, and final protocol separation.
- The key theme is not only model performance, but also how to make evaluation trustworthy.

### Delivery tip
Keep this opening confident and concise. Tell the audience that the story includes both results and correction logic.

---

## Slide 2 — Clinical Background and Motivation

### What to say
- Hemodialysis removes toxins, but direct biochemical monitoring is not continuous.
- Optical sensing of spent dialysate offers a possible indirect monitoring route.
- Machine learning can map sensed patterns and clinical context to toxin estimates.

### Delivery tip
Do not overcomplicate the physiology. Focus on why prediction is useful operationally.

---

## Slide 3 — Problem Statement

### What to say
- The dataset supports a multi-target regression problem.
- The six targets include urea, creatinine, phosphorus, potassium, beta-2 microglobulin, and an `Acid` column that we treat cautiously as the workbook counterpart of uric acid.
- The challenge is not only prediction, but correct interpretation of repeated clinical-session data.

### Delivery tip
When mentioning `Acid`, explicitly say it is an inferred mapping.

---

## Slide 4 — Research Goal and Expected Outcome

### What to say
- I wanted a complete homework submission, not just a notebook.
- That means code, tests, figures, documentation, PPT materials, and a trustworthy evaluation story.
- OpenClaw was used to help drive the work from requirement parsing all the way to final deliverables.

### Delivery tip
This is where you connect the assignment requirements to the work produced.

---

## Slide 5 — Original Experiment Design from Prior Study

### What to say
- The prior study gives the conceptual starting point: optical sensing, three core wavelengths, SVR baseline, and five-fold CV.
- That paper is useful, but implementation against the real workbook reveals additional complexity.
- So this project is partly reproduction, partly stress test of the methodology.

### Delivery tip
Be respectful to the paper — you are extending and auditing, not dismissing it.

---

## Slide 6 — Dataset Verification and Real Workbook Schema

### What to say
- The first thing I did was inspect the actual workbook rather than hard-code the paper’s assumptions.
- That verified the real sheet structure, target columns, session structure, and feature groups.
- This step was critical because a wrong schema assumption would invalidate everything downstream.

### Delivery tip
Use this slide to signal disciplined data work.

---

## Slide 7 — Feature Design: Optical, Machine, and Personal Features

### What to say
- The workbook contains five optical wavelengths, not just three.
- It also includes machine variables and patient context that should be tested rather than ignored.
- So I defined three feature sets that progressively add more context.

### Delivery tip
Make clear that expanding the feature space was based on real data inspection, not feature creep.

---

## Slide 8 — Modeling Workflow and OpenClaw Collaboration Flow

### What to say
- OpenClaw helped across multiple stages: requirement analysis, code generation, testing, debugging, figure revision, and reporting.
- The process was iterative.
- Several corrections came from questioning seemingly reasonable outputs and then tightening the workflow.

### Delivery tip
This is the slide where you show the collaboration was substantive, not superficial.

---

## Slide 9 — Early Baseline Results and Why They Were Not Enough

### What to say
- The early pipeline looked promising: multiple models, feature-selection outputs, and attractive figures.
- But attractive figures are not enough if the evaluation design is not fully rigorous.
- This slide sets up why the debugging story matters.

### Delivery tip
Do not undersell the early work — describe it as useful, but incomplete.

---

## Slide 10 — Key Issue 1: Output Interpretation Problems in Early Figures

### What to say
- One issue was that some predicted-vs-actual figures mixed scatter-fit style logic with formal model metrics.
- That can confuse the audience because plot-level fit and CV-level evaluation are not the same thing.
- The correction was to redesign the figures so the interpretation is cleaner and less misleading.

### Delivery tip
This is a good example of why visualization choices are methodological, not just aesthetic.

---

## Slide 11 — Key Issue 2: Session-Level Leakage and Unsafe Evaluation Logic

### What to say
- Because rows within the same HD session are correlated, row-level evaluation can leak session structure.
- That means the model can appear stronger than it really is.
- The first major correction was to move to grouped session-level evaluation.

### Delivery tip
This is one of the most important scientific points. Slow down here.

---

## Slide 12 — Key Issue 3: Test-Set Model Selection Problem

### What to say
- Even after grouped unseen-session CV was added, there was still a deeper issue.
- If I use unseen-session results to choose the winning model, then that unseen set is no longer a pure final test set.
- That creates selection bias.
- So grouped unseen-session benchmarking was reclassified as exploratory only.

### Delivery tip
This slide shows mature scientific judgment. Emphasize that the correction was explicit, not hidden.

---

## Slide 13 — Corrected Final Evaluation Protocol

### What to say
- The final protocol uses a fixed session-level train / validation / test split.
- Model choice happens on validation only.
- Test is used once at the end for final evaluation.
- This is the protocol-compliant result set that should be trusted most.

### Delivery tip
Make sure the audience understands why this is different from grouped CV benchmarking.

---

## Slide 14 — Final Model Selection Results

### What to say
- This slide shows which model won for each toxin under validation-only model selection.
- This is where model comparison is allowed.
- The chosen models are then frozen before the test evaluation.

### Delivery tip
Separate selection and evaluation clearly in your wording.

---

## Slide 15 — Final Trustworthy Evaluation Figures

### What to say
- These are the final held-out test results.
- The figures on this slide are the main evidence to present when asked about final model performance.
- They are more trustworthy than earlier exploratory grouped-CV figures because test data no longer participates in model choice.

### Delivery tip
State explicitly: “These are the final held-out test artifacts.”

---

## Slide 16 — Discussion, Limitations, and What Changed vs the Paper

### What to say
- Compared with the paper, this project used a richer feature space, more explicit benchmarking, and stronger audit/report logic.
- It also showed that implementation can expose hidden evaluation issues that a polished paper narrative may not make obvious.
- The result is a more deployment-aware and methodologically honest workflow.

### Delivery tip
Frame this as learning and strengthening, not criticism for its own sake.

---

## Slide 17 — Reflection, Learnings, and Final Takeaway

### What to say
- The final lesson is that trustworthy ML requires both predictive modeling and disciplined evaluation design.
- OpenClaw added value not only by accelerating implementation, but by helping iterate through corrections and documentation.
- The final deliverable is stronger precisely because the mistakes were found, explained, and corrected.

### Delivery tip
End with confidence: the value of the project is the combination of technical result + methodological rigor.
