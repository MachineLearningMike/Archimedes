import json
from fastapi import FastAPI

from utils.helper import fetch_pools_data
from utils.models import \
    Optimization_Input, Test_Optimization_Input, Transition_Input

import numpy as np
import datetime
from tools_m1 import *

description = """
Archimedes API
"""

app = FastAPI(
    title="Archimedes",
    description=description,
    version="0.0.1",
    contact={
        "name": "Author",
        "url": "https://example.com",
        "email": "admin@example.com",
    },
)


@app.get("/poolstate")
def portfolio_get(start_timeslot: int, number_timeslots: int):
    return f"GET: start_timeslot={start_timeslot} start_timeslot={number_timeslots}"

@app.post("/optimize")
def optimize(input: Optimization_Input):
    portfolio = []; rewards = []

    try:
        mozaic_total_stake, pool_chains, start_timeslot, number_timeslots, seconds_per_slot = \
            parse_optimization_input(input)
        
        ["arbitrum", "avalanche", "bsc", "polygon"]
        ["FRAX", "USDC", "USDT"]


        # ["FRAX", "arbitrum", "USDC", "polygon", "USDT", "polygon", "USDC", "arbitrum", "USDT", "arbitrum"]

        # ["arbitrum", "FRAX", "arbitrum", "USDC", "arbitrum", "USDT", "polygon", "USDC", "polygon", "USDT"]

        

        if number_timeslots == 1: # analytical optimization, not ML one.
            start_timeslot -= 1

            pools_state = fetch_pools_data(
                pool_chains = pool_chains, 
                start_timestamp = seconds_per_slot * start_timeslot,
                end_timestamp = seconds_per_slot * (start_timeslot + number_timeslots)
            )

            timeslot = 0
            # print("state", pools_state)
            portfolio, rewards = get_optimum_m1_core(mozaic_total_stake, pools_state, timeslot)
            # print("------------", portfolio, mozaic_total_stake)
            assert np.abs(np.sum(portfolio) - mozaic_total_stake) / (mozaic_total_stake + 1e-3) <= 0.0001
            # print("result", mozaic_total_stake, reward, portfolio)

        else: # ML optimzation. To be filled soon.
            pass

    except:
        raise Exception("Error")
        
    return json.dumps(list(portfolio) + list(rewards))


@app.post("/test_optimize")
def test_optimize(input: Test_Optimization_Input):
    portfolio = []; rewards = []

    try:
        mozaic_total_stake, number_pools, number_timeslots, release_rates, rival_stakes = \
            parse_test_optimization_input(input)
        print(mozaic_total_stake)

        if number_pools > 0:
            if number_timeslots == 1: # analytical optimization, not ML one.
                pools_state = np.transpose(np.array( [release_rates, rival_stakes], dtype=np.float64))
                pools_state = np.expand_dims(pools_state, axis=2)

                timeslot = 0
                # print("state", pools_state)
                portfolio, rewards = get_optimum_m1_core(mozaic_total_stake, pools_state, timeslot)
                # print("------------", portfolio, mozaic_total_stake)
                assert np.abs(np.sum(portfolio) - mozaic_total_stake) / (mozaic_total_stake + 1e-3) <= 0.0001
                # print("result", mozaic_total_stake, reward, portfolio)

            else: # ML optimzation. To be filled soon.
                pass

    except:
        raise Exception("Error")
        
    return json.dumps(list(portfolio) + list(rewards))


def parse_optimization_input(input):
    mozaic_total_stake = input.mozaic_total_stake * 1.0
    pool_chains = input.pool_chains
    assert len(pool_chains) % 2 == 0
    nPools = len(pool_chains) // 2
    pool_chains = [ (pool_chains[2*i], pool_chains[2*i+1]) for i in range(nPools) ]
    pool_chains_disordered = list(set(pool_chains))
    assert len(pool_chains_disordered) == nPools

    number_timeslots = int(input.number_timeslots)
    seconds_per_slot = int(input.seconds_per_slot)
    assert seconds_per_slot in [1800, 3600, 7200]

    start_timeslot = int(input.start_timeslot)
    if start_timeslot < 0:
        start_timeslot = int(datetime.utcnow().timestamp() / seconds_per_slot) - (start_timeslot + 1)

    # constraints for the beta version
    assert number_timeslots == 1
    assert seconds_per_slot == 3600

    return mozaic_total_stake, pool_chains, start_timeslot, number_timeslots, seconds_per_slot


def parse_test_optimization_input(input):
    mozaic_total_stake = input.mozaic_total_stake * 1.0

    number_pools = int(input.number_pools)
    number_timeslots = int(input.number_timeslots)
    release_rates = input.release_rates
    rival_stakes = input.rival_stakes

    if number_pools > 0:
        assert len(release_rates) // number_pools == number_timeslots
        assert len(release_rates) % number_pools == 0
        assert len(rival_stakes) // number_pools == number_timeslots
        assert len(rival_stakes) % number_pools == 0
    else:
        assert len(release_rates) == 0
        assert len(rival_stakes) == 0

    return mozaic_total_stake, number_pools, number_timeslots, release_rates, rival_stakes