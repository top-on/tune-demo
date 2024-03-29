#!/usr/bin/env python
# Example for simple grid search.
# See: https://towardsdatascience.com/fast-hyperparameter-tuning-at-scale-d428223b081c

# %%
from ray import tune

from tune_demo.train import get_iris_data, rf_cv


# %%
def eval_model(config):
    X, y = get_iris_data()
    for i in range(3):
        acc = rf_cv(config, X, y)
        tune.track.log(acc=acc)


# %%
analysis = tune.run(
    eval_model,
    config={
        "max_depth": tune.grid_search([1, 4, 20]),
        "n_estimators": tune.grid_search([10, 100, 1000]),
    },
)

print("Best config: ", analysis.get_best_config(metric="acc"))
# config = {'max_depth': 4, 'n_estimators': 1000}

# Get a dataframe for analyzing trial results.
print(analysis.dataframe())

# %%
