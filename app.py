from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

# Role-based skills
ROLE_SKILLS = {
    "Java Full Stack": ["java", "spring", "hibernate", "html", "css", "javascript", "sql"],
    "Cloud Engineer": ["aws", "gcp", "docker", "kubernetes", "linux", "ci/cd"],
    "Data Analyst": ["python", "sql", "excel", "power bi", "statistics"]
}

# Extract text from uploaded PDF
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text().lower()
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        resume = request.files["resume"]
        role = request.form["role"]

        text = extract_text(resume)
        required = ROLE_SKILLS[role]

        matched = [skill for skill in required if skill in text]
        missing = list(set(required) - set(matched))
        score = int((len(matched) / len(required)) * 100)

        result = {
            "score": score,
            "matched": matched,
            "missing": missing
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)