"""Run with Python 3 after installing examples/requirements.txt."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import Ridge

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)
X = rng.normal(size=(260, 6))
X[:, 1] = 0.8 * X[:, 0] + 0.2 * X[:, 1]
y = 2 + X @ np.array([2.5, 1.5, 0, 0, -1, 0]) + rng.normal(0, 0.8, 260)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
scaler = StandardScaler().fit(X_train)
Z = scaler.transform(X_train)
Z_test = scaler.transform(X_test)
y_mean = y_train.mean()
yc = y_train - y_mean
n, p = Z.shape

lam = 0.1
beta = np.linalg.solve(Z.T @ Z + n * lam * np.eye(p), Z.T @ yc)
pred = y_mean + Z_test @ beta
pipe = make_pipeline(StandardScaler(), Ridge(alpha=n * lam))
pipe.fit(X_train, y_train)
np.testing.assert_allclose(pred, pipe.predict(X_test), atol=1e-9)
print("Standardized coefficients:", beta)

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
