"""Run with Python 3 after installing examples/requirements.txt."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
X = rng.uniform(-2, 2, size=(300, 1))
noise_scale = 0.2 + 0.5 * np.abs(X[:, 0])
y = 1 + 2 * X[:, 0] + X[:, 0] ** 2 + rng.normal(size=300) * noise_scale
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_test)
residual = y_test - pred
A = np.column_stack([np.ones(len(X_train)), X_train])
Q, _ = np.linalg.qr(A, mode="reduced")
leverage = (Q ** 2).sum(axis=1)
np.testing.assert_allclose(leverage.sum(), A.shape[1], atol=1e-10)
print("Training leverage range:", leverage.min(), leverage.max())

print("Test MAE:", mean_absolute_error(y_test, pred))
print("Test RMSE:", np.sqrt(mean_squared_error(y_test, pred)))
print("Test R2:", r2_score(y_test, pred))

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(pred, residual, alpha=0.7)
axes[0].axhline(0, color="black", linestyle="--")
axes[0].set(xlabel="Fitted value on test rows", ylabel="Test residual")
axes[1].scatter(y_test, pred, alpha=0.7)
limits = [min(y_test.min(), pred.min()), max(y_test.max(), pred.max())]
axes[1].plot(limits, limits, "k--")
axes[1].set(xlabel="Actual target", ylabel="Predicted target")
fig.tight_layout()
plt.show()
