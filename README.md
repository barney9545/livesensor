# Sensor Fault Detection for Air Pressure System (APS) in Scania Trucks

## Project Overview

This repository addresses the problem of detecting failures in the **Air Pressure System (APS)** of Scania trucks, a critical system responsible for essential functions such as braking and gear changes. The goal is to develop a predictive model that can accurately detect faults and minimize the associated costs of false positives (unnecessary repairs) and false negatives (undetected faults leading to breakdowns).

## Problem Statement

In heavy trucks like those produced by Scania, failures in the APS can lead to significant operational disruptions. The challenge is to predict component failures using operational data from various truck systems. The dataset comprises historical sensor data that has been anonymized for proprietary reasons. 

The key challenge is the **imbalance** in the dataset:
- **Positive Class**: Represents trucks with APS component failures (1.67% of the data).
- **Negative Class**: Represents trucks with failures in components unrelated to the APS (98.33% of the data).

### Dataset Description

- **Training Set**: 60,000 instances (1,000 positive class, 59,000 negative class)
- **Test Set**: 16,000 instances
- **Attributes**: 171 anonymized operational features including numerical counters and histograms
- **Missing Data**: Some features contain missing values denoted by 'na'

The operational data includes both numerical and histogram-based variables. Histogram variables are categorized into bins representing ranges of conditions, such as ambient temperature, with different ranges for each bin.

### Cost Considerations

A unique aspect of this problem is that different types of prediction errors have different associated costs:
- **Cost of False Positives (Cost_1)**: $10, represents the cost of an unnecessary inspection.
- **Cost of False Negatives (Cost_2)**: $500, represents the cost of missing a faulty truck, which could result in a breakdown.

The **Total Cost** is calculated as:
```
Total_Cost = Cost_1 * No_False_Positives + Cost_2 * No_False_Negatives
```

The model’s objective is to minimize this total cost by balancing accuracy in predicting both APS-related failures and non-APS-related failures.

## Solution Approach

1. **Data Preprocessing**:  
   - Handle missing values (imputation strategies)
   - Normalize/scale features for improved model performance

2. **Model Selection**:  
   - Use of classification algorithms like Random Forest, XGBoost, and Support Vector Machines, which are known for handling imbalanced datasets.
   - Employ **cost-sensitive learning** techniques to account for the differing costs of false positives and false negatives.

3. **Performance Metrics**:  
   - Since the dataset is highly imbalanced, traditional metrics like accuracy may not be appropriate.
   - We focus on metrics like **Precision**, **Recall**, and especially **F1-score** for the positive class.
   - A custom cost metric, reflecting the overall prediction cost, is also calculated to assess model performance.

4. **Model Evaluation**:  
   - The model is trained to minimize the total prediction cost, ensuring that the cost of undetected faults (false negatives) is significantly reduced without drastically increasing the false positives.

## Conclusion

This project leverages historical operational data from Scania trucks to develop a predictive maintenance solution that minimizes operational costs associated with APS failures. By accurately detecting potential failures, we can avoid both unnecessary repairs and costly breakdowns, improving efficiency and reducing downtime.

## Acknowledgements

This project is based on the APS Failure and Operational Data for Scania Trucks, originally sourced from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/APS+Failure+at+Scania+Trucks).

