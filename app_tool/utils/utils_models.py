import math
import os
import pathlib
import sys

sys.path.append(
    os.path.join(pathlib.Path(os.getcwd()))
)
from pickle import load

import numpy as np
import pandas as pd
import streamlit as st
from gensim.utils import simple_preprocess
from pycaret.classification import predict_model as pc
from pycaret.regression import predict_model as pr


def norm_text(texto:str):
    """
    The function takes a string as input, converts it to lowercase, tokenizes it, removes punctuation
    and words with length less than 1 or greater than 40, and returns the normalized text as a string.
    
    Args:
      texto (str): The input text that needs to be normalized.
    
    Returns:
      The function `norm_text` returns a normalized version of the input text, which is converted to
      lowercase and tokenized using the `simple_preprocess` function with specified parameters. The
      resulting tokens are then joined back into a string and returned.
    """
    texto = texto.lower()
    word_tokens = simple_preprocess(texto, deacc=True, min_len=1, max_len=40)
    texto = ' '.join(word_tokens)
    return texto




def normalice_data(features_df:pd.DataFrame, type:str)-> pd.DataFrame:
    """
    This function normalizes data in a pandas DataFrame based on the specified type using pre-trained
    preprocessor models.
    
    Args:
      features_df (pd.DataFrame): A pandas DataFrame containing the features to be normalized.
      type (str): The "type" parameter is a string that specifies the type of normalization to be
    applied to the data. It can take on one of the following values: "monto", "prorroga", "tiempo",
    "keras", or "adicion". Depending on the value of "type",
    
    Returns:
      a pandas DataFrame with the normalized data based on the input type parameter. 
    """
    
    # convert dtype category
    features_df['tipo_de_contrato'] = features_df['tipo_de_contrato'].astype('category')
    features_df['departamento_ejecucion'] = features_df['departamento_ejecucion'].astype('category')
    features_df['id_objeto_a_contratar'] = features_df['id_objeto_a_contratar'].astype('category')
    # normalice data
    path = pathlib.Path(__file__).parent
    #path = os.path.join(os.getcwd(),'app_tool', 'utils')
    if type == "monto":
        preprocessor = load(open(f'{path}/preprocessor_monto.pkl', 'rb'))
        data_scaler = preprocessor.transform(features_df)
    if type == "prorroga":
        preprocessor = load(open(f'{path}/preprocessor_prorroga.pkl', 'rb'))
        data_scaler = preprocessor.transform(features_df)
    if type == "tiempo":
        preprocessor = load(open(f'{path}/preprocessor_tiempo.pkl', 'rb'))
        data_scaler = preprocessor.transform(features_df)
    if type == "keras":
        preprocessor = load(open(f'{path}/preprocessor_keras.pkl', 'rb'))
        data_scaler = preprocessor.transform(features_df)
    else:
        preprocessor = load(open(f'{path}/preprocessor_adicion.pkl', 'rb'))
        data_scaler = preprocessor.transform(features_df)

    return data_scaler


def preprocess_data(features:dict, type:str)-> pd.DataFrame:
    """
    This function preprocesses a dictionary of features by converting it to a dataframe, normalizing
    text data, and scaling numerical data.
    
    Args:
      features (dict): The features parameter is a dictionary containing the input features for the
    machine learning model.
      type (str): The `type` parameter is a string that specifies the type of data normalization to be
    applied to the input features. It is used as an input to the `normalice_data` function, which is not
    shown in the code snippet provided.
    
    Returns:
      a preprocessed and normalized pandas DataFrame 
    """
    # convert dict to dataframe
    features_df  = pd.DataFrame([features])
    # normalice text
    features_df[['tipo_de_contrato', 
                 'departamento_ejecucion']] = features_df[['tipo_de_contrato', 
                 'departamento_ejecucion']].apply(lambda x: x.apply(norm_text))
    type_predict = type
    data_scaler = normalice_data(features_df=features_df, type=type_predict)
    return data_scaler


