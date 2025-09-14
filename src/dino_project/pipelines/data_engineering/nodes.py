# src/proyecto_ml/pipelines/data_engineering/nodes.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler  # ← ¡AGREGA ESTO!

def clean_donations_data(df_raw, parameters: dict):
    """Limpia los datos de donaciones usando parámetros configurables"""
    
    # Usar parámetros del YAML
    imputation_strategy = parameters["imputation_strategy"]
    scaling_vars = parameters["scaling"] 
    outlier_params = parameters["outlier_limits"]
    encode_cols = parameters["encode_columns"]
    
    df_clean = df_raw.copy()
    
    # 1. IMPUTACIÓN DE VALORES FALTANTES
    for col in df_clean.columns:
        if df_clean[col].isnull().any():
            if df_clean[col].dtype == 'object':
                # Imputar categóricas con moda
                df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
            else:
                # Imputar numéricas con mediana
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    # 2. MANEJO DE OUTLIERS (winsorization)
    numeric_vars = ['Weight (lbs)', 'Daily Walk Distance (miles)', 
                    'Play Time (hrs)', 'Annual Vet Visits']
    
    for col in numeric_vars:
        if col in df_clean.columns:
            Q1 = df_clean[col].quantile(outlier_params["lower_percentile"])
            Q3 = df_clean[col].quantile(outlier_params["upper_percentile"])
            IQR = Q3 - Q1
            lower_bound = Q1 - outlier_params["iqr_multiplier"] * IQR
            upper_bound = Q3 + outlier_params["iqr_multiplier"] * IQR
            
            # Aplicar winsorization
            df_clean[col] = np.where(df_clean[col] < lower_bound, lower_bound, df_clean[col])
            df_clean[col] = np.where(df_clean[col] > upper_bound, upper_bound, df_clean[col])
    
    # 3. ESCALADO DE VARIABLES
    # StandardScaler
    if scaling_vars["standard_scaler"]:
        scaler_standard = StandardScaler()
        for col in scaling_vars["standard_scaler"]:
            if col in df_clean.columns:
                df_clean[col] = scaler_standard.fit_transform(df_clean[[col]])
    
    # RobustScaler  
    if scaling_vars["robust_scaler"]:
        scaler_robust = RobustScaler()
        for col in scaling_vars["robust_scaler"]:
            if col in df_clean.columns:
                df_clean[col] = scaler_robust.fit_transform(df_clean[[col]])
    
    # 4. CODIFICACIÓN DE VARIABLES CATEGÓRICAS
    df_encoded = df_clean.copy()
    for col in encode_cols:
        if col in df_encoded.columns and col != 'Healthy':  # No codificar target
            df_encoded = pd.get_dummies(df_encoded, columns=[col], 
                                      prefix_sep='_', drop_first=True)
    
    # 5. CORRECCIÓN DE VALORES NEGATIVOS
    numeric_cols = df_encoded.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df_encoded[col] = df_encoded[col].clip(lower=0)
    
    return df_encoded



def clean_charity_donations_data(df_raw, parameters: dict):
    """Limpia datos de DONACIONES caritativas (el nuevo dataset)"""
    
    df_clean = df_raw.copy()
    
    # 1. ELIMINAR COLUMNAS CON INFO PERSONAL
    columns_to_drop = ['donor_id', 'name', 'email']
    df_clean = df_clean.drop(columns=columns_to_drop)
    
    # 2. MANEJO DE OUTLIERS EN DONATION_AMOUNT
    Q1 = df_clean['donation_amount'].quantile(0.01)
    Q3 = df_clean['donation_amount'].quantile(0.99)
    df_clean['donation_amount'] = df_clean['donation_amount'].clip(Q1, Q3)
    
    # 3. TRANSFORMACIÓN LOGARÍTMICA
    df_clean['donation_amount_log'] = np.log1p(df_clean['donation_amount'])
    
    # 4. ENGINEERING DE FECHAS
    df_clean['donation_date'] = pd.to_datetime(df_clean['donation_date'])
    df_clean['donation_year'] = df_clean['donation_date'].dt.year
    df_clean['donation_month'] = df_clean['donation_date'].dt.month
    
    # 5. CODIFICACIÓN DE VARIABLES CATEGÓRICAS (LO QUE HICISTE EN NOTEBOOK)
    categorical_cols = ['country', 'payment_method', 'referral_channel', 'sector', 'campaign']
    df_encoded = pd.get_dummies(df_clean, columns=categorical_cols, prefix_sep='_', drop_first=True)
    
    return df_encoded

def clean_aac_intakes_outcomes(df_aac: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Limpieza y transformación del dataset AAC"""
    
    # Verificar que los parámetros necesarios existen
    required_params = ['animal_type_filter', 'null_imputation', 'health_mapping', 'positive_outcomes']
    for param in required_params:
        if param not in parameters:
            raise ValueError(f"Parámetro requerido faltante: {param}")
    
    # Filtrado inicial con manejo de errores
    animal_filter = parameters.get('animal_type_filter', 'Dog')
    df_clean = df_aac[df_aac['animal_type'] == animal_filter].copy()
    
    # Eliminar duplicados
    df_clean = df_clean.drop_duplicates(subset=['animal_id_intake'])
    
    # Manejo de nulos con valores por defecto
    null_params = parameters.get('null_imputation', {})
    df_clean['intake_condition'] = df_clean['intake_condition'].fillna(
        null_params.get('intake_condition', 'Unknown')
    )
    df_clean['outcome_type'] = df_clean['outcome_type'].fillna(
        null_params.get('outcome_type', 'Not Specified')
    )
    
    # Ingeniería de variables con manejo seguro
    health_mapping = parameters.get('health_mapping', {})
    df_clean['health_status_intake'] = df_clean['intake_condition'].map(
        lambda x: health_mapping.get(x, 0.5)
    )
    
    positive_outcomes = parameters.get('positive_outcomes', [])
    df_clean['positive_outcome'] = df_clean['outcome_type'].apply(
        lambda x: 1 if x in positive_outcomes else 0
    )
    
    # Segmentación por edad (opcional)
    if 'age_upon_intake_(years)' in df_clean.columns:
        age_bins = parameters.get('age_bins', [0, 1, 3, 7, 10, 20])
        age_labels = parameters.get('age_labels', ['Cachorro', 'Joven', 'Adulto', 'Maduro', 'Senior'])
        
        df_clean['age_group'] = pd.cut(
            df_clean['age_upon_intake_(years)'],
            bins=age_bins,
            labels=age_labels,
            right=False
        )
    
    # Tiempo en refugio en semanas (opcional)
    if 'time_in_shelter_days' in df_clean.columns:
        df_clean['shelter_stay_weeks'] = df_clean['time_in_shelter_days'] / 7
    
    # Selección de columnas finales
    selected_columns = parameters.get('selected_columns', [])
    available_columns = [col for col in selected_columns if col in df_clean.columns]
    
    # Si no hay columnas seleccionadas, mantener todas
    if not available_columns:
        available_columns = df_clean.columns.tolist()
    
    df_final = df_clean[available_columns].copy()
    
    return df_final