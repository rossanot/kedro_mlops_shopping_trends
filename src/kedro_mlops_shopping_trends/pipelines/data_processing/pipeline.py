"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""

# from kedro.pipeline import Pipeline, pipeline, node
# import kedro.pipeline.modular_pipeline.pipeline as mpipeline
# from .nodes import (get_intermediate, split_data, get_model_input)
from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline
from .nodes import (get_intermediate,
                    get_primary,
                    get_feature,
                    split_data,
                    get_model_input)


def create_pipeline(**kwargs) -> Pipeline:
    preprocess_pipeline = pipeline([
        node(
            func=get_intermediate,
            inputs='shopping_raw',
            outputs='shopping_02_intermediate',
            name='get_intermediate_data'
            ),
        node(
            func=get_primary,
            inputs='shopping_02_intermediate',
            outputs='shopping_03_primary',
            name='get_primary_data'
            ),
        node(
            func=get_feature,
            inputs='shopping_03_primary',
            outputs='shopping_04_feature',
            name='get_feature_data'
        )
    ])
    
    encode_pipeline = pipeline([
        node(
            func=split_data,
            inputs=[
                'input_data',
                'params:split_data',
                'params:features'],
            outputs=[
                '_X_train',
                '_X_val',
                '_X_test',
                'y_train',
                'y_val',
                'y_test'
                ],
        ),
        node(
            func=get_model_input,
            inputs=[
                '_X_train',
                '_X_val',
                '_X_test',
                'params:features'
                ],
            outputs=['X_train', 'X_val', 'X_test'],
        )
    ])

    model_input1 = pipeline(
        pipe=encode_pipeline,
        inputs={'input_data': 'shopping_raw'},
        outputs={
            'X_train': 'X_train_intermediate',
            'X_val': 'X_val_intermediate',
            'X_test': 'X_test_intermediate',
            'y_train': 'y_train_intermediate',
            'y_val': 'y_val_intermediate',
            'y_test': 'y_test_intermediate'
            },
        namespace='intermediate_data_layer_pipeline'
        )
    
    model_input2 = pipeline(
        pipe=encode_pipeline,
        inputs={'input_data': 'shopping_02_intermediate'},
        outputs={
            'X_train': 'X_train_primary',
            'X_val': 'X_val_primary',
            'X_test': 'X_test_primary',
            'y_train': 'y_train_primary',
            'y_val': 'y_val_primary',
            'y_test': 'y_test_primary'
            },
        namespace='primary_data_layer_pipeline'
        )
    
    model_input3 = pipeline(
        pipe=encode_pipeline,
        inputs={'input_data': 'shopping_03_primary'},
        outputs={
            'X_train': 'X_train_feature',
            'X_val': 'X_val_feature',
            'X_test': 'X_test_feature',
            'y_train': 'y_train_feature',
            'y_val': 'y_val_feature',
            'y_test': 'y_test_feature'
            },
        namespace='feature_data_layer_pipeline'
        )

    return model_input1 + model_input2 + model_input3 + preprocess_pipeline
