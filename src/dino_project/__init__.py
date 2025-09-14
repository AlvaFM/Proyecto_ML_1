from dino_project.pipelines.data_engineering import create_pipeline

def register_pipelines():
    return {
        "data_engineering": create_pipeline(),
        "__default__": create_pipeline(),
    }
