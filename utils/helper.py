import pandas as pd
import numpy as np
import requests
import json

def fetch_pools_data(
        pool_chains: list,
        start_timestamp: int,
        end_timestamp: int
):
    url = "http://109.123.229.249:8545/api/farming/execute_query/"
    headers = { "Content-Type": "application/json" }

    chain_condition = []
    for elem in pool_chains:
        pool_name = elem[0]; chain_name = elem[1]
        chain_condition.append(f"\"CHAIN\" = '{chain_name}' AND \"POOL\" = '{pool_name}'")

    chain_join = ' OR '.join(chain_condition)

    # query_text = f"SELECT \"TS_TO\", \"STGRS\", \"LPSupply\", \"CHAIN\", \"POOL\" FROM chain_farmingmodel WHERE ( {chain_join} ) AND \"TS_FROM\" >= {start_timestamp} AND \"TS_TO\" <= {end_timestamp} ORDER BY \"CHAIN\", \"TS_FROM\";"
    query_text = f"SELECT \"STGRS\", \"LPSupply\", \"TS_TO\", \"CHAIN\", \"POOL\" FROM chain_farmingmodel WHERE ( {chain_join} ) AND \"TS_FROM\" >= {start_timestamp} AND \"TS_TO\" <= {end_timestamp} ORDER BY \"CHAIN\", \"POOL\", \"TS_FROM\";"
    print(query_text)

    query = { "query":  query_text}

    response = requests.post(url, headers=headers, data=json.dumps(query))
    new_result = []
    if response.status_code == 200:
        result = response.json()
        for item in pool_chains:
            pool = item[0]
            chain = item[1]
            for elem in result:
                if elem["POOL"] == pool and elem["CHAIN"] == chain:
                    new_result.append({
                        'STGRS': elem['STGRS'],
                        'LPSupply': elem['LPSupply'],
                        'TS_TO': elem['TS_TO'],
                    })
                    break
    else:
        print("Error: ", response.text)

    print("--------------------")

    print([{'STGRS': x['STGRS'], 'LPSupply': x['LPSupply'], 'TS_TO': x['TS_TO']} for x in result])
    print(new_result)

    df = pd.DataFrame(new_result)
    assert df["STGRS"].to_numpy().shape[0] == df["LPSupply"].to_numpy().shape[0]
    assert df["LPSupply"].to_numpy().shape[0] == df["TS_TO"].to_numpy().shape[0]
    assert df["TS_TO"].to_numpy()[-1] == end_timestamp
    num = df.to_numpy()
    # print(num)

    assert num.shape[0] % len(pool_chains) == 0
    nRows_per_pool = num.shape[0] // len(pool_chains)
    pool_chains = [num[id*nRows_per_pool:(id+1)*nRows_per_pool] for id in range(len(pool_chains))]
    pool_chains = [np.reshape(np.swapaxes(pool, 0, 1), (1, len(("STGRS", "LPSupply", "TS_TO")), -1)) for pool in pool_chains]
    pools_state = np.concatenate(pool_chains, axis=0)
    # print("...pools_state", query_text, result, pools_state)
    return pools_state
