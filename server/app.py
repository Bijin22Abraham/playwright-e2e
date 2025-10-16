from flask import Flask, jsonify, render_template_string, send_file
app = Flask(__name__)

LOGIN_HTML = "<html><body><h1>Dashboard</h1></body></html>"
ANALYZE_HTML = """
<html><body>
  <h1>Analyze</h1>
  <input type='file' id='file'>
  <button id='start'>Start Analysis</button>
  <div class='analysis-status'>Completed</div>
  <div class='result-peak-value'>42.0</div>
</body></html>
"""
RESULTS_HTML = "<html><body><h1>Results</h1><div class='result-peak-value'>42.0</div><button id='export'>Export CSV</button></body></html>"

@app.route("/login")
def login():
    return render_template_string(LOGIN_HTML)

@app.route("/analyze")
def analyze():
    return render_template_string(ANALYZE_HTML)

@app.route("/results")
def results():
    return render_template_string(RESULTS_HTML)

@app.route("/api/analysis", methods=["GET","POST"])
def api_analysis():
    return jsonify({"runId":"abc","status":"completed","results":{"peak":42.0}})

@app.route("/download/results.csv")
def download_results():
    # small CSV response
    return ("id,peak\n1,42.0", 200, {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=results.csv"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
