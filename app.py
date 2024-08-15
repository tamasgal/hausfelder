import os
from flask import Flask, render_template, request
from dbfread import DBF

app = Flask(__name__)

print("Staring the application")

SIZE_LABELS = {
        '0': range(0, 100),
        '1': range(1, 100),
        '2': range(2, 100),
        '3': range(3, 100),
        '4': range(4, 100),
        '5': range(5, 100),
        '6': range(6, 100),
        '7': range(7, 100),
        '8': range(8, 100),
        '9': range(9, 100),
}

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}

    stock = {}
    for record in DBF('SPORT/LAG.DBF', 'Latin-1'):
        stock[record["EDV"]] = record

    if request.method == "POST":
        try:
            EDV = request.form['edv'].strip()
            record = stock[EDV]
        except KeyError:
            errors.append(f"Artikel nicht gefunden.")
        except Exception as e:
            errors.append(e)
        else:
            results["EDV"] = record["EDV"]
            FB = results["FB"] = record["FB"]
            sizes1 = [(size, record[key]) for key, size in zip(char_range("A", "U"), SIZE_LABELS[FB]) if key not in "JT"]
            sizes2 = [(size, record[key + "1"]) for key, size in zip(char_range("A", "U"), SIZE_LABELS[FB]) if key not in "JT"]
            sizes3 = [(size, record[key + "2"]) for key, size in zip(char_range("A", "U"), SIZE_LABELS[FB]) if key not in "JT"]
            results["sizes"] = [sizes1]#, sizes2, sizes3]
#            results["price"] =              ('VKWERT', 464.92)) for key, size in zip(char_range("A", "U"), range(1, 100)) if key not in "JT"]
            results["sizes"] = [sizes1, sizes2, sizes3]
#            results["price"] =              ('VKWERT', 464.92),

    return render_template('index.html', errors=errors, results=results)


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
