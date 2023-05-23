import os
import pathlib
import sys

import pandas as pd
import streamlit as st

sys.path.append(
    os.path.join(pathlib.Path(os.getcwd()))
)
from PIL import Image
from pycaret.classification import load_model
from tensorflow.keras.models import load_model as model_load

from app_tool.utils.utils_models import (predict_adicion, predict_prorroga,
                                         preprocess_data)


def main(model_adicion,
         model_monto,
         model_prorroga,
         model_tiempo,
         model_tiempo_keras,
         model_monto_keras,
         proyect_path):

    with st.sidebar:
        st.markdown("# Ingrese los datos de la consulta")
        tipo_contrato = st.selectbox(
        'Tipo de contrato',
        ('','Acuerdo Marco', 'Arrendamiento', 'Comodato', 'Prestación de Servicios',
        'Compraventa', 'Concesión', 'Consultoria', 'Suministro' ,'Obra','Otro tipo de contrato'))
        departamento = st.selectbox('Departamento de Ejecución',('','Amazonas','Antioquia',
                        'Arauca','Atlantico','Bogota','Bolivar','Boyaca','Caldas','Caqueta',
                        'Casanare','Cauca','Cesar','Choco','Colombia','Cordoba','Cundinamarca',
                        'Huila','La guajira','Magdalena','Meta','Nariño','Norte de Santander',
                        'Putumayo','Quindio','Risaralda','San Andres','Santander','Sucre','Tolima',
                        'Valle del Cauca'))
        id_grupo = st.selectbox('Id Grupo', ('','A', 'B', 'C', 'D', 'E', 'F', 'G'))
        cuantia_proceso = st.number_input('Cuantia del Proceso',step=100000)
        plazo_ejecucion_dias = st.slider('Plazo de Ejecución del Contrato',
                                        min_value=0,
                                        max_value=2000,
                                        step=30)
        id_objeto_a_contratar = st.selectbox('Id Objeto a Contratar', ('',10000000, 11000000, 12000000, 
                                                                       13000000, 14000000, 15000000, 20000000, 
                                                                       21000000, 22000000, 23000000, 24000000, 
                                                                       25000000, 26000000, 27000000, 30000000, 
                                                                       31000000, 32000000, 39000000, 40000000, 
                                                                       41000000, 42000000, 43000000, 44000000, 
                                                                       45000000, 46000000, 47000000, 48000000, 
                                                                       49000000, 50000000, 51000000, 52000000, 
                                                                       53000000, 54000000, 55000000, 56000000, 
                                                                       60000000, 70000000, 71000000, 72000000, 
                                                                       73000000, 76000000, 77000000, 78000000, 
                                                                       80000000, 81000000, 82000000, 83000000, 
                                                                       84000000, 85000000, 86000000, 90000000, 
                                                                       91000000, 92000000, 93000000, 94000000, 
                                                                       95000000))
        type_model = st.selectbox('Tipo de Modelo', ('','Machine Learning', 'Deep Learning'))

    features = {'tipo_de_contrato': tipo_contrato, 'departamento_ejecucion':departamento,
                'id_grupo': id_grupo, 'cuantia_proceso': cuantia_proceso,
                'id_objeto_a_contratar': id_objeto_a_contratar, 
                'plazo_de_ejec_del_contrato_': plazo_ejecucion_dias
                }

    features_preprocess_monto = preprocess_data(features=features, type="monto")
    features_preprocess_adicion = preprocess_data(features=features, type="adicion")
    features_preprocess_prorroga = preprocess_data(features=features, type="prorroga")
    features_preprocess_tiempo = preprocess_data(features=features, type="tiempo")
    features_preprocess_keras = preprocess_data(features=features, type="keras")
    keras = True if type_model == 'Deep Learning' else False

    # Predictios Sections
    title_image = Image.open(f"{proyect_path}/img/logo-inpec.png")
    st.image(title_image)

    st.title("Herramienta de Predicción de Contratación Eficiente - INPEC")

    st.markdown("## Guía de Configuración")
    with st.expander("Guía de configuración :book:"):

        st.write("1. **Tipo de Contrato:** Tipo de contrato de acuerdo a su marco jurídico.")
        st.write("2. **Departamento de Ejecución:** Departamento en el cual se ejecutara el contrato.")
        st.write("3. **Id Grupo:** ID de la Categorización inicial del bien o servicio definido en el proceso de compra, de acuerdo con sus características principales.")
        grupo_id = pd.read_parquet(f"{proyect_path}/app_tool/info_data/grupo.parquet")
        st.dataframe(grupo_id)
        st.write("4. **Cuantia del Proceso:** Valor por el cual se lanza el proceso de compra.")
        st.write("5. **Plazo de Ejecución del Contrato:** Valor sobre el cual se determina la duración del contrato.")
        st.write("6. **Id Objeto a Contrato:** ID del Objeto de la contratación, basado en el catálogo de bienes y servicios UNSPSC.")
        objeto_a_contratar = pd.read_parquet(f"{proyect_path}/app_tool/info_data/objeto_a_contratar.parquet")
        st.dataframe(objeto_a_contratar)
        st.write("6. **Tipo de Modelo:** Configuración para escoger que tipo de modelo ejecutar para la predicción.")


    st.markdown("## Análisis Predictivo")
    if st.button('Predecir :point_left:', help="Botón para realizar la ejecución de las predicciones"):
        # Entradas
        # create columns for the chars
        input_1, input_2 = st.columns(2)
        with input_1:
            ##---------------------------predicciones presupuestales------------------------------------------------------#
            features_monto_final = features_preprocess_keras if type_model == 'Deep Learning' else features_preprocess_monto            
            # Predicción adición y monto estimado
            prediction_adicion, prediction_monto = predict_adicion(model_adicion=model_adicion,
                                                model_monto=model_monto,
                                                model_monto_keras=model_monto_keras,
                                                keras=keras,
                                                dataframe_adicion=features_preprocess_adicion,
                                                dataframe_monto=features_monto_final
                                                )
            adicion =  "{:.1f}%".format(prediction_adicion)
            monto = "${:,.2f}".format(prediction_monto)
            # Predicción monto estimado
            st.markdown('<h3 style="color:#005073;">Probabilidad de Adición Presupuestal</h2>', unsafe_allow_html=True)
            st.metric(label="Probabilidad de Adición",value=adicion, )
            # Predicción monto estimado
            st.markdown('<h3 style="color:#e8702a;">Monto estimado del Contrato</h2>', unsafe_allow_html=True)
            st.metric(label="Monto Estimado final",value=monto, )

        with input_2:
            ##---------------------------predicciones tiempo---------------------------------------------------------------#
            features_tiempo_final = features_preprocess_keras if type_model == 'Deep Learning' else features_preprocess_tiempo
            #Predicción prorroga y tiempo adicionado estimado
            prediction_prorroga, prediction_tiempo = predict_prorroga(model_prorroga=model_prorroga,
                                                model_tiempo=model_tiempo,
                                                model_tiempo_keras=model_tiempo_keras,
                                                keras=keras,
                                                dataframe_prorroga=features_preprocess_prorroga,
                                                dataframe_tiempo=features_tiempo_final)
            tiempo = int(prediction_tiempo)
            prorroga =  "{:.1f}%".format(prediction_prorroga)
            # Predicción prorroga estimado
            st.markdown('<h3 style="color:#005073;">Probabilidad de Prórroga</h2>', unsafe_allow_html=True)
            st.metric(label="Probabilidad de Prórroga",value=prorroga, )
            # Predicción tiempo estimado
            st.markdown('<h3 style="color:#e8702a;">Tiempo de Adición Estimado</h2>', unsafe_allow_html=True)
            st.metric(label="Tiempo Adición final",value=tiempo, )

        st.success('El análisis predictivo fue ejecutado satisfactoriamente', icon="✅")

        if st.button('Reiniciar :leftwards_arrow_with_hook:', 
                    help="Botón para realizar nueva consulta"):
        # Clicking this button will rerun the script from the top
            st.experimental_rerun()

if __name__ == "__main__":

    # Configuración App - Page
    st.set_page_config(page_icon=":mag:", 
                    layout='wide',
                    menu_items={
                        'Report a bug': "https://github.com/njimenez92/proyecto-grado-miad/issues",
                        'About': """Esta Herramienta se realizo como proyecto de grado de la Mestría en 
                                Inteligencia Analítica para la Toma de decisiones""" })
    @st.cache_resource
    def load_models():
        """
        The function loads several machine learning models from specified paths.
        
        Returns:
          The function `load_models()` is returning six machine learning models: `model_monto`,
        `model_adicion`, `model_prorroga`, `model_tiempo`, `model_tiempo_keras`, and `model_monto_keras`.
        """
        # Path model
        model_path = pathlib.Path(__file__).parent / 'models'
        # Load model
        model_monto = load_model(f'{model_path}/lightgbm_model_monto_recomendado')
        model_adicion = load_model(f'{model_path}/RFClassifier_adicion')
        model_prorroga = load_model(f'{model_path}/xgboost_prorroga')
        model_tiempo = load_model(f'{model_path}/lightgbm_tiempo_adicion')
        model_tiempo_keras = model_load(f'{model_path}/keras_model_tiempo')
        model_monto_keras = model_load(f'{model_path}/keras_model_monto')
        return model_monto, model_adicion, model_prorroga, model_tiempo, model_tiempo_keras, model_monto_keras
    
    model_monto, model_adicion, model_prorroga, model_tiempo, model_tiempo_keras, model_monto_keras = load_models()

    # Imagen Portada
    proyect_path = pathlib.Path(__file__).parent.parent
    main(model_adicion=model_adicion,model_monto=model_monto, 
         model_prorroga=model_prorroga, model_tiempo=model_tiempo,
         model_tiempo_keras=model_tiempo_keras,model_monto_keras=model_monto_keras,
         proyect_path=proyect_path)