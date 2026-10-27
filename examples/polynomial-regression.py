"""Run with Python 3 after installing examples/requirements.txt."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, KFold

rng = np.random.default_rng(42)
X = rng.uniform(-2, 2, size=(200, 1))
y = 1 + 0.5 * X[:, 0] + 2 * X[:, 0] ** 2 + rng.normal(0, 0.7, 200)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
pipe = Pipeline([
    ("input_scale", StandardScaler()),
    ("poly", PolynomialFeatures(include_bias=False)),
    ("feature_scale", StandardScaler()),
    ("model", Ridge(alpha=0.01)),
])
search = GridSearchCV(pipe, {"poly__degree": list(range(1, 7))},
                      scoring="neg_mean_squared_error",
                      cv=KFold(5, shuffle=True, random_state=42))
search.fit(X_train, y_train)
pred = search.predict(X_test)
print("Selected degree:", search.best_params_["poly__degree"])

print("Test MAE:", mean_absolute_error(y_test, pred))
print("Test RMSE:", np.sqrt(mean_squared_error(y_test, pred)))
print("Test R2:", r2_score(y_test, pred))

grid = np.linspace(-2, 2, 300).reshape(-1, 1)
plt.scatter(X_test[:, 0], y_test, label="Test observations")
plt.plot(grid[:, 0], search.predict(grid), color="tab:orange", label="Selected polynomial")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.tight_layout()
plt.show()
