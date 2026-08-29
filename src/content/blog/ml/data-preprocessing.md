---
author: Jyoti Ranjan Jally
pubDatetime: 2026-08-29T10:00:00Z
title: "Data Preprocessing for Machine Learning: Cleaning, Theory, Mathematics, and Python"
description: "A practical guide to data preprocessing for machine learning: missing values, duplicates, incorrect values, outliers, inconsistent formats, mathematical foundations, and Python implementation."
draft: false
featured: true
tags:
  - machine-learning
  - data-preprocessing
  - data-cleaning
  - python
  - data-science
---

# Phase 2: Data Preprocessing for Machine Learning

In real-world machine learning, the quality of the input data often has more impact than the choice between two capable algorithms. A sophisticated model trained on incomplete, duplicated, incorrectly typed, or inconsistent data can produce unreliable results. Data preprocessing is the disciplined process of turning raw observations into a trustworthy dataset for analysis and modelling.

This phase covers five essential data-cleaning problems:

- Missing values
- Duplicate records
- Incorrect values
- Outliers
- Inconsistent formats

The goal is not to make the dataset look perfect. The goal is to make every transformation explainable, reproducible, and appropriate for the business problem.

---

## 1. A Reproducible Preprocessing Workflow

Before changing any values, preserve the source data and record what changes are made. A dependable workflow is:

1. Profile the data: shape, types, missingness, ranges, and category values.
2. Define validation rules with domain knowledge.
3. Split data into training and test sets before learning statistics such as means or medians.
4. Fit preprocessing steps on the training data only.
5. Apply the same fitted transformations to validation, test, and production data.

The fourth step prevents **data leakage**. For example, calculating a median using the full dataset lets information from the test set influence training-time decisions and can make evaluation overly optimistic.

---

## 2. Missing Values

A missing value means an observation is unavailable. It is commonly represented by `NaN`, `None`, an empty string, or a sentinel such as `"N/A"`, `"unknown"`, or `-999`.

### 2.1 Why values are missing matters

The mechanism behind missingness determines whether a simple imputation is reasonable.

- **MCAR — Missing Completely At Random:** missingness is unrelated to observed or unobserved values. Example: a random system outage.
- **MAR — Missing At Random:** missingness depends on other observed variables. Example: income is more frequently missing for a particular age group.
- **MNAR — Missing Not At Random:** missingness depends on the missing value itself. Example: people with high income may be less likely to report income.

MCAR is the easiest case. MAR often benefits from feature-based imputation. MNAR may require a missingness indicator, domain investigation, or a separate modelling assumption.

### 2.2 Common strategies

**Delete rows or columns** when missingness is small, random, and does not remove an important group. Avoid this if it meaningfully reduces data or introduces selection bias.

**Simple imputation** replaces a missing numeric value with a summary statistic:

\[
\tilde{x}_{j} = \operatorname{median}\{x_{1j}, x*{2j}, \ldots, x*{nj}\}
\]

The median is robust to extreme values. For a roughly symmetric feature without influential outliers, the mean is also common:

\[
\bar{x}_{j} = \frac{1}{n_j}\sum_{i \in O*j}x*{ij}
\]

where \(O_j\) is the set of rows where feature \(j\) is observed, and \(n_j = |O_j|\).

For categorical features, use the mode or a dedicated category such as `"Missing"`. Adding an indicator can preserve useful information:

\[
m*{ij} =
\begin{cases}
1 & \text{if } x*{ij} \text{ is missing} \\
0 & \text{otherwise}
\end{cases}
\]

### Python: inspect and impute missing data

```python
import pandas as pd
from sklearn.impute import SimpleImputer

df = pd.read_csv("customers.csv")

# Standardise common text representations before measuring missingness.
missing_tokens = ["", "N/A", "NA", "unknown", "?"]
df = df.replace(missing_tokens, pd.NA)

print(df.isna().sum().sort_values(ascending=False))
print((df.isna().mean() * 100).round(2))  # percentage missing per column

# Keep whether income was originally missing.
df["income_was_missing"] = df["income"].isna().astype(int)

# Median for a skewed numeric feature; most-frequent value for a category.
df[["income"]] = SimpleImputer(strategy="median").fit_transform(df[["income"]])
df[["city"]] = SimpleImputer(strategy="most_frequent").fit_transform(df[["city"]])
```

---

## 3. Duplicate Records

Duplicates can be exact copies or repeated entities with slightly different values. They may result from repeated data entry, duplicate imports, retry logic, or joins that multiply rows unexpectedly.

### 3.1 Exact versus business-key duplicates

An **exact duplicate** has identical values in every column. A **business-key duplicate** represents the same entity according to a meaningful identifier, such as `customer_id`, `transaction_id`, or a combination of email and event timestamp.

Do not remove repeated records blindly. Two purchases by the same customer are legitimate; two rows with the same transaction ID may not be.

If \(D\) is the number of duplicated rows under a chosen key and \(N\) is the total number of rows, the duplicate rate is:

\[
\text{Duplicate rate} = \frac{D}{N} \times 100\%
\]

### Python: identify and remove duplicates

```python
# Exact duplicates across all columns.
print("Exact duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()

# Duplicate business events. Keep the newest record after sorting.
df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce", utc=True)
duplicate_events = df[df.duplicated(subset=["customer_id", "event_time"], keep=False)]

df = (
    df.sort_values("updated_at")
      .drop_duplicates(subset=["customer_id", "event_time"], keep="last")
)
```

---

## 4. Incorrect Values

Incorrect values violate what is possible or expected for a feature. Examples include a negative age, an invalid email address, a revenue field stored as text, or a future date in historical data.

### 4.1 Validation rules

Use rules based on data types, ranges, allowed categories, cross-field relationships, and time.

- **Range rule:** \(0 \leq \text{age} \leq 120\)
- **Set-membership rule:** `country` belongs to an approved ISO-code list.
- **Relational rule:** \(\text{end_date} \geq \text{start_date}\)
- **Type rule:** `quantity` is a non-negative integer.

For a numeric feature \(x\), a simple range constraint is:

\[
L \leq x_i \leq U
\]

Values outside \([L, U]\) are not automatically outliers; they are invalid only when the domain says they are impossible. Prefer changing them to missing values and investigating, rather than silently clipping or deleting them.

### Python: validate values

```python
import numpy as np

# Coerce malformed text to missing values rather than raising an error.
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

# Domain-invalid values become missing, ready for a documented imputation rule.
df.loc[~df["age"].between(0, 120), "age"] = np.nan
df.loc[df["revenue"] < 0, "revenue"] = np.nan

allowed_statuses = {"active", "inactive", "pending"}
invalid_status = ~df["status"].isin(allowed_statuses)
df.loc[invalid_status, "status"] = pd.NA

# A cross-field validation check.
df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")
invalid_date_order = df["end_date"] < df["start_date"]
print("Rows with an invalid date order:", invalid_date_order.sum())
```

---

## 5. Outliers

An outlier is an observation that is unusually distant from most other observations. It may be a data-entry error, a rare but legitimate event, or an important signal such as fraud. Treating every outlier as bad data is a mistake.

### 5.1 Z-score method

For a feature with mean \(\mu\) and standard deviation \(\sigma\), the z-score of \(x_i\) is:

\[
z_i = \frac{x_i - \mu}{\sigma}
\]

A common heuristic flags values where \(|z_i| > 3\). This assumes a roughly normal distribution, so it is less reliable for skewed features such as income or transaction amount.

### 5.2 Interquartile range method

The IQR method is more robust because it relies on quartiles:

\[
\operatorname{IQR} = Q_3 - Q_1
\]

Using multiplier \(k = 1.5\), the usual fences are:

\[
\text{Lower fence} = Q_1 - k \cdot \operatorname{IQR}
\]

\[
\text{Upper fence} = Q_3 + k \cdot \operatorname{IQR}
\]

An observation outside these fences is a candidate for review, not an automatic deletion.

### Python: detect and cap outliers with IQR

```python
def iqr_bounds(series: pd.Series, multiplier: float = 1.5) -> tuple[float, float]:
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - multiplier * iqr, q3 + multiplier * iqr

lower, upper = iqr_bounds(df["revenue"].dropna())
outlier_mask = ~df["revenue"].between(lower, upper)
print("Potential revenue outliers:", outlier_mask.sum())

# Cap only after confirming that extreme values should not be preserved.
df["revenue_capped"] = df["revenue"].clip(lower=lower, upper=upper)
```

Alternative responses include correcting a known data error, applying `log1p` to a heavily skewed positive feature, using robust models, or retaining the value because it is business-critical.

---

## 6. Inconsistent Formats

The same concept can appear in incompatible forms: `"Mumbai"`, `"mumbai"`, and `" MUMBAI "`; dates in several locale formats; currencies with symbols; or phone numbers with varying punctuation. Inconsistent formats create false categories and prevent reliable joins, aggregation, and feature engineering.

### 6.1 Standardisation principles

- Trim leading and trailing whitespace.
- Apply a consistent case for categorical values.
- Parse dates into a single datetime type and timezone.
- Store amounts as numeric values plus an explicit currency code.
- Keep raw columns when standardisation is irreversible or uncertain.

### Python: standardise text, dates, and currency

```python
# Preserve the original value when auditability matters.
df["city_raw"] = df["city"]
df["city"] = (
    df["city"].astype("string")
      .str.strip()
      .str.replace(r"\s+", " ", regex=True)
      .str.title()
)

# Parse known date patterns explicitly. Use dayfirst only if the source requires it.
df["signup_date"] = pd.to_datetime(
    df["signup_date"], errors="coerce", dayfirst=True, utc=True
)

# Convert a currency string such as "$1,250.50" to a number.
df["amount"] = (
    df["amount"].astype("string")
      .str.replace(r"[^0-9.-]", "", regex=True)
      .pipe(pd.to_numeric, errors="coerce")
)
```

---

## 7. A Train-Safe Preprocessing Pipeline

For model training, use a pipeline so preprocessing is fitted only on training data and applied consistently later.

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

target = "churned"
numeric_features = ["age", "income", "revenue_capped"]
categorical_features = ["city", "status"]

X = df[numeric_features + categorical_features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features),
])

X_train_ready = preprocessor.fit_transform(X_train)
X_test_ready = preprocessor.transform(X_test)  # never fit on test data
```

For standardisation, `StandardScaler` transforms a feature as:

\[
x*i^{\prime} = \frac{x_i - \mu*{\text{train}}}{\sigma\_{\text{train}}}
\]

The training-set mean and standard deviation are deliberately reused for the test set and later predictions.

---

## 8. Preprocessing Checklist

Before training a model, confirm that you can answer these questions:

- Which columns have missing values, and why might they be missing?
- Which duplicate definition reflects the business entity or event?
- Which domain rules identify incorrect values?
- Are unusual values errors, rare legitimate events, or the signal of interest?
- Are categories, dates, units, and currencies represented consistently?
- Was every learned transformation fitted only on training data?
- Can another person reproduce the cleaning steps from source data?

## Conclusion

Data preprocessing is not a single command or a one-time cleanup. It is a series of reasoned decisions that protect data quality, reduce leakage, and make model behaviour more trustworthy. When the data is well understood and transformations are reproducible, model selection becomes a much more meaningful next step.
