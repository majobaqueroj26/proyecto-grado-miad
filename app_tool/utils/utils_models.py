import os 
import pandas as pd
from pickle import load
import streamlit as st
from gensim.utils import simple_preprocess
from pycaret.classification import predict_model as pc
from pycaret.regression import predict_model as pr



@st.cache_data
def norm_text(texto:str):
    texto = texto.lower()
    word_tokens = simple_preprocess(texto, deacc=True, min_len=1, max_len=40)
    texto = ' '.join(word_tokens)
    return texto



@st.cache_data
def normalice_data(features_df:pd.DataFrame, type:str)-> pd.DataFrame:
    
    # convert dtype category
    features_df['tipo_de_contrato'] = features_df['tipo_de_contrato'].astype('category')
    features_df['departamento_ejecucion'] = features_df['departamento_ejecucion'].astype('category')
    features_df['id_objeto_a_contratar'] = features_df['id_objeto_a_contratar'].astype('category')
    # normalice data
    path = os.path.join(os.getcwd(),'app_tool', 'utils')
    if type == "monto":
        preprocessor = load(open(f'{path}/preprocessor_monto.pkl', 'rb'))
        data_scaler = preprocessor.transform(features_df)
    if type == "prorroga":
        preprocessor = load(open(f'{path}/preprocessor_prorroga.pkl', 'rb'))
        data_scaler = preprocessor.transform(features_df)
    if type == "tiempo":
        preprocessor = load(open(f'{path}/preprocessor_tiempo.pkl', 'rb'))
        data_scaler = preprocessor.transform(features_df)
    else:
        preprocessor = load(open(f'{path}/preprocessor_adicion.pkl', 'rb'))
        data_scaler = preprocessor.transform(features_df)

    return data_scaler

@st.cache_data
def preprocess_data(features:dict, type:str)-> pd.DataFrame:
    # convert dict to dataframe
    features_df  = pd.DataFrame([features])
    # normalice text
    features_df[['tipo_de_contrato', 
                 'departamento_ejecucion']] = features_df[['tipo_de_contrato', 
                 'departamento_ejecucion']].apply(lambda x: x.apply(norm_text))
    type_predict = type
    data_scaler = normalice_data(features_df=features_df, type=type_predict)
    return data_scaler


def predict_adicion(model_adicion, model_monto, dataframe:pd.DataFrame, monto_inicial:int):
    predictions_data = pc(estimator = model_adicion, 
                          data = dataframe,
                          probability_threshold=0.25)
    if predictions_data['prediction_label'][0] == 1:
        # resultado probabilidad de adición
        result_prob_adicion = predictions_data['prediction_score'][0]*100
        # resultado monto estimado en días
        predict_monto = pr(estimator=model_monto, 
                           data=dataframe,
                           round=1)
        result_monto = predict_monto['prediction_label'][0]
    else:
        result_prob_adicion = 1
        result_monto = monto_inicial
    return result_prob_adicion, result_monto


def predict_prorroga(model_prorroga, model_tiempo, dataframe:pd.DataFrame):
    predictions_data = pc(estimator = model_prorroga, 
                          data = dataframe,
                          probability_threshold=0.25)
    if predictions_data['prediction_label'][0] == 1:
        # resultado probabilidad de prorroga
        result_prob_prorroga = predictions_data['prediction_score'][0]*100
        # resultado tiempo adicionado en días
        predict_tiempo_dias = pr(estimator=model_tiempo, 
                                 data=dataframe,
                                 round=1)
        result_tiempo_dias = predict_tiempo_dias['prediction_label'][0]

    else:
        result_prob_prorroga = 1
        result_tiempo_dias = 0
    return result_prob_prorroga, result_tiempo_dias

