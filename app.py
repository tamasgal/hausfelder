import os
from flask import Flask, render_template, request
from dbfread import DBF

app = Flask(__name__)

print("Staring the application")


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
            FB = results["FB"] = record["FB"]  # Farbe
            SZ = results["SZ"] = record["SZ"]  # Sortimentsziffer
            sizes1 = [(size, record[key]) for key, size in zip(CHARS, SIZE_LABELS[SZ]) if key not in "JT"]
            sizes2 = [(size, record[key + "1"]) for key, size in zip(CHARS, SIZE_LABELS[SZ]) if key not in "JT"]
            sizes3 = [(size, record[key + "2"]) for key, size in zip(CHARS, SIZE_LABELS[SZ]) if key not in "JT"]
            results["sizes"] = [sizes1]#, sizes2, sizes3]
#            results["price"] =              ('VKWERT', 464.92)) for key, size in zip(char_range("A", "U"), range(1, 100)) if key not in "JT"]
            results["sizes"] = [sizes1, sizes2, sizes3]
#            results["price"] =              ('VKWERT', 464.92),

    return render_template('index.html', errors=errors, results=results)


def fullsizes(lower, upper):
    sizes = []
    for s in range(lower, upper+1):
        sizes.append(f"{s}")
    return sizes

def halfsizes(lower, upper):
    sizes = []
    for s in range(lower, upper+1):
        sizes.append(f"{s}")
        sizes.append(f"-")
    return sizes


CHARS = "ABCDEFGHIKLMNOPQRSU"
SIZE_LABELS = {
        '1': halfsizes(1, 10),
        '2': halfsizes(34, 43),
        '3': fullsizes(30, 48),
        '4': halfsizes(5, 14),
        '5': halfsizes(39, 47) + ["48", "49"],
        '6': fullsizes(15, 33),
        '7': fullsizes(25, 43),
        '8': halfsizes(3, 12)
}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
