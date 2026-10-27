"""Run with Python 3 after installing examples/requirements.txt."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
X = rng.normal(size=(220, 2))
y = 2 + X @ np.array([2.0, -1.0]) + rng.normal(0, 1, 220)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_test)
residual = y_test - pred
mae = np.abs(residual).mean()
mse = (residual ** 2).mean()
sst = ((y_test - y_test.mean()) ** 2).sum()
r2 = 1 - (residual ** 2).sum() / sst if sst > 0 else np.nan
np.testing.assert_allclose(mae, mean_absolute_error(y_test, pred))
np.testing.assert_allclose(mse, mean_squared_error(y_test, pred))
np.testing.assert_allclose(r2, r2_score(y_test, pred))
assert mae <= np.sqrt(mse) + 1e-12
print("NumPy MAE, MSE, RMSE, R2:", mae, mse, np.sqrt(mse), r2)

plt.scatter(y_test, pred, alpha=0.7)
limits = [min(y_test.min(), pred.min()), max(y_test.max(), pred.max())]
plt.plot(limits, limits, "k--", label="Perfect prediction")
plt.xlabel("Actual target")
plt.ylabel("Predicted target")
plt.legend()
plt.tight_layout()
plt.show()
