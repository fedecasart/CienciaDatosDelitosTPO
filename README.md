# CienciaDatosDelitosTPO

Professional scaffold for a university **Data Mining** project focused on crime datasets.

## Recommended project structure

```text
CienciaDatosDelitosTPO/
├── data/
│   ├── raw/                 # Original datasets (never manually edited)
│   ├── processed/           # Cleaned/transformed datasets ready for analysis
│   └── external/            # Third-party reference data
├── notebooks/
│   ├── 01_data_cleaning/    # Data quality checks and cleaning exploration
│   ├── 02_exploratory_analysis/ # Exploratory Data Analysis notebooks
│   └── 03_visualizations/   # Plot-focused notebooks for storytelling
├── src/
│   ├── data_cleaning/       # Reusable cleaning/preprocessing code (future)
│   ├── eda/                 # Reusable EDA utilities (future)
│   └── visualization/       # Reusable plotting helpers (future)
├── docs/
│   ├── project_plan/README.md    # Scope, research questions, timeline
│   ├── data_dictionary/README.md # Variable definitions and metadata
│   └── methodology/README.md     # Analytical decisions and method notes
├── reports/
│   ├── figures/             # Figures exported for reports
│   ├── tables/              # Final tables for reports
│   └── README.md            # Reporting usage notes
└── presentation/
    └── README.md            # Slides and presentation assets
```

> `.gitkeep` placeholders are included to preserve empty directories until content is added.

## Brief recommended workflow

1. **Data acquisition**: place original files in `data/raw/`.
2. **Documentation first**: register column meanings and assumptions in `docs/data_dictionary/`.
3. **Cleaning stage**: prototype cleaning in `notebooks/01_data_cleaning/`; later move reusable logic to `src/data_cleaning/` and save outputs in `data/processed/`.
4. **Exploration stage**: perform EDA in `notebooks/02_exploratory_analysis/` and keep reusable helpers in `src/eda/`.
5. **Visualization stage**: create publication-ready charts in `notebooks/03_visualizations/` and export results to `reports/figures/` and `reports/tables/`.
6. **Communication**: produce final narrative in `reports/` and slides in `presentation/`.

This layout is intentionally lightweight now and scalable as datasets and analyses are added.
