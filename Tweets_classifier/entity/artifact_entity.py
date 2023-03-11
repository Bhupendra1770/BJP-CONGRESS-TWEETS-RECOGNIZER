from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str


@dataclass
class DataValidationArtifact:
    pass

@dataclass
class DataTransformationArtifact:
    transform_object_path:str
    transformed_feature_path:str
    transformed_target_path:str


@dataclass
class ModelTrainerArtifact:
    model_path:str 


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_accuracy:float

@dataclass
class ModelPusherArtifact:
    pusher_model_dir:str 
    saved_model_dir:str


