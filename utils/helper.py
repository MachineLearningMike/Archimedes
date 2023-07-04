import pandas as pd
import numpy as np
import requests
import json

def fetch_pools_data(
        pools: list,
        start_timestamp: int,
        end_timestamp: int
):
    url = "http://109.123.229.249:8545/api/farming/execute_query/"
    headers = { "Content-Type": "application/json" }

    chain_condition = []
    for pool in pools:
        chain_name = pool[0]; pool_name = pool[1]
        chain_condition.append(f"\"CHAIN\" = '{chain_name}' AND \"POOL\" = '{pool_name}'")

    chain_join = ' OR '.join(chain_condition)

    # query_text = f"SELECT \"TS_TO\", \"STGRS\", \"LPSupply\", \"CHAIN\", \"POOL\" FROM chain_farmingmodel WHERE ( {chain_join} ) AND \"TS_FROM\" >= {start_timestamp} AND \"TS_TO\" <= {end_timestamp} ORDER BY \"CHAIN\", \"TS_FROM\";"
    query_text = f"SELECT \"STGRS\", \"LPSupply\", \"TS_TO\" FROM chain_farmingmodel WHERE ( {chain_join} ) AND \"TS_FROM\" >= {start_timestamp} AND \"TS_TO\" <= {end_timestamp} ORDER BY \"CHAIN\", \"TS_FROM\";"

    query = { "query":  query_text}

    response = requests.post(url, headers=headers, data=json.dumps(query))
    if response.status_code == 200:
        result = response.json()
    else:
        print("Error: ", response.text)

    df = pd.DataFrame(result)
    assert df["STGRS"].to_numpy().shape[0] == df["LPSupply"].to_numpy().shape[0]
    assert df["LPSupply"].to_numpy().shape[0] == df["TS_TO"].to_numpy().shape[0]
    assert df["TS_TO"].to_numpy()[-1] == end_timestamp
    num = df.to_numpy()
    # print(num)

    assert num.shape[0] % len(pools) == 0
    nRows_per_pool = num.shape[0] // len(pools)
    pools = [num[id*nRows_per_pool:(id+1)*nRows_per_pool] for id in range(len(pools))]
    pools = [np.reshape(np.swapaxes(pool, 0, 1), (1, len(("STGRS", "LPSupply", "TS_TO")), -1)) for pool in pools]
    pools_state = np.concatenate(pools, axis=0)
    print("pools_state", pools_state)
    return pools_state
