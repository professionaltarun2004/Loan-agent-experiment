"""Bayesian belief updates for the synthetic experiment."""


def bayesian_update(priors: dict, likelihoods: dict) -> dict:
    """Return normalized P(state | evidence) using Bayes' rule."""
    joint = {
        state: priors[state] * likelihoods[state]
        for state in priors
    }
    normalizing_constant = sum(joint.values())
    if normalizing_constant == 0:
        raise ValueError("Evidence has zero probability under all states")
    return {
        state: joint[state] / normalizing_constant
        for state in joint
    }

