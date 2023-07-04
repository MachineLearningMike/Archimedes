from typing import List

from pydantic import BaseModel


class Data(BaseModel):

    chain_names: List[str]
    pool_names: List[str]
    mozaic_total_stake: int
    start_timeslot: int
    number_timeslots: int
    seconds_per_slot: int