def predict_adicion(model_adicion, 
                    model_monto, 
                    model_monto_keras, 
                    keras:bool,
                    dataframe_adicion:pd.DataFrame, 
                    dataframe_monto:pd.DataFrame):
    """
    This function predicts the probability of addition and estimated amount based on machine learning or
    neural network models.
    
    Args:
      model_adicion: This is a machine learning or statistical model that predicts the probability of a
    certain event (adición) occurring based on input data.
      model_monto: It is a machine learning or neural network model used for predicting the estimated
    amount in days.
      model_monto_keras: This parameter is a Keras model for predicting the estimated amount in days.
    Keras is a high-level neural networks API, written in Python and capable of running on top of
    TensorFlow, CNTK, or Theano.
      keras (bool): A boolean variable indicating whether to use a Keras neural network model for
    predicting the estimated amount or a machine learning model.
      dataframe_adicion (pd.DataFrame): A pandas DataFrame containing the input data for the model that
    predicts the probability of an addition.
      dataframe_monto (pd.DataFrame): The parameter `dataframe_monto` is a pandas DataFrame containing
    the input data for the model that predicts the estimated amount in days.
    
    Returns:
      two values: `result_prob_adicion` and `result_monto`.
    """
    predictions_data = pc(estimator = model_adicion, 
                          data = dataframe_adicion,
                          probability_threshold=0.25)
    if predictions_data['prediction_label'][0] == 1:
        # resultado probabilidad de adición
        result_prob_adicion = predictions_data['prediction_score'][0]*100

        if keras:
            # Modelo de detección de monto estimado en días - Red Neuronal
            input_test_press = np.asarray(dataframe_monto).astype(np.float32)
            example_result = model_monto_keras.predict(input_test_press)
            result_monto = math.ceil(float(example_result))
        else:
            # Modelo de detección de monto estimado en días - Machine Learning
            predict_monto = pr(estimator=model_monto, 
                            data=dataframe_monto,
                            round=1)
            result_monto = predict_monto['prediction_label'][0]
    else:
        result_prob_adicion = 1
        if keras:
            # Modelo de detección de monto estimado en días - Red Neuronal
            input_test_press = np.asarray(dataframe_monto).astype(np.float32)
            example_result = model_monto_keras.predict(input_test_press)
            result_monto = math.ceil(float(example_result))
        else:
            # Modelo de detección de monto estimado en días - Machine Learning
            predict_monto = pr(estimator=model_monto, 
                            data=dataframe_monto,
                            round=1)
            result_monto = predict_monto['prediction_label'][0]
    return result_prob_adicion, result_monto


def predict_prorroga(model_prorroga, model_tiempo, model_tiempo_keras ,keras:bool, dataframe_prorroga:pd.DataFrame, dataframe_tiempo:pd.DataFrame):
    """
    This function takes in machine learning models and dataframes, predicts the probability of overtime
    and the duration of overtime, and returns the results.
    
    Args:
      model_prorroga: The model used for predicting the probability of extension (prorroga).
      model_tiempo: It is a machine learning or neural network model used for predicting the time of
    addition.
      model_tiempo_keras: The model_tiempo_keras parameter is a neural network model used for predicting
    the time of addition in a given task. It is used in the predict_prorroga function to determine the
    time of addition if the probability of extension is greater than 0.25.
      keras (bool): A boolean variable indicating whether to use a Keras neural network model for
    predicting the time of addition or a machine learning model.
      dataframe_prorroga (pd.DataFrame): The input data for the model that predicts the probability of a
    contract extension (prorroga). It should be a pandas DataFrame.
      dataframe_tiempo (pd.DataFrame): The parameter "dataframe_tiempo" is a pandas DataFrame containing
    the input data for the model that predicts the time of addition. This data should be in the same
    format as the data used to train the model.
    
    Returns:
      two values: `result_prob_prorroga` and `result_tiempo_dias`.
    """
    predictions_data = pc(estimator = model_prorroga, 
                          data = dataframe_prorroga,
                          probability_threshold=0.25)
    if predictions_data['prediction_label'][0] == 1:
        # resultado probabilidad de prorroga
        result_prob_prorroga = predictions_data['prediction_score'][0]*100

        if keras:
            # Modelo de detección de tiempo de adición - Red Neuronal
            input_test_press = np.asarray(dataframe_tiempo).astype(np.float32)
            example_result = model_tiempo_keras.predict(input_test_press)
            result_tiempo_dias = math.ceil(float(example_result))
        else:
            # Modelo de detección de tiempo de adicón - Machine Learning
            predict_tiempo_dias = pr(estimator=model_tiempo, 
                                    data=dataframe_tiempo,
                                    round=1)
            
            result_tiempo_dias = predict_tiempo_dias['prediction_label'][0]
    else:
        result_prob_prorroga = 1
        result_tiempo_dias = 0
    return result_prob_prorroga, result_tiempo_dias

