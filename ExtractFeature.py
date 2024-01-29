# Copyright 2017 Harvard Medical School
# https://github.com/AIM-Harvard/pyradiomics
from __future__ import print_function

import logging
import os
import pandas
import SimpleITK as sitk
import radiomics
from radiomics import featureextractor

def fn_extract_radiomics_feature(in_csv_fp_image_mask, out_dir, config_yaml):
    """
    Extract radiomics feature from image and mask file path in a csv file, and save the result into a csv file.
    :param in_csv_fp_image_mask: absolute file path, including image and mask file path.
    :param out_dir: result directory.
    :param config_yaml: pyradiomics config YAML file path.
    :return: None.
    """
    fp_radiomics_fature = os.path.join(out_dir, 'radiomics_features.csv')
    fp_log = os.path.join(out_dir, 'log_extract.txt')

    # Set logging
    rLogger = logging.getLogger('radiomics')
    handler = logging.FileHandler(filename=fp_log, mode='w')
    handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
    rLogger.addHandler(handler)
    logger = rLogger.getChild('batch')

    # Set pyradiomics
    radiomics.setVerbosity(logging.INFO)
    extractor = featureextractor.RadiomicsFeatureExtractor(config_yaml)
    logger.info('pyradiomics version: %s', radiomics.__version__)
    logger.info('Enabled input images types: %s', extractor.enabledImagetypes)
    logger.info('Enabled features: %s', extractor.enabledFeatures)
    logger.info('Current settings: %s', extractor.settings)

    # Read image and mask file path
    logger.info('Loading CSV')
    try:
        flists = pandas.read_csv(in_csv_fp_image_mask).T
    except Exception:
        logger.error('CSV READ FAILED', exc_info=True)
        exit(-1)
    logger.info('Loading Done')
    logger.info('Patients: %d', len(flists.columns))

    # Start Extract Feature
    results = pandas.DataFrame()

    for entry in flists:
        logger.info("(%d/%d) Processing Patient (Image: %s, Mask: %s)",
                    entry + 1,
                    len(flists),
                    flists[entry]['Image'],
                    flists[entry]['Mask'])

        imageFilepath = flists[entry]['Image']
        maskFilepath = flists[entry]['Mask']
        label = flists[entry].get('Label', None)

        if str(label).isdigit():
            label = int(label)
        else:
            label = None

        if (imageFilepath is not None) and (maskFilepath is not None):
            featureVector = flists[entry]  # This is a pandas Series
            featureVector['Image'] = os.path.basename(imageFilepath)
            featureVector['Mask'] = os.path.basename(maskFilepath)

            try:
                result = pandas.Series(extractor.execute(imageFilepath, maskFilepath, label=1))
                featureVector = featureVector.append(result)
            except Exception:
                logger.error('FEATURE EXTRACTION FAILED:', exc_info=True)
            featureVector.name = entry
            results = results.join(featureVector, how='outer')  # If feature extraction failed, results will be all NaN

    logger.info('Extraction complete, writing CSV')
    # .T transposes the data frame, so that each line will represent one patient, with the extracted features as columns
    results.T.to_csv(fp_radiomics_fature, index=False, na_rep='NaN')
    logger.info('CSV writing complete')

def main():
    root_dir = r"./"
    fn_extract_radiomics_feature(
        in_csv_fp_image_mask=os.path.join(root_dir, "dataset_filepath.csv"),
        out_dir=os.path.join(root_dir, "result"),
        config_yaml=os.path.join(root_dir, "config", "US_2D_extraction_v3.0.1.yaml"))


if __name__ == '__main__':
    main()
