def build_insights(df):
    overall = round(df["survived"].mean() * 100, 2)

    by_sex = (df.groupby("sex", as_index=False)["survived"]
              .mean().assign(survival_rate=lambda x: (x["survived"] * 100).round(2))
              .drop(columns="survived"))

    by_class = (df.groupby("pclass", as_index=False)["survived"]
                .mean().assign(survival_rate=lambda x: (x["survived"] * 100).round(2))
                .drop(columns="survived"))

    by_age_band = (df.groupby("age_band", observed=True, as_index=False)["survived"]
                   .mean().assign(survival_rate=lambda x: (x["survived"] * 100).round(2))
                   .drop(columns="survived"))

    by_family = (df.groupby("family_size", as_index=False)["survived"]
                 .agg(passengers="count", survival_rate="mean"))
    by_family["survival_rate"] = (by_family["survival_rate"] * 100).round(2)

    return {
        "overall_survival_rate": overall,
        "by_sex": by_sex.to_dict("records"),
        "by_class": by_class.to_dict("records"),
        "by_age_band": by_age_band.to_dict("records"),
        "by_family_size": by_family.to_dict("records")
    }