"""Run with Python 3 after installing examples/requirements.txt."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
X = rng.normal(size=(240, 3)) * np.array([1, 10, 100])
y = 2 + X @ np.array([2, -0.3, 0.01]) + rng.normal(0, 0.5, 240)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
scaler = StandardScaler().fit(X_train)
Z_train = scaler.transform(X_train)
Z_test = scaler.transform(X_test)
A = np.column_stack([np.ones(len(Z_train)), Z_train])
A_test = np.column_stack([np.ones(len(Z_test)), Z_test])
n = len(A)
hessian = A.T @ A / n
rate = 1 / np.linalg.eigvalsh(hessian).max()
theta = np.zeros(A.shape[1])
losses = []
for iteration in range(10000):
    error = A @ theta - y_train
    losses.append(0.5 * np.mean(error ** 2))
    gradient = A.T @ error / n
    if np.linalg.norm(gradient) < 1e-9:
        break
    theta -= rate * gradient
else:
    raise RuntimeError("Gradient descent did not converge")
exact = np.linalg.lstsq(A, y_train, rcond=None)[0]
np.testing.assert_allclose(theta, exact, atol=1e-7)
pred = A_test @ theta
model = LinearRegression().fit(Z_train, y_train)
np.testing.assert_allclose(pred, model.predict(Z_test), atol=1e-7)
assert np.all(np.diff(losses) <= 1e-10)
print("Learning rate:", rate, "Updates:", iteration)

print("Test MAE:", mean_absolute_error(y_test, pred))
print("Test RMSE:", np.sqrt(mean_squared_error(y_test, pred)))
print("Test R2:", r2_score(y_test, pred))

plt.plot(losses)
plt.xlabel("Batch gradient update")
plt.ylabel("Training half-MSE")
plt.title("Convergence of the stated objective")
plt.tight_layout()
plt.show()
