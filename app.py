from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:

        features = [float(x) for x in request.form.values()]

        final_features = np.array(features).reshape(1, -1)

        scaled_output = model.predict(final_features)[0]

        original_output = round(scaler.inverse_transform([[scaled_output]])[0][0])

        return render_template(
            "index.html", prediction_text=f"The prediction is: {original_output}"
        )

    except Exception as e:
        return render_template("index.html", prediction_text=f"Error occurred: {e}")


@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:

        data = request.get_json(force=True)

        features = np.array(data["features"]).reshape(1, -1)

        scaled_output = model.predict(features)[0]

        original_output = scaler.inverse_transform([[scaled_output]])[0][0]

        return jsonify({"prediction": original_output})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
