import json
from fastapi import FastAPI

from utils.helper import fetch_pools_data
from utils.models import Data

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


@app.get("/portfolio")
def portfolio_get(start_timeslot: int, number_timeslots: int):
    return f"GET: start_timeslot={start_timeslot} start_timeslot={number_timeslots}"

@app.post("/portfolio")
def portfolio(data: Data):
    chain_names = data.chain_names
    pool_names = data.pool_names
    assert len(chain_names) == len(pool_names)
    pools = zip(chain_names, pool_names)
    pools = list(set(pools))
    assert len(chain_names) == len(pools)

    mozaic_total_stake = data.mozaic_total_stake
    number_timeslots = data.number_timeslots
    seconds_per_slot = data.seconds_per_slot
    assert seconds_per_slot in [1800, 3600, 7200]

    start_timeslot = data.start_timeslot
    if start_timeslot < 0:
        ct = datetime.utcnow()
        start_timeslot = int(ct.timestamp() / seconds_per_slot)

    # constraints for the beta version
    assert number_timeslots == 1
    assert seconds_per_slot == 3600

    portfolio = None; rewards = None



        
    return json.dumps(list(portfolio)) #, json.dumps(list(rewards))
