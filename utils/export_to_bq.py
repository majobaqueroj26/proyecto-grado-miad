# %%
from utils.bq_conn import load_credentials
import pandas as pd


secop_I = pd.read_csv('data/extrac_secopII_I.csv')

# %%
def upload_to_bq(bq_table, dataframe, project_id, my_credentials):
  """
  This function takes a dataframe, a table name, a project ID, and credentials, and uploads the
  dataframe to the table in BigQuery
  
  Args:
    bq_table: The name of the table you want to create in BigQuery.
    dataframe: the dataframe you want to upload to BigQuery
    project_id: The name of your Google Cloud project.
    my_credentials: The credentials object you created in the previous step.
  """

    # Column conversion added to load table

  dataframe.to_gbq(bq_table, project_id=project_id, if_exists='replace',
                    credentials=my_credentials)

# from utils.bq_conn import load_credentials

# %%
# Nombre de tabla
table = 'Proyecto.DatosSecopII'
# Nombre proyecto google
project_id = 'dsa-miad-365616'
# Credenciales de acceso en google
credentials = load_credentials()

# Dataframe a subir / tabla
table_up = secop_I
upload_to_bq(table, table_up, project_id, credentials)
# %%
