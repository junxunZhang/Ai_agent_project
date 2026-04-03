# Final Comparison Report

## Executive Summary

This project reproduced and extended the hemodialysis toxin-prediction idea described in `OptoEML_SNB_Final .docx`, but with a more explicit emphasis on reproducible Python pipelines, multiple model comparison, feature-selection outputs, and artifact traceability. After comparing the paper methodology with the implementation developed in this repository, the biggest conclusion is:

> The paper presents a strong clinical proof-of-concept centered on SVR with absorbance + personalized features, but its reporting style leaves several validation and deployment ambiguities that can easily create optimistic or misleading interpretations if not handled carefully.

This repository surfaced those issues directly during implementation. In particular, several problems become important when transitioning from a research-style demonstration to a reproducible interview-homework or deployment-style analysis pipeline.

---

## 1. What the paper does

Based on `OptoEML_SNB_Final .docx`, the paper's core methodology is:

1. Build a multi-wavelength optoelectronic system for spent dialysate monitoring.
2. Use three absorbance wavelengths:
   - 255nm
   - 275nm
   - 310nm
3. Add selected personalized / machine features.
4. Use SVR as the primary prediction model.
5. Evaluate by five-fold cross-validation.
6. Convert spent-dialysate predictions to blood concentration by linear regression.
7. Present:
   - predicted-vs-actual concentration curves in a final clinical experiment
   - predicted-vs-actual blood concentration relationships

The paper reports strong R² values, especially for urea, creatinine, and uric acid.

---

## 2. What this project does differently

This repository intentionally goes beyond the paper in several ways.

### 2.1 Dataset-driven schema verification

Instead of assuming the schema from the paper, the implementation first inspected the real Excel workbook and verified:

- sheet names
- target columns
- feature columns
- missing values
- session structure
- machine parameters
- personalized features

This revealed that the real workbook contains **five absorbance wavelengths**:

- 255nm
- 275nm
- 285nm
- 295nm
- 310nm

The paper focuses on three wavelengths, but the provided dataset exposes two additional wavelengths that should not be ignored in a practical baseline analysis.

### 2.2 Expanded feature sets

Instead of only comparing absorbance-only vs absorbance + personalized, this project evaluated:

- **Feature Set A**: all five absorbance features only
- **Feature Set B**: all five absorbance + all available dialysis machine parameters
- **Feature Set C**: all five absorbance + all machine parameters + personalized features

### 2.3 Multi-model benchmarking

The paper centers on SVR. This project kept SVR as the main baseline, but also compared:

- Linear Regression
- Random Forest Regressor
- KNN Regressor

This matters because the best model is not identical across all toxins. In this implementation:

- SVR remains strongest for urea, creatinine, phosphorus, and inferred uric acid
- KNN performs better for potassium and β2-microglobulin

### 2.4 Explicit feature selection outputs

The paper describes ANOVA F-test + wrapper-style selection. This project used:

- mutual information regression
- permutation importance

and generated explicit artifacts for:

- selected feature tables
- feature importance plots
- full vs selected performance comparison tables

### 2.5 Model persistence and inference artifacts

The paper presents prediction curves, but does not describe a concrete deployable artifact flow.

This project adds:

- saved final model files (`.joblib`)
- metadata manifests for each toxin
- inference-oriented pipeline outputs

This is more aligned with practical deployment and demo reproducibility.

---

## 3. Biggest methodological differences

### 3.1 Three wavelengths vs five wavelengths

**Paper:** restricts the core system and modeling story to 255nm, 275nm, and 310nm.

**This project:** uses all five available wavelengths because the real workbook includes 285nm and 295nm, and excluding them without analysis would be arbitrary.

**Why this matters:**
- The paper's wavelength choice is driven by hardware and UV absorption reasoning.
- The dataset, however, already contains richer measurements.
- In the current implementation, 285nm and 310nm repeatedly appear as highly informative features.

### 3.2 Single-model emphasis vs evidence-driven model choice

**Paper:** emphasizes SVR as the main model.

**This project:** evaluates multiple models and lets the data decide.

**Why this matters:**
- A single model can be a clean research story.
- But for actual predictive deployment, forcing one algorithm for all toxins may be suboptimal.

### 3.3 Research demonstration vs deployment-style workflow

**Paper:** shows convincing figures, but does not fully describe how a final model would be saved, loaded, and used for single-session inference.

**This project:** explicitly implements:
- saved final models
- metadata files
- inference from saved artifacts

This exposes practical problems that are easy to hide in a paper-style narrative.

---

## 4. What problems can happen in the paper's approach

This section highlights the main risks or weaknesses in the paper-style methodology, especially from a reproducibility and ML-evaluation standpoint.

### 4.1 Potential confusion between evaluation R² and plotting R²

A major issue surfaced during this project:

- the **model R²** from cross-validation
- and the **R² of a fitted line on a predicted-vs-actual scatter plot**

are not the same thing.

If a paper-style figure shows predicted vs actual points with a regression line and quotes R², readers may mistakenly assume that this is the same as the formal model validation R².

**Problem:**
This can make the visual story look cleaner than the actual evaluation logic.

**What can happen:**
- reviewers may overinterpret the scatter-plot R²
- inconsistency can appear between figures and validation tables
- the presentation may become misleading even if not intentionally so

### 4.2 Risk of data leakage or optimistic demonstration in session-level prediction curves

The paper shows a final clinical experiment with predicted-vs-actual concentration curves. That is visually persuasive. However, from an ML validation perspective, a crucial question is:

> Was that session truly unseen by the final model?

If a final fitted model is used to predict a session that was also part of model fitting, then the resulting session curve becomes a **train-on-train demonstration**, not a strict validation figure.

**Problem:**
This does not necessarily mean feature leakage in the narrow sense, but it introduces **optimistic bias**.

**What can happen:**
- the curve looks better than real-world generalization
- readers may interpret it as independent validation
- the figure becomes stronger as a demo than as evidence

This exact issue surfaced in this project and had to be explicitly separated into:
- validation-style figures
- deployment/demo-style figures

### 4.3 Session-based data are not independent observations

The dataset consists of repeated measurements within HD sessions across time.

**Paper:** uses five-fold cross-validation, but does not appear to frame the problem as a grouped/session-aware time-series-like structure.

**Problem:**
If folds are split at row level, correlated measurements from the same patient/session can leak across train and validation folds.

**What can happen:**
- inflated performance estimates
- overly optimistic R²
- weaker generalization to truly unseen sessions or patients

This is one of the most important methodological cautions.

### 4.4 Manual exclusion / anomaly removal can be hard to reproduce

The paper states that invalid values and anomalies were removed, including abrupt fluctuations due to drug administration.

**Problem:**
If exclusion rules are not fully formalized, then:
- another team cannot exactly reproduce the dataset
- performance may depend heavily on subjective data cleaning
- a final “cleaned” dataset may look stronger than the raw operational reality

**What can happen:**
- hidden selection bias
- unclear reproducibility
- difficulty comparing future studies fairly

### 4.5 Blood-concentration conversion by linear regression may amplify uncertainty

The paper converts spent-dialysate predictions into blood concentration by linear regression.

**Problem:**
This is effectively a second modeling layer:
1. predict toxin in spent dialysate
2. convert prediction to blood concentration

Each step adds uncertainty.

**What can happen:**
- error propagation
- overly strong interpretation of blood-equivalent estimates
- confusion between direct biochemical measurement and model-derived conversion

### 4.6 Limited sample size and patient heterogeneity

The paper itself acknowledges small sample size.

**Problem:**
With only a limited number of patients/sessions, model selection and feature selection can become unstable.

**What can happen:**
- performance metrics may vary sharply if a few sessions are removed
- apparent “best features” may not generalize
- different toxins may favor different models purely due to sample limitations

---

## 5. What this project uncovered during implementation

Several important issues only became obvious when building a reproducible pipeline.

### 5.1 The session-curve figure can become wrong if model/feature configuration is not preserved exactly

When comparing:
- full features
- selected features
- multiple models

it is easy to accidentally generate a “best model” curve using the wrong feature configuration.

This happened during development and produced obviously unrealistic predictions for several toxins.

**Lesson:**
A convincing figure is not enough. The exact saved model and exact feature list must be preserved and reused during inference.

### 5.2 Final models should be persisted explicitly

For practical inference, the final model per toxin should be:
- trained
- saved
- documented with feature list and metrics
- reloaded for prediction

This project now does that via:
- `outputs/models/*.joblib`
- `outputs/models/*_metadata.json`
- `outputs/models/model_manifest.csv`

### 5.3 Feature selection improves interpretability more than performance

In this expanded implementation, feature selection helped identify useful predictors, but it did **not consistently improve predictive performance** over the full feature models.

This is an important contrast with the paper's clean “selected features improve the model” storyline.

---

## 6. Summary of the biggest difference

If one sentence must capture the biggest difference between the paper and this project, it is this:

> The paper presents a strong proof-of-concept using a clean SVR-centered story, while this project stress-tests that idea under reproducible, artifact-driven, deployment-aware analysis — revealing that model choice varies by toxin, five wavelengths matter, and validation/demo figures must be separated carefully to avoid optimistic interpretation.

---

## 7. Practical final conclusion

### What the paper does well

- strong clinical motivation
- meaningful hardware + ML integration
- clear demonstration that absorbance is essential
- persuasive evidence that personalized/context features help

### What can go wrong in the paper-style approach

- confusion between visual-fit R² and validation R²
- session-level demonstration that may not be fully independent
- row-level CV on repeated session data may be optimistic
- manual exclusion rules may be hard to reproduce
- converted blood predictions may hide compounded uncertainty
- final inference workflow is not fully operationalized

### What this project adds

- real-schema verification from the workbook
- full five-wavelength analysis
- multi-model comparison
- systematic feature-selection outputs
- saved model artifacts
- explicit separation between validation logic and application-style inference

---

## 8. Recommended message for interview presentation

A concise and honest presentation message would be:

> We reproduced the study idea and extended it into a reproducible end-to-end ML workflow. Our analysis confirms the importance of absorbance features and contextual dialysis features, but also shows that the best algorithm can vary by toxin. More importantly, when turning a research figure into a deployable workflow, we must distinguish between cross-validated evidence and final-model demo inference to avoid optimistic or misleading interpretation.
