from flask import Flask, jsonify, request
from preprocessing import load_and_clean, validate
from analysis import build_insights

app = Flask(__name__)

df = load_and_clean()
validate(df)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "rows": len(df)})


@app.get("/api/summary")
def summary():
    return jsonify({
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "overall_survival_rate": round(float(df["survived"].mean()), 4)
    })


@app.get("/api/insights")
def insights():
    return jsonify(build_insights(df))


@app.get("/api/passengers")
def passengers():
    result = df.copy()
    sex = request.args.get("sex")
    pclass = request.args.get("pclass", type=int)
    survived = request.args.get("survived", type=int)
    limit = min(request.args.get("limit", default=20, type=int), 100)

    if sex:
        if sex not in {"male", "female"}:
            return jsonify({"error": "sex must be male or female"}), 400
        result = result[result["sex"] == sex]

    if pclass is not None:
        if pclass not in {1, 2, 3}:
            return jsonify({"error": "pclass must be 1, 2, or 3"}), 400
        result = result[result["pclass"] == pclass]

    if survived is not None:
        if survived not in {0, 1}:
            return jsonify({"error": "survived must be 0 or 1"}), 400
        result = result[result["survived"] == survived]

    return jsonify({
        "count": len(result),
        "records": result.head(limit).to_dict("records")
    })


@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "endpoint not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)