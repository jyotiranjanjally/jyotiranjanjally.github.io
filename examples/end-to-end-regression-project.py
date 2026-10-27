"""Run with Python 3 after installing examples/requirements.txt."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import GridSearchCV, KFold
import pandas as pd
import sklearn
from sklearn.datasets import load_diabetes
from sklearn.impute import SimpleImputer

print("Versions:", "numpy", np.__version__, "pandas", pd.__version__,
      "scikit-learn", sklearn.__version__)
data = load_diabetes(as_frame=True, scaled=False)
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Training/test shapes:", X_train.shape, X_test.shape)
print("Training missing values:", X_train.isna().sum().to_dict())
print("Training target summary:", y_train.describe().to_dict())
pipe = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
    ("model", Ridge()),
])

# These are library alpha values, not identical normalized penalties.
param_grid = [
    {"model": [LinearRegression()]},
    {"model": [Ridge()], "model__alpha": [0.1, 1, 10, 100, 1000]},
    {"model": [Lasso(max_iter=50000)], "model__alpha": [0.01, 0.1, 1, 10]},
    {"model": [ElasticNet(max_iter=50000)],
     "model__alpha": [0.01, 0.1, 1, 10], "model__l1_ratio": [0.2, 0.5, 0.8]},
]
search = GridSearchCV(pipe, param_grid, scoring="neg_mean_squared_error",
                      cv=KFold(5, shuffle=True, random_state=42), n_jobs=1)
search.fit(X_train, y_train)
pred = search.predict(X_test)
print("Selected configuration:", search.best_params_)
print("CV RMSE (sqrt of mean fold MSE):", np.sqrt(-search.best_score_))

baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
rows = []
for name, predictions in [("Training-mean baseline", baseline.predict(X_test)),
                          ("Selected pipeline", pred)]:
    rows.append({"model": name, "MAE": mean_absolute_error(y_test, predictions),
                 "RMSE": np.sqrt(mean_squared_error(y_test, predictions)),
                 "R2": r2_score(y_test, predictions)})
print(pd.DataFrame(rows).to_string(index=False))
coefficients = search.best_estimator_.named_steps["model"].coef_
print(pd.Series(coefficients, index=X.columns, name="Standardized coefficient"))
assert np.isfinite(pred).all()
assert len(pred) == len(y_test)
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].scatter(y_test, pred, alpha=0.7)
limits = [min(y_test.min(), pred.min()), max(y_test.max(), pred.max())]
axes[0].plot(limits, limits, "k--")
axes[0].set(xlabel="Actual progression response", ylabel="Predicted response")
axes[1].scatter(pred, y_test - pred, alpha=0.7)
axes[1].axhline(0, color="black", linestyle="--")
axes[1].set(xlabel="Predicted response", ylabel="Observed minus predicted")
fig.tight_layout()
plt.show()
