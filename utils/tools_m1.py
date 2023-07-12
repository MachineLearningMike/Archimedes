import numpy as np
from datetime import datetime, timedelta

dimRewardRate: int = 0
dimRivalStake: int = 1
dimMozaicStake: int = 2

def get_reward_vector(states, portfolio, timeslot):
    return (states[:, dimRewardRate, timeslot] * portfolio[:]) / (states[:, dimRivalStake, timeslot] + portfolio[:] + 1e-30)

def reward_function(states, portfolio):
    loss = 0.0
    for t in range(states.shape[2]):
        loss += np.sum(get_reward_vector(states, portfolio, t), axis=None)
    return loss

def get_unlimited_optimum_m1(mLpTotal, states):
    fertility = np.sqrt(states[:, dimRewardRate] * states[:, dimRivalStake])
    total_fertility = np.sum(fertility)
    supply_total = mLpTotal + np.sum(states[:, dimRivalStake])
    c = np.square( total_fertility / (supply_total + 1e-9) )
    unlimited_mLp = fertility / (total_fertility + 1e-20) * supply_total - states[:, dimRivalStake]
    return unlimited_mLp

def get_optimum_m1(totalStates, timeslot, mode=2): # Keep the default mode 1.
    # totalState = ( pools, 3 = (Relsese, public LP supply, Mozaic LP supply), timeslot)
    mozaic_total_stake = np.sum(totalStates[:, dimMozaicStake, timeslot]) # total mozaic stake across pools.
    return get_optimum_m1_core(mozaic_total_stake, totalStates, timeslot, mode=mode)

def get_optimum_m1_core(mozaic_total_stake, totalStates, timeslot, mode=2):
    now = datetime.now()
    expiry = datetime(2023,10,31)    # ------------------------ Notice the expiry date.

    if now > expiry:
        portfolio = np.zeros( (totalStates.shape[0],), dtype=totalStates.dtype )
        portfolio[0] = mozaic_total_stake
        reward = 0.0
    else:
        states = totalStates[:, :, timeslot]
        portfolio = np.ones( (totalStates.shape[0],), dtype=totalStates.dtype )

        while True:
            pIndices = portfolio > 0    # pick up positive dimensions
            if not np.any(pIndices): break  # no positive dimensions, break

            states = totalStates[pIndices, :, timeslot]
            _mLp = get_unlimited_optimum_m1(mozaic_total_stake, states)  # allocate total to cared pools

            portfolio[pIndices] = _mLp

            if np.min(_mLp) >= 0: break

        portfolio[portfolio < 0] = 0    # kill zer0-or-negative values now.
        reward_vector = get_reward_vector(totalStates, portfolio, timeslot)

    return portfolio, reward_vector
