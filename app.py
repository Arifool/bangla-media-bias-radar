from flask import Flask, render_template, request, redirect, url_for
from model import predict_bias

app = Flask(__name__)

@app.route("/")
def root():
    return redirect(url_for("analyzer"))

@app.route("/analyzer", methods=["GET", "POST"])
def analyzer():
    result = None
    if request.method == "POST":
        headline = request.form.get("headline", "").strip()
        channel  = request.form.get("channel", "").strip()
        date     = request.form.get("date", "").strip()

        if headline:
            label, color, confidence, prob_list = predict_bias(headline)
            result = {
                "headline":   headline,
                "channel":    channel,
                "date":       date,
                "label":      label,
                "color":      color,
                "confidence": confidence,
                "probs": {
                    "pro":     prob_list[0],
                    "neutral": prob_list[1],
                    "anti":    prob_list[2],
                }
            }

    return render_template("analyzer.html", active="analyzer", result=result)

@app.route("/news")
def news():
    channels = [
        {"name": "প্রথম আলো (Prothom Alo)",  "url": "https://www.prothomalo.com"},
        {"name": "দৈনিক সমকাল (Somokal)",    "url": "https://www.samakal.com"},
        {"name": "যুগান্তর (Jugantor)",        "url": "https://www.jugantor.com"},
        {"name": "যমুনা টিভি (Jamuna TV)",     "url": "https://www.jamuna.tv"},
        {"name": "সময় টিভি (Somoy TV)",       "url": "https://www.somoynews.tv"},
        {"name": "ইত্তেফাক (Ittefaq)",         "url": "https://www.ittefaq.com.bd"},
        {"name": "ডেইলি স্টার (Daily Star)",   "url": "https://www.thedailystar.net"},
    ]
    return render_template("news.html", active="news", channels=channels)

@app.route("/methodology")
def methodology():
    return render_template("methodology.html", active="methodology")

@app.route("/ethics")
def ethics():
    return render_template("ethics.html", active="ethics")

if __name__ == "__main__":
    print("Starting Bangla Media Bias Radar...")
    app.run(debug=True, host="127.0.0.1", port=5000)