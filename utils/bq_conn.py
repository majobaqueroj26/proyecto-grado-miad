"""
    Script that contains the necessary methods for the communication
    of the project to a BigQuery database.
"""

import os
import pathlib
import json
import sys

from google.cloud import bigquery
sys.path.append(
    os.path.join(pathlib.Path(__file__).parent.parent)
)
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

class BigQuery:
    """
    This class allows you to connect a project to a BigQuery database.
    Args:
        - my_credentials (google.oauth2.service_account.Credentials): BQ service account.
        - project_id (str): project id.
    """

    def __init__(self, my_credentials, project_id=None):
        self.credentials = my_credentials
        self.project_id = project_id
        self.client = self.connect_client() if project_id else None

    def connect_client(self):
        """
        Return the client after making the connection to BQ.
        Returns:
            - BQ client
        """
        try:
            client = bigquery.Client(
                credentials=self.credentials,
                project=self.project_id,
            )
            return client
        except Exception as msg:
            raise Exception("Could not connect to BQ Client || ", msg) from None

    def execute_query(self, query):
        """
        Returns the results of a query in DataFrame format.
        Args:
            - query (str): SQL query
        Returns:
            - DataFrame
        """
        try:
            #t_inicial = time.time()
            dataframe = self.client.query(query, location="US").result().to_dataframe()
            #t_final = time.time() - t_inicial
            return dataframe
        except Exception as msg:
            raise Exception(
                "Could not transform response to Dataframe || ", msg
            ) from None


def load_credentials():
    """
    It loads the credentials from the environment variable CREDENTIALS_PATH
    Returns:
      Credentials
    """

    # Load environment variables
    credentials_path = os.environ.get("BQ_PATH_MIAD")
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )
    return credentials


def bq_conn_file(project_id:str):
    """
    This function loads the credentials from the pipeline or from the local machine, depending on the
    environment

    Args:
      project_id (str): The name of the project you created in the 
      Google Cloud Platform. Defaults to chiperdw

    Returns:
      A BigQuery client object.
    """
    # Load environment variables
    credentials_path = os.environ.get("BQ_PATH_MIAD")
    # Loading credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )

    bq_client = BigQuery(my_credentials=credentials, project_id=project_id)

    return bq_client


