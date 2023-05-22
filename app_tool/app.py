import os
import sys
import pathlib
import streamlit as st
sys.path.append(
    os.path.join(pathlib.Path(os.getcwd()))
)
from PIL import Image
from app_tool.utils.utils_models import preprocess_data, predict_adicion, predict_prorroga
from pycaret.classification import load_model





def main(model_adicion,
         model_monto,
         model_prorroga,
         model_tiempo,
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
        cuantia_proceso = st.number_input('Cuantia del Proceso', step=1)
        plazo_ejecucion_dias = st.number_input('Plazo de Ejecución del Contrato', step=1)
        id_objeto_a_contratar = st.number_input('Id Objeto a Contratar', step=1)

    features = {'tipo_de_contrato': tipo_contrato, 'departamento_ejecucion':departamento,
                'id_grupo': id_grupo, 'cuantia_proceso': cuantia_proceso,
                'id_objeto_a_contratar': id_objeto_a_contratar, 
                'plazo_de_ejec_del_contrato_': plazo_ejecucion_dias
                }

    features_preprocess_monto = preprocess_data(features=features, type="monto")
    features_preprocess_adicion = preprocess_data(features=features, type="adicion")
    features_preprocess_prorroga = preprocess_data(features=features, type="prorroga")
    features_preprocess_tiempo = preprocess_data(features=features, type="tiempo")

    # Predictios Sections
    title_image = Image.open(f"{proyect_path}/img/logo-inpec.png")
    st.image(title_image)

    st.title("Herramienta de Predicción de Contratación Eficiente - INPEC")

    st.markdown("## Análisis Predictivo")
    if st.button('Predecir :point_left:', help="Botón para realizar la ejecución de las predicciones"):
        # Entradas
        # create columns for the chars
        input_1, input_2 = st.columns(2)
        with input_1:
            ##---------------------------predicciones presupuestales------------------------------------------------------#
            # Predicción adición y monto estimado
            prediction_adicion, prediction_monto = predict_adicion(model_adicion=model_adicion,
                                                model_monto=model_monto,
                                                dataframe=features_preprocess_adicion,
                                                monto_inicial=cuantia_proceso)
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
                #Predicción prorroga y tiempo adicionado estimado
                prediction_prorroga, prediction_tiempo = predict_prorroga(model_prorroga=model_prorroga,
                                                    model_tiempo=model_tiempo,
                                                    dataframe=features_preprocess_prorroga)
                tiempo = int(prediction_tiempo)
                prorroga =  "{:.1f}%".format(prediction_prorroga)
                # Predicción prorroga estimado
                st.markdown('<h3 style="color:#005073;">Probabilidad de Prorroga</h2>', unsafe_allow_html=True)
                st.metric(label="Probabilidad de Prorroga",value=prorroga, )
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
        # Path model
        model_path = pathlib.Path(__file__).parent / 'models'
        # Load model
        model_monto = load_model(f'{model_path}/lightgbm_model_monto_recomendado')
        model_adicion = load_model(f'{model_path}/RFClassifier_adicion')
        model_prorroga = load_model(f'{model_path}/xgboost_prorroga')
        model_tiempo = load_model(f'{model_path}/lightgbm_tiempo_adicion')
        return model_monto, model_adicion, model_prorroga, model_tiempo
    
    model_monto, model_adicion, model_prorroga, model_tiempo = load_models()

    # Imagen Portada
    proyect_path = pathlib.Path(__file__).parent.parent
    main(model_adicion=model_adicion,model_monto=model_monto, 
         model_prorroga=model_prorroga, model_tiempo=model_tiempo,
         proyect_path=proyect_path)