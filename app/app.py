from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # if form submitted then grab user input
        user_input = request.form.get("description")

        # debugging
        print(f"User input captured: {user_input}")

        return render_template("index.html", input=user_input)

    # render input form
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)