# Demo Voiceover

## Opening
This project is a reproducible hemodialysis toxin estimation baseline built from the provided clinical Excel dataset. It combines optoelectronic absorbance signals, dialysis machine parameters, and patient features in an end-to-end AI-assisted workflow.

## Dataset verification
I started by inspecting the workbook structure directly rather than assuming the schema from the paper. That step verified the actual target columns, machine parameters, and the fact that the dataset contains five absorbance wavelengths instead of only three.

## Modeling strategy
I compared three feature settings: all absorbance only, absorbance plus machine parameters, and absorbance plus machine plus personal features. I also compared multiple regressors including SVR, linear regression, random forest, and KNN under five-fold cross-validation.

## Feature selection
To make the analysis more interpretable, I used mutual information regression and permutation importance. This revealed that wavelengths such as 285nm and 310nm, along with treatment context features like ultrafiltration-related variables, are often important for prediction.

## Results
The strongest models were not identical across all toxins. SVR remained best for several targets such as urea and creatinine, while KNN performed better for potassium and beta-2 microglobulin. This means the best algorithm depends on the toxin being predicted.

## Visual outputs
The project generates feature-importance plots, model-comparison plots, correlation heatmaps, and predicted-versus-actual figures. It also saves the final models to support reproducible inference.

## Final insight
One of the key contributions of this project is methodological clarity. It separates rigorous validation from demo-style inference and explicitly discusses where paper-style visualizations can become misleading if validation logic is not handled carefully.

## Closing
Overall, this submission demonstrates not only a baseline modeling result, but also a practical and honest end-to-end AI-agent-assisted workflow for clinical tabular regression.
