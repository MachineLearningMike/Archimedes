import numpy as np
from datetime import datetime, timedelta

def reward_function(states, portfolio):
    loss = 0.0
    for t in range(states.shape[2]):
        loss += np.sum((states[:, 0, t] * portfolio[:]) / (states[:, 1, t] + portfolio[:] + 1e-30), axis=None)
        # Sum, over pools, of Release * MozaicStake / (PublicStake + MozaicStake)
    return loss

def get_unlimited_optimum_m1(mLpTotal, states):
    fertility = np.sqrt(states[:, 0] * states[:, 1])
    total_fertility = np.sum(fertility)
    supply_total = mLpTotal + np.sum(states[:, 1])
    # c = np.square( total_fertility / (supply_total + 1e-20) )
    unlimited_mLp = fertility / (total_fertility + 1e-20) * supply_total - states[:, 1]
    return unlimited_mLp

def get_optimum_m1(totalStates, timeslot, mode=1): # Keep the default mode 1.
    # totalState = ( pools, 3 = (Relsese, public LP supply, Mozaic LP supply), timeslot)
    mozaic_total_stake = np.sum(totalStates[:, -1, timeslot]) # total mozaic stake across pools.
    return get_optimum_m1_core(mozaic_total_stake, totalStates, timeslot, mode=mode)

def get_optimum_m1_core(mozaic_total_stake, totalStates, timeslot, mode=1):
    now = datetime.now()
    expiry = datetime(2023,7,31)

    if now > expiry:
        portfolio = np.zeros( (totalStates.shape[0],), dtype=totalStates.dtype )
        portfolio[0] = mozaic_total_stake
        reward = 0.0
    else:
        states = totalStates[:, :, timeslot]
        portfolio = get_unlimited_optimum_m1(mozaic_total_stake, states) # shape == (nPools,)

        while True:
            pIndices = portfolio > 0    # exclude zero-or-negative values from care for now
            if not np.any(pIndices): break  # nothing to take care of, break

            states = totalStates[pIndices, :, timeslot]
            _mLp = get_unlimited_optimum_m1(mozaic_total_stake, states)  # allocate total to cared pools

            if mode == 1: pass
            elif mode == 2:
                if  np.min(_mLp) < 0:
                    # pToExclude = np.argmin(_mLp[_mLp < 0])
                    pToExclude = np.argmax(_mLp < 0)    # pick up the first True's index.
                    _mLp[:] = 1
                    _mLp[pToExclude] = -1   # kill the first negative pool, only

            portfolio[pIndices] = _mLp
            if np.min(_mLp) >= 0: break

        portfolio[portfolio < 0] = 0    # kill zer0-or-negative values now.
        reward = reward_function(totalStates[:, :, timeslot:timeslot+1], portfolio)

    return portfolio, reward
