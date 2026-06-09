# CienciaDatosDelitosTPO

Scaffold for a university Data Mining project focused on crime-related datasets.

## Project structure

```text
CienciaDatosDelitosTPO/
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── .gitkeep
│   ├── metadata/
│   │   └── data_dictionary_template.csv
│   └── README.md
├── notebooks/
│   ├── 01_data_cleaning/
│   │   └── .gitkeep
│   ├── 02_exploratory_analysis/
│   │   └── .gitkeep
│   ├── 03_visualizations/
│   │   └── .gitkeep
│   └── README.md
├── src/
│   ├── data_cleaning/
│   │   └── .gitkeep
│   ├── exploratory_analysis/
│   │   └── .gitkeep
│   ├── visualization/
│   │   └── .gitkeep
│   └── README.md
├── docs/
│   ├── references/
│   │   └── .gitkeep
│   └── README.md
├── reports/
│   ├── final_report/
│   │   └── .gitkeep
│   ├── presentation/
│   │   └── .gitkeep
│   └── README.md
└── .gitignore
```

## Folder and file purposes

- `data/raw/`: immutable source datasets as provided.
- `data/processed/`: curated datasets ready for analysis.
- `data/metadata/data_dictionary_template.csv`: placeholder for future variable definitions and schema notes.
- `notebooks/`: staged notebook workflow (cleaning → exploration → visualization).
- `src/`: reusable analysis utilities that can later replace repeated notebook code.
- `docs/`: project documentation and supporting references.
- `reports/final_report/`: final written academic submission.
- `reports/presentation/`: slide deck and presentation assets.
- `.gitignore`: excludes raw/processed data files and common local artifacts.

## Recommended workflow (brief)

1. Acquire datasets and store original files in `data/raw/`.
2. Document source and columns in `data/metadata/`.
3. Perform cleaning in `notebooks/01_data_cleaning/`; save outputs to `data/processed/`.
4. Conduct exploratory analysis in `notebooks/02_exploratory_analysis/`.
5. Build publication-ready figures in `notebooks/03_visualizations/`.
6. Move repeated logic into `src/` modules for maintainability.
7. Consolidate methodology/results in `reports/final_report/` and prepare slides in `reports/presentation/`.
