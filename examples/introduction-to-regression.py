"""Run with Python 3 after installing examples/requirements.txt."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
X = rng.uniform(0, 10, size=(240, 1))
y = 3 + 2 * X[:, 0] + rng.normal(0, 2, 240)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
for name, model in [("Mean baseline", DummyRegressor()),
                    ("Linear model", LinearRegression())]:
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(name, "MAE", mean_absolute_error(y_test, pred),
          "RMSE", np.sqrt(mean_squared_error(y_test, pred)),
          "R2", r2_score(y_test, pred))
plt.scatter(X_test[:, 0], y_test, label="Test observations")
order = np.argsort(X_test[:, 0])
plt.plot(X_test[order, 0], pred[order], color="tab:orange", label="Linear prediction")
plt.xlabel("Input x")
plt.ylabel("Target y")
plt.legend()
plt.tight_layout()
plt.show()
