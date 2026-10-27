import pandas as pd
import numpy as np

def load_and_clean():
    df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/refs/heads/master/titanic.csv")

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    df = df.drop_duplicates()

    for col in ["age", "fare", "sibsp", "parch"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.loc[(df["age"] < 0) | (df["age"] > 100), "age"] = np.nan

    df.loc[df["fare"] < 0, "fare"] = np.nan

    df["age"] = df.groupby(["pclass", "sex"])["age"].transform(
        lambda x: x.fillna(x.median())
    )
    df["age"] = df["age"].fillna(df["age"].median())

    df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])
    df["embark_town"] = df["embark_town"].fillna(df["embark_town"].mode()[0])

    df["deck"] = df["deck"].astype(object)
    df["deck"] = df["deck"].fillna("Unknown")

    df["fare"] = df.groupby("pclass")["fare"].transform(
        lambda x: x.mask(x <= 0, x.median())
    )
    df["fare"] = df["fare"].fillna(df["fare"].median())

    df = df.drop(columns=["alive", "class"])

    df["family_size"] = df["sibsp"] + df["parch"] + 1
    df["is_alone"] = (df["family_size"] == 1).astype(int)
    df["age_band"] = pd.cut(
        df["age"], bins=[0, 12, 18, 35, 60, 100],
        labels=["Child", "Teen", "Young Adult", "Adult", "Senior"]
    )
    df["fare_band"] = pd.qcut(df["fare"], q=4, labels=["Low", "Medium", "High", "Very High"])

    df = df.drop_duplicates()

    return df

def validate(df):
    """Run assertions to confirm the data is clean and reliable."""
    required = {"survived", "pclass", "sex", "age", "fare", "family_size"}
    assert required.issubset(df.columns), "Required columns missing"
    assert df.duplicated().sum() == 0, "Duplicates remain"
    assert df["survived"].isin([0, 1]).all(), "Invalid target values"
    assert df["pclass"].isin([1, 2, 3]).all(), "Invalid passenger class"
    assert df["age"].between(0, 100).all(), "Age outside valid range"
    assert (df["fare"] > 0).all(), "Fare must be positive"
    assert df[list(required)].isna().sum().sum() == 0, "Critical nulls remain"
    return True


if __name__ == "__main__":
    df = load_and_clean()
    validate(df)
    print("Data loaded and validated successfully!")
    print("Shape:", df.shape)
    df.to_csv("data/cleaned_titanic.csv", index=False)
    print("Saved to data/cleaned_titanic.csv")

