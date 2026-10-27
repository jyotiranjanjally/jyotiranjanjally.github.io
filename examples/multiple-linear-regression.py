"""Run with Python 3 after installing examples/requirements.txt."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
X = rng.normal(size=(240, 3))
y = 1 + X @ np.array([2.0, -1.0, 0.5]) + rng.normal(0, 0.4, 240)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
A_train = np.column_stack([np.ones(len(X_train)), X_train])
A_test = np.column_stack([np.ones(len(X_test)), X_test])
beta, residual_sums, rank, singular_values = np.linalg.lstsq(
    A_train, y_train, rcond=None
)
pred = A_test @ beta
model = LinearRegression().fit(X_train, y_train)
np.testing.assert_allclose(pred, model.predict(X_test), atol=1e-10)
np.testing.assert_allclose(A_train.T @ (y_train - A_train @ beta), 0, atol=1e-9)
print("Coefficients including intercept:", beta)
print("Rank:", rank, "Singular values:", singular_values)

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
