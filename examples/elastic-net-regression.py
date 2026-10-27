"""Run with Python 3 after installing examples/requirements.txt."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV, KFold

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

def coordinate_descent(Z, yc, lam, rho, tolerance=1e-10, max_iter=50000):
    n, p = Z.shape
    beta = np.zeros(p)
    residual = yc.copy()
    mean_square = (Z * Z).mean(axis=0)
    for iteration in range(max_iter):
        previous = beta.copy()
        for j in range(p):
            residual += Z[:, j] * beta[j]
            z = Z[:, j] @ residual / n
            denominator = mean_square[j] + lam * (1 - rho)
            if denominator <= 0:
                beta[j] = 0
            else:
                beta[j] = (np.sign(z) * max(abs(z) - lam * rho, 0)
                           / denominator)
            residual -= Z[:, j] * beta[j]
        if np.max(np.abs(beta - previous)) < tolerance:
            return beta
    raise RuntimeError("Coordinate descent did not converge")

lam, rho = 0.1, 0.5
beta = coordinate_descent(Z, yc, lam, rho)
fixed = make_pipeline(StandardScaler(), ElasticNet(alpha=lam, l1_ratio=rho,
                                                   tol=1e-10, max_iter=50000))
fixed.fit(X_train, y_train)
np.testing.assert_allclose(y_mean + Z_test @ beta, fixed.predict(X_test), atol=1e-6)
search = GridSearchCV(
    make_pipeline(StandardScaler(), ElasticNet(max_iter=50000)),
    {"elasticnet__alpha": [0.01, 0.1, 1.0], "elasticnet__l1_ratio": [0.2, 0.5, 0.8]},
    scoring="neg_mean_squared_error", cv=KFold(5, shuffle=True, random_state=42)
)
search.fit(X_train, y_train)
pred = search.predict(X_test)
print("Selected parameters:", search.best_params_)

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
