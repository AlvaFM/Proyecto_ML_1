## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `context`, 'session', `catalog`, and `pipelines`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

# 🐕 Proyecto Machine Learning - Análisis de Bienestar Animal

## 📋 Información del Proyecto
**Integrantes:** Álvaro Flores y Aurora Mansilla 🦕  
**Asignatura:** Machine Learning (MLY0100)  
**Fecha de Entrega:** 15-09-2025  
**Framework:** Kedro 0.18.0+

## 🎯 Objetivo del Proyecto
Analizar cómo la **edad y nivel de actividad** de los perros influyen en su estado de salud general, y cómo esta relación se ve potenciada por la **inversión en bienestar animal** en diferentes regiones.

### 🔍 Hipótesis Principal
"La edad y nivel de actividad de los perros influye en su estado de salud general, y esta relación se ve potenciada en lugares con mayor inversión en bienestar."

## 📊 Datasets Utilizados
1. **`synthetic_dog_breed_health_data`** - Datos de salud canina
   - Variables: edad, peso, actividad, visitas veterinarias, estado de salud
   https://www.kaggle.com/datasets/aaronisomaisom3/canine-wellness-dataset-synthetic-10k-samples
2. **`animal_charity_donation_records`** - Donaciones a beneficencia animal  
   - Variables: montos, países, campañas, tipos de donación
   https://www.kaggle.com/datasets/jaderz/synthetic-animal-charity-donations
3. **`aac_intakes_outcomes`** - Datos de clínica veterinaria
   - Variables: ingresos, tratamientos, resultados
   https://www.kaggle.com/datasets/aaronschlegel/austin-animal-center-shelter-intakes-and-outcomes

## 🛠️ Instalación y Configuración

### Prerrequisitos
```bash
Python 3.8+
Git