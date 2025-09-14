# src/proyecto_ml/pipelines/data_engineering/pipeline.py

from kedro.pipeline import Pipeline, node
from .nodes import clean_donations_data, clean_charity_donations_data, clean_aac_intakes_outcomes # ← AGREGAR LA NUEVA FUNCIÓN

def create_pipeline(**kwargs):
    return Pipeline([
        # 1. Primer dataset: Salud de perros
        node(
            func=clean_donations_data,
            inputs=["synthetic_dog_breed_health_data", "params:data_engineering"],
            outputs="cleaned_dog_breed",
            name="clean_dog_health_node"
        ),
        
        # 2. Segundo dataset: Donaciones de dinero ← ¡NUEVO NODO!
        node(
            func=clean_charity_donations_data,
            inputs=["animal_charity_donation_records", "params:data_engineering"],
            outputs="cleaned_charity_donations",  # ← NUEVO OUTPUT
            name="clean_charity_donations_node"
        ),

          # 3. Tercer dataset: Ingresos y salidas del refugio 
       node(
            func=clean_aac_intakes_outcomes,
            inputs=["aac_intakes_outcomes", "params:aac_processing"],    # ← CORRECTO
            outputs="cleaned_aac_intakes_outcomes",
            name="clean_aac_intakes_outcomes"
        )
    ])