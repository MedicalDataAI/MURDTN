# MURDTN
Multi US modality radiomics for diagnosing TNs

If you use this code in your research, consider citing:
```
@article{
  title={A comparative study of two radiomics-based blood flow models with Thyroid Imaging Reporting and Data System in predicting malignancy of thyroid nodules and reducing unnecessary fine-needle aspiration rate},
  author={xxxx},
  journal={xxxx},
  year={xxxx},
  publisher={xxxx}
}
```

## Prerequisites

- Python 3.7.11 with dependencies listed in the `requirements.txt` file
```
   pip install -r requirements.txt
```
- R 3.6.1 with packages list below
```
   install.packages("renv")
   library("renv")
   renv::init()
   renv::restore(lockfile="./renv.lock")
```

## Running

1. Train Radiomics model, save the result in "./radiomics model/[BMUS\BMUS_CEUS\BMUS_SMI\ALL]/result"
```
   RadiomicsModel.Rmd
```

2. Train Clinical-Radiomics model, save the result in "./combind model/result"
```
   ClinicalAndRadiomicsModel.Rmd
```