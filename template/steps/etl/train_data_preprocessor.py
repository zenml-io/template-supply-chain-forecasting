# {% include 'template/license_header' %}


from typing import List, Optional, Tuple
from typing_extensions import Annotated

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from constants import DATA_CLASSIFICATION
from utils.preprocess import ColumnsDropper, DataFrameCaster, NADropper
from zenml import step, ArtifactConfig


@step
def train_data_preprocessor(
    dataset_trn: pd.DataFrame,
    dataset_tst: pd.DataFrame,
    drop_na: Optional[bool] = None,
    normalize: Optional[bool] = None,
    drop_columns: Optional[List[str]] = None,
) -> Tuple[
    Annotated[pd.DataFrame, ArtifactConfig(name="dataset_trn", tags=[DATA_CLASSIFICATION])],
    Annotated[pd.DataFrame, ArtifactConfig(name="dataset_tst", tags=[DATA_CLASSIFICATION])],
    Annotated[Pipeline, ArtifactConfig(name="preprocess_pipeline", tags=[DATA_CLASSIFICATION])],
]:
    """Data preprocessor step.

    This is an example of a data processor step that prepares the data so that
    it is suitable for model training. It takes in a dataset as an input step
    artifact and performs any necessary preprocessing steps like cleaning,
    feature engineering, feature selection, etc. It then returns the processed
    dataset as an step output artifact.

    This step is parameterized, which allows you to configure the step
    independently of the step code, before running it in a pipeline.
    In this example, the step can be configured to drop NA values, drop some
    columns and normalize numerical columns. See the documentation for more
    information:

        https://docs.zenml.io/how-to/build-pipelines/use-pipeline-step-parameters

    Args:
        dataset_trn: The train dataset.
        dataset_tst: The test dataset.
        drop_na: If `True` all NA rows will be dropped.
        normalize: If `True` all numeric fields will be normalized.
        drop_columns: List of column names to drop.

    Returns:
        The processed datasets (dataset_trn, dataset_tst) and fitted `Pipeline` object.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    preprocess_pipeline = Pipeline([("passthrough", "passthrough")])
    if drop_na:
        preprocess_pipeline.steps.append(("drop_na", NADropper()))
    if drop_columns:
        # Drop columns
        preprocess_pipeline.steps.append(("drop_columns", ColumnsDropper(drop_columns)))
    if normalize:
        # Normalize the data
        preprocess_pipeline.steps.append(("normalize", MinMaxScaler()))
    preprocess_pipeline.steps.append(("cast", DataFrameCaster(dataset_trn.columns)))
    dataset_trn = preprocess_pipeline.fit_transform(dataset_trn)
    dataset_tst = preprocess_pipeline.transform(dataset_tst)
    ### YOUR CODE ENDS HERE ###

    return dataset_trn, dataset_tst, preprocess_pipeline
