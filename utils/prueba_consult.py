# %%
import os
import pandas as pd
from datetime import datetime

from utils.bq_conn import bq_conn_file
# %%
bq_client = bq_conn_file(project_id="dsa-miad-365616")
# %%
query = '''
SELECT
   refresh_date AS Day,
   term AS Top_Term,
   rank,
FROM `bigquery-public-data.google_trends.top_terms`
WHERE
   rank = 1
   AND refresh_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 WEEK)

GROUP BY Day, Top_Term, rank
ORDER BY Day DESC
'''
consult = bq_client.execute_query(query=query)
# %%
