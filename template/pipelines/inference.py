# {% include 'template/license_header' %}

from steps import (
    data_loader,
{%- if data_quality_checks %}
    drift_quality_gate,
{%- endif %}
    inference_data_preprocessor,
    inference_predict,
    notify_on_failure,
    notify_on_success,
)
from zenml import pipeline, get_pipeline_context
from zenml.integrations.evidently.metrics import EvidentlyMetricConfig
from zenml.integrations.evidently.steps import evidently_report_step
from zenml.logger import get_logger

from constants import DATA_CLASSIFICATION

logger = get_logger(__name__)


@pipeline(on_failure=notify_on_failure, tags=[DATA_CLASSIFICATION])
def {{product_name}}_inference():
    """
    Model batch inference pipeline.

    This is a pipeline that loads the inference data, processes
    it, analyze for data drift and run inference.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Link all the steps together by calling them and passing the output
    # of one step as the input of the next step.
    model = get_pipeline_context().model
    ########## ETL stage  ##########
    df_inference, target, _ = data_loader(
        random_state=model.get_artifact("random_state"),
        is_inference=True
    )
    df_inference = inference_data_preprocessor(
        dataset_inf=df_inference,
        preprocess_pipeline=model.get_artifact("preprocess_pipeline"),
        target=target,
    )

{%- if data_quality_checks %}
    ########## DataQuality stage  ##########
    report, _ = evidently_report_step(
        reference_dataset=model.get_artifact("dataset_trn"),
        comparison_dataset=df_inference,
        ignored_cols=["target"],
        metrics=[
            EvidentlyMetricConfig.metric("DataQualityPreset"),
        ],
    )
    drift_quality_gate(report)
{%- endif %}
    ########## Inference stage  ##########
    inference_predict(
        dataset_inf=df_inference,
{%- if data_quality_checks %}
        after=["drift_quality_gate"],
{%- endif %}
    )

    notify_on_success(after=["inference_predict"])
    ### YOUR CODE ENDS HERE ###
