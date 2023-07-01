import pandas_gbq
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file("creds.json")
# chain_list = ['bsc', 'avalanche', 'polygon', 'arbitrum', 'optimism']
chain_list = ["bsc", "avalanche", "polygon", "arbitrum"]
pool_list = {
    "bsc": ["USDT"],
    "avalanche": ["USDC", "USDT", "FRAX"],
    "polygon": ["USDC", "USDT"],
    "arbitrum": ["USDC", "USDT", "FRAX"],
    "optimism": ["USDC", "DAI", "FRAX"],
}


def download():
    project_id = "train-portfolio-ml"

    dataset_id = "farming"
    tbl_name = "tbl_bsc_USDT"

    orderby = "TS_FROM"
    query = f"SELECT * FROM `{dataset_id}.{tbl_name}` order by {orderby}"

    df = pandas_gbq.read_gbq(
        query, project_id=project_id, credentials=creds, progress_bar_type=None
    )

    return df
