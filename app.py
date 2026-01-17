from datetime import datetime

from flask import Flask, request, render_template_string
from openai import OpenAI
def log_usage():
    with open("usage.txt", "a") as f:
        f.write(f"{datetime.now()}\n")


app = Flask(__name__)
import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

HTML = """
<!DOCTYPE html>
<html>
<head>
    <h1>ReplyPilot AI 🚀</h1>
<p>Paste a customer email and generate a professional reply.</p>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f4f4f4;
        }
        textarea, select, button {
            font-size: 16px;
            padding: 8px;
            margin-top: 5px;
        }
        button {
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>ReplyPilot AI 🚀</h1>

    <form method="post">
        <textarea name="email" rows="6" cols="60" placeholder="Paste the customer email here...">
{{ request.form.email if request.form else "" }}</textarea>
<br><br>

        <label>Tone:</label>
        <select name="tone">
            <option>friendly</option>
<option>formal</option>
<option>direct</option>
        </select>

        <label>Goal:</label>
        <select name="goal">
            <option>inform</option>
<option>sell</option>
<option>decline</option>
        </select>

        <br><br>
        <button type="submit">Generate answer</button>
    </form>

    {% if answer %}
        <h2>AI Answer</h2>
        <textarea rows="8" cols="80">{{ answer }}</textarea>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    answer = None

    if request.method == "POST":
        email = request.form["email"]
        tone = request.form["tone"]
        goal = request.form["goal"]

        prompt = f"""
You are a professional customer service employee.
Write a {tone} reply with the goal to {goal}.
Reply to this e-mail:
{email}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You write professional customer answers."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content
        log_usage()

    return render_template_string(HTML, answer=answer)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

