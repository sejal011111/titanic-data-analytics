import matplotlib.pyplot as plt
import seaborn as sns
import os

def setup_theme():
    sns.set_theme(style="whitegrid", palette="deep")


def save_plot(name):
    os.makedirs("outputs", exist_ok=True)
    plt.tight_layout()
    plt.savefig(f"outputs/{name}.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_visualizations(df):
    setup_theme()

# Chart 1: Survival Count
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="survived")
    plt.title("Passenger Survival Count")
    plt.xlabel("Survived (0 = No, 1 = Yes)")
    plt.ylabel("Number of Passengers")
    save_plot("survival_count")

# Chart 2: Survival Rate by Sex
    plt.figure(figsize=(6, 4))
    sns.barplot(data=df, x="sex", y="survived", errorbar=None)
    plt.title("Survival Rate by Sex")
    plt.xlabel("Sex")
    plt.ylabel("Survival Rate")
    save_plot("survival_by_sex")

# Chart 3: Survival by Class and Sex
    plt.figure(figsize=(7, 5))
    sns.barplot(data=df, x="pclass", y="survived", hue="sex", errorbar=None)
    plt.title("Survival by Passenger Class and Sex")
    plt.xlabel("Passenger Class")
    plt.ylabel("Survival Rate")
    save_plot("survival_by_class")

# Chart 4: Age Distribution by Survival
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="age", hue="survived", bins=25, multiple="stack", kde=True)
    plt.title("Age Distribution by Survival")
    plt.xlabel("Age")
    plt.ylabel("Number of Passengers")
    save_plot("age_distribution")

# Chart 5: Fare by Class and Survival
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="pclass", y="fare", hue="survived")
    plt.title("Fare by Class and Survival")
    plt.xlabel("Passenger Class")
    plt.ylabel("Fare")
    save_plot("fare_by_class")

# Chart 6: Family Size and Survival
    plt.figure(figsize=(8, 5))
    sns.pointplot(data=df, x="family_size", y="survived", errorbar=None)
    plt.title("Family Size and Survival")
    plt.xlabel("Family Size")
    plt.ylabel("Survival Rate")
    save_plot("family_size_survival")

# Chart 7: Correlation Heatmap
    plt.figure(figsize=(8, 6))
    numeric = df[["survived", "pclass", "age", "sibsp", "parch", "fare", "family_size", "is_alone"]]
    sns.heatmap(numeric.corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Correlation Heatmap")
    save_plot("correlation_heatmap")

    print("All 7 visualizations created successfully in the 'outputs' folder!")


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("data/cleaned_titanic.csv")
    create_visualizations(df)
