from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route('/likes', methods=["GET"])
def test():
    names = request.args.get('names', '')
    text = str.split(names, ",")
    error_message = False
    data = None
    error_text = None

    for i in range(len(text)):
        if len(text) > 0 and len(text[i]) > 10 or not text[i].isalpha():
            error_message = True

    if text[0] == '':
        print("Это никому не нравится")
        error_message = False
        data = "Это никому не нравится"
    if len(text) == 1 and text[0] != '':
        print(f"{text[0]} лайкнул это")
        data = f"{text[0]} лайкнул это"
    if len(text) == 2:
        print(f"{text[0]} и {text[1]} лайкнули это")
        data = f"{text[0]} и {text[1]} лайкнули это"
    if len(text) == 3:
        print(f"{text[0]}, {text[1]} и {text[2]} лайкнули это")
        data = f"{text[0]}, {text[1]} и {text[2]} лайкнули это"
    if len(text) >= 4:
        print(f"{text[0]}, {text[1]} и еще {len(text) - 2} лайкнули это")
        data = f"{text[0]}, {text[1]} и еще {len(text) - 2} лайкнули это"

    if error_message:
        data = None
        print("Error")

    if request.method == "GET":
        error_text = "У тебя тут это что-то сломалось"
    return render_template("index.html", error_message=error_message, data=data, error_text=error_text)


if __name__ == '__main__':
    app.run(debug=True)
