![](img/logo_readme.png)

# Herramienta de Análisis Predictivo de Contratación Eficiente - Instituto Nacional Penitenciario y Carcelario (INPEC)


Este proyecto implementa una herramienta integral, tanto descriptiva como predictiva, que optimiza la gestión de contratación dentro del INPEC. Esta herramienta ofrece una visualización comprensible del análisis descriptivo basado en el registro histórico del SECOP. Adicionalmente, dispone de una funcionalidad predictiva que estima la probabilidad de una adición presupuestaria, determina el monto recomendado para dicha adición, calcula la probabilidad de extensión del contrato y sugiere el número de días adecuados para una prórroga.

## Tabla de contenido  
- [Información general](#informacion_general)  
- [Estructura del repositorio](#estructura) 
- [Tecnologías](#tecnologias) 
- [Ejecutar localmente](#ejecutarlocal)  
- [Herramienta Descriptiva - Predictiva](#herramienta) 
- [Autores](#autores) 
- [Contacto](#contacto)
   
## Información general
![](img/workflow.png)

La herramienta fue desarrollada como proyecto final de la Maestría en Inteligencia Analítica para la Toma de Decisiones. El proyecto se desarrollo en varias partes: 

1. **Extracción:** extracción de los datos historicos por medio de una conexión al API del SECOP I Y II.
2. **Transformación:** normalización de los datos, creación de nuevas variables, filtro de datos, limpieza y proceso de scrambling para valores faltantes. Adicionalmente el resultado de este proceso ETL se envio a BigQuery como el data warehose de los datos.
3. **Análisis:** análisis exploratorio y  análisis descriptivo de los datos.
4. **Modelamiento:** aplicación de métodos para determinar la importancia de las características en las variables de salida de los modelos. Implementación de modelos de regresión, clasificación y redes neuronales, además de la ejecución de procesos de optimización y validación de resultados.
5. **Streamlit Web App:** se implementó una aplicación web Streamlit para la visualización y ejecución de modelos encargados de realizar predicciones sobre las variables de interés.
6. **Deploy Web App:** se ha desplegado una instancia de ``Cloud Run`` en la nube de Google Cloud Platform (GCP), la cual asumirá la responsabilidad de ejecutar la herramienta web a través de una URL pública. El objetivo de esta implementación es gestionar el servicio de manera más eficiente y simplificar su uso.
7. **Desarrollo Herramienta:** la herramienta final se diseñó utilizando Looker Studio, donde se implementó un análisis descriptivo y se incorporó a una aplicación web de predicción.

## Estructura del repositorio
Este repositorio utiliza la siguiente estructura:
* `/app_tool`: este directorio contiene el script principal y sus dependencias para la ejecución de la aplicación web de la herramienta predictiva.
* `/data_extraction`: este directorio contiene los notebooks del proceso de extracción de los datos desde su fuente principal.
* `/exploration_data`: este directorio contiene los notebooks del proceso de análisis exploratorio de los datos.
*  `/img`: este directorio contiene imágenes utilizadas en la aplicación.
* `/models`: este directorio contiene los notebooks de los modelos entrenados que se usan en este proyecto. Estos modelos incluyen los modelos LightGBM, XGBoost, Random Forest y Keras.
* `/utils`: este directorio contiene los scripts necesarios para realizar la conexión, extracción y carga de dato a Big Query en Google Cloud.
* `/validations`: este directorio contiene el notebooks del proceso de validación de la app web predictiva.
* `/Dockerfile`: este archivo contiene instrucciones para que Docker cree la imagen, configure el entorno de Python, instale las dependencias requeridas e inicie la Aplicación Streamlit Web.
* `/requirements.txt`: este archivo contiene todos los paquetes de Python que deben instalarse para ejecutar la aplicación.
* `/.gitignore`: este archivo contiene la lista de archivos y directorios que están excluidos del repositorio de Git.

## Tecnologías
El proyecto se creo con:

* `Streamlit` para el desarrollo de aplicaciones web.
* `Sklearn`, `LightGBM`, `XGBoost` y `Keras` para el desarrollo de modelos de aprendizaje automático.
* `Pandas` para el procesamiento de datos.
* ``GCP-Cloud Run``: para el despliegue e infraestructura del app.

## Ejecutar localmente - App Web
Clonar el respositorio

```bash
  git clone https://github.com/njimenez92/proyecto-grado-miad.git
```

Ir a la carpeta donde clono el repositorio

```bash
  cd /proyecto-grado-miad
```

Instalar dependencias

```bash
  pip install -r requirements.txt
```

Inicie localmente `App Streamlit`

```bash
  streamlit run app_tool/app.py
```

## Herramienta Descriptiva - Predictiva 
El primer enlace a continuación lleva al tablero completo de la herramienta. Este tablero integra tanto elementos predictivos como descriptivos para proporcionar una visión completa y detallada del producto final. Y el segundo corresponde al ``Streamlit Web App`` en donde esta la herramienta de predicción de los modelos.

- [Herramienta-Final-Looker](https://lookerstudio.google.com/u/0/reporting/bcc04777-e44e-47cb-95fa-492c884c6b4a/page/4HOOD)
- [Herramienta-Predictiva](https://app-inpec-xhzoorl2zq-uc.a.run.app/)

## Autores
- [Natalia Jiménez](https://github.com/njimenez92)
- [Maria José Baquero](https://github.com/majobaqueroj26)
- [Mario Rivera](https://github.com/marioriveravargas)
## Contacto
Puede informar cualquier problema [aquí](https://github.com/njimenez92/proyecto-grado-miad/issues). Para cualquier consulta o sugerencia adicional, no dude en comunicarse.

