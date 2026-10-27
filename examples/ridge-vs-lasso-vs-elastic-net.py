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

rng = np.random.default_rng(42)
X = rng.normal(size=(300, 12))
X[:, 1] = 0.9 * X[:, 0] + 0.1 * X[:, 1]
y = 3 + X @ np.array([2, 2, -1, 0.5, 0, 0, 0, 0, 0, 0, 0, 0]) + rng.normal(0, 1, 300)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
pipe = Pipeline([("scale", StandardScaler()), ("model", Ridge())])

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

baseline = DummyRegressor().fit(X_train, y_train)
print("Baseline test RMSE:", np.sqrt(mean_squared_error(y_test, baseline.predict(X_test))))

print("Test MAE:", mean_absolute_error(y_test, pred))
print("Test RMSE:", np.sqrt(mean_squared_error(y_test, pred)))
print("Test R2:", r2_score(y_test, pred))

plt.scatter(y_test, pred, alpha=0.7)
limits = [min(y_test.min(), pred.min()), max(y_test.max(), pred.max())]
plt.plot(limits, limits, "k--", label="Perfect prediction")
plt.xlabel("Actual target")
plt.ylabel("Predicted target")
plt.legend()
plt.tight_layout()
plt.show()
