def grade(state, action, reward):
    return reward if 0 < reward < 1 else 0.5
