from typing import List

from pydantic import BaseModel

class Optimization_Input(BaseModel):
    mozaic_total_stake: float
    pool_chains: List[str]
    start_timeslot: int
    number_timeslots: int
    seconds_per_slot: int


class Test_Optimization_Input(BaseModel):
    mozaic_total_stake: float
    number_pools: int
    number_timeslots: int
    release_rates: List[float]
    rival_stakes: List[float]


class Transition_Input(BaseModel):
    number_pools: int
    mozaic_total_stake: int
    number_timeslots: int
    seconds_per_slot: int
