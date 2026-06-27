# =====================================================
#        HYPOTHESIS TESTING - ACCIDENT PROJECT
# =====================================================

import pandas as pd

from scipy.stats import chi2_contingency

# =====================================================
# LOAD DATASET
# =====================================================

df = pd.read_csv("cleaned_accident_data.csv")

# =====================================================
# CLEAN TEXT
# =====================================================

for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].astype(str).str.upper().str.strip()

# =====================================================
# FUNCTION FOR CHI-SQUARE TEST
# =====================================================

def chi_square_test(feature, target):

    print("\n================================================")
    print(f"TEST: {feature} VS {target}")
    print("================================================")

    # Create contingency table
    table = pd.crosstab(df[feature], df[target])

    # Apply Chi-Square
    chi2, p, dof, expected = chi2_contingency(table)

    print(f"\nChi-Square Value : {round(chi2,2)}")
    print(f"P-Value          : {p}")

    # Result
    if p < 0.05:

        print("\nRESULT:")
        print(f"✔ Significant relationship found between")
        print(f"'{feature}' and '{target}'")

    else:

        print("\nRESULT:")
        print(f"✘ No significant relationship found between")
        print(f"'{feature}' and '{target}'")

# =====================================================
# HYPOTHESIS TESTS
# =====================================================

# 1
chi_square_test(
    'Weather',
    'Injury Severity'
)

# 2
chi_square_test(
    'Light',
    'Injury Severity'
)

# 3
chi_square_test(
    'Driver Substance Abuse',
    'Injury Severity'
)

# 4
chi_square_test(
    'Collision Type',
    'Vehicle Damage Extent'
)

# 5
chi_square_test(
    'Driver Distracted By',
    'Injury Severity'
)

# =====================================================

print("\n================================================")
print("HYPOTHESIS TESTING COMPLETED")
print("================================================")