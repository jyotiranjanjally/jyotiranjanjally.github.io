---
author: Jyoti Ranjan Jally
pubDatetime: 2024-07-02T12:00:00Z
title: "Understanding Linear Regression: Theory, Equations, and Python Code with Visualization"
description: "A detailed, all-in-one guide to linear regression covering the theory, mathematical equations, Python code, and visualizations in one page."
tags:
  - machine-learning
  - regression
  - python
  - data-science
draft: false
---

# Understanding Linear Regression: Theory, Equations, and Python Code with Visualization

Linear regression is one of the most fundamental algorithms in statistics and machine learning. It helps us understand the relationship between a dependent variable and one or more independent variables by fitting a straight line through the data.

This article provides a complete overview on one page — including the math behind it, Python code, and visualization.

---

## What is Linear Regression?

Linear regression models the relationship between variables by fitting a linear equation to observed data.  

When we have one independent variable, it's called **simple linear regression**. With multiple independent variables, it's called **multiple linear regression**.

---

## Mathematical Equation

For simple linear regression, the model can be described by:

\[
y = \beta_0 + \beta_1 x + \epsilon
\]

Where:  
- \(y\): dependent variable (target).  
- \(x\): independent variable (feature).  
- \(\beta_0\): intercept.  
- \(\beta_1\): slope (coefficient).  
- \(\epsilon\): error term.

The goal is to find \(\beta_0\) and \(\beta_1\) that minimize the **mean squared error**.

---

## Loss Function

The **Mean Squared Error (MSE)** is commonly used as the loss function:

\[
J(\beta_0, \beta_1) = \frac{1}{n}\sum_{i=1}^{n}(y_i - (\beta_0 + \beta_1 x_i))^2
\]

Where \(n\) is the number of data points.

---

## Python Implementation

Below is a complete, runnable example using `scikit-learn` and `matplotlib`.

### Import Libraries

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
