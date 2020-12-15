''' FRAMEWORK CODE - This entire file as provided. Modify only if you need to change workflow or add/remove tasks.
All methods in this file are luigi Tasks. The flow is called from __main__.py.
'''

import luigi
from luigi import ExternalTask, Task, LocalTarget

import numpy as np

import pickle

# Change these utils if removed out of the project and into its own repo
from csci_utils.utils.luigi.task import Requirement, Requires, TargetOutput
from csci_utils.utils.luigi.dask.target import CSVTarget, ParquetTarget

from ..preprocess.getsource import getsourceurl
from ..preprocess.cleandata import clean_datasets
from ..preprocess.extractfeatures import extract_features_from_dask_dataframe
from ..preprocess.transformdata import transform_dataframe
from ..model.trainmodel import train_model
from ..visualize.visualizefeaturesignificance import visualizefeaturesignificance
from ..model.evaluatemodel import evaluate_model
from ..visualize.visualizepredictions import visualizepredictions


# VERSION = os.getenv('PIPELINE_VERSION', '0.1')
#

# class Debug(luigi.Task):
#     """Use this task with appropriate image to debug things."""
#
#     @property
#     def image(self):
#         return f'code-challenge/download-data:{VERSION}'
#
#     @property
#     def command(self):
#         return [
#             'sleep', '3600'
#         ]


class DownloadData(ExternalTask):
    SOURCE_URL = getsourceurl()

    output = TargetOutput(
        file_pattern=SOURCE_URL,
        flag="",
        target_class=CSVTarget,
        storage_options=dict(requester_pays=True),
        glob="*.csv",
    )


class CleanData(Task):
    dir_path = luigi.Parameter(default="data")

    requires = Requires()
    source_data = Requirement(DownloadData)

    output = TargetOutput(
        file_pattern="{task.dir_path}/{task.__class__.__name__}/",
        target_class=ParquetTarget,
        glob="*.parquet",
    )

    def run(self):
        ddf = self.input()["source_data"].read_dask()

        ddf = clean_datasets(ddf)

        self.output().write_dask(ddf, compression='gzip')


class ExtractFeatures(Task):
    dir_path = luigi.Parameter(default="data")

    requires = Requires()
    source_data = Requirement(CleanData)

    output = TargetOutput(
        file_pattern="{task.dir_path}/{task.__class__.__name__}/",
        target_class=ParquetTarget,
        glob="*.parquet",
    )

    def run(self):
        ddf = self.input()["source_data"].read_dask()

        ddf = extract_features_from_dask_dataframe(ddf)

        self.output().write_dask(ddf, compression='gzip')


class TransformData(Task):
    dir_path = luigi.Parameter(default="data")

    requires = Requires()
    source_data = Requirement(ExtractFeatures)

    output = TargetOutput(
        file_pattern="{task.dir_path}/{task.__class__.__name__}/",
        target_class=ParquetTarget,
        glob="*.parquet",
    )

    def run(self):
        ddf = self.input()["source_data"].read_dask()

        ddf = transform_dataframe(ddf)

        self.output().write_dask(ddf, compression='gzip')


class MakeDatasets(Task):
    TEST_AS_PERCENT_OF_DATASET = 0.20

    dir_path = luigi.Parameter(default="data")

    requires = Requires()

    output = TargetOutput(
        file_pattern="{task.dir_path}/{task.__class__.__name__}/",
        target_class=ParquetTarget,
        glob="*.parquet",
    )
        

class MakeTrainingSet(MakeDatasets):
    source_data = Requirement(TransformData)

    def run(self):
        ddf = self.input()["source_data"].read_dask()

        train, _ = ddf.random_split([
            1 - self.TEST_AS_PERCENT_OF_DATASET,
            self.TEST_AS_PERCENT_OF_DATASET],
            random_state=123
            )

        self.output().write_dask(train, compression='gzip')

 
class MakeTestSet(MakeDatasets):
    source_data = Requirement(TransformData)
        
    def run(self):
        ddf = self.input()["source_data"].read_dask()

        _, test = ddf.random_split([
            1 - self.TEST_AS_PERCENT_OF_DATASET,
            self.TEST_AS_PERCENT_OF_DATASET],
            random_state=123
            )

        self.output().write_dask(test, compression='gzip')


class TrainModel(Task):
    dir_path = luigi.Parameter(default="data")
    model_path = luigi.Parameter(default="data/Model/model.pckl")

    requires = Requires()
    source_data = Requirement(MakeTrainingSet)

    def output(self):
        return LocalTarget(self.model_path)

    def run(self):
        train_ddf = self.input()["source_data"].read_dask()

        model = train_model(train_ddf)

        self.output().makedirs()

        with self.output().temporary_path() as temp_output_path:
            print(temp_output_path)
            pickle.dump(model, open(temp_output_path, 'wb'))


class VisualizeFeatureImportance(Task):
    dir_path = luigi.Parameter(default="data")
    importance_path = luigi.Parameter(default="data/VisualizeFeatureSignificance/featureimportance.png")

    requires = Requires()
    source_data_testset = Requirement(MakeTestSet)
    source_model = Requirement(TrainModel)

    def output(self):
        return LocalTarget(self.importance_path)

    def run(self):
        test_ddf = self.input()["source_data_testset"].read_dask()

        with open(self.input()["source_model"].fn, "rb") as file:
            model = pickle.load(file)

        fig = visualizefeaturesignificance(model, test_ddf)

        self.output().makedirs()

        # https://mattiacinelli.com/tutorial-on-luigi-part-3-pipeline-input-and-output/
        fig.savefig(self.output().path)
                       


class EvaluateModel(Task):
    dir_path = luigi.Parameter(default="data")
    predicted_values_path = luigi.Parameter(default="data/EvaluateModel/predicted.npy")

    requires = Requires()
    source_data_testset = Requirement(MakeTestSet)
    source_model = Requirement(TrainModel)

    def output(self):
        return LocalTarget(self.predicted_values_path)

    def run(self):
        test_ddf = self.input()["source_data_testset"].read_dask()

        with open(self.input()["source_model"].fn, "rb") as file:
            model = pickle.load(file)

        y_predicted = evaluate_model(model, test_ddf)

        self.output().makedirs()

        np.save(self.output().path, y_predicted) 


class VisualizePredictions(Task):
    dir_path = luigi.Parameter(default="data")
    prediction_visualization_path = luigi.Parameter(default="data/VisualizePredictions/predictions.png")

    requires = Requires()
    source_data_testset = Requirement(MakeTestSet)
    source_predictions = Requirement(EvaluateModel)

    def output(self):
        return LocalTarget(self.prediction_visualization_path)

    def run(self):
        test_ddf = self.input()["source_data_testset"].read_dask()

        y_predicted = np.load(self.input()["source_predictions"].path, allow_pickle=True)

        fig = visualizepredictions(y_predicted, test_ddf)

        self.output().makedirs()

        # https://mattiacinelli.com/tutorial-on-luigi-part-3-pipeline-input-and-output/
        fig.savefig(self.output().path)





