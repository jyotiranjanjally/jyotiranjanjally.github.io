"""Run with Python 3 after installing examples/requirements.txt."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
X = rng.uniform(-3, 3, size=(200, 1))
y = 1.2 + 2.5 * X[:, 0] + rng.normal(0, 0.8, 200)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
x = X_train[:, 0]
xc = x - x.mean()
yc = y_train - y_train.mean()
denominator = xc @ xc
if denominator <= 0:
    raise ValueError("A nonconstant feature is required")
slope = (xc @ yc) / denominator
intercept = y_train.mean() - slope * x.mean()
pred = intercept + slope * X_test[:, 0]
model = LinearRegression().fit(X_train, y_train)
np.testing.assert_allclose(pred, model.predict(X_test), atol=1e-10)
print("Intercept and slope:", intercept, slope)

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
