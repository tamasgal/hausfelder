import os
from flask import Flask, render_template, request
from dbfread import DBF

app = Flask(__name__)

print("Staring the application")


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}

    stock_sport = {}
    for record in DBF('SPORT/LAG.DBF', 'Latin-1'):
        stock_sport[record["EDV"]] = record
        stock_sport[record["EDV"].replace("-", "")] = record

    stock_schuh = {}
    for record in DBF('SCHUH/LAG.DBF', 'Latin-1'):
        stock_schuh[record["EDV"]] = record
        stock_schuh[record["EDV"].replace("-", "")] = record

    if request.method == "POST":
        edv = request.form['edv'].strip()
        if edv in stock_sport.keys():
            stock = stock_sport
            size_lables = SIZE_LABELS_SPORT
        elif edv in stock_schuh.keys():
            stock = stock_schuh
            size_lables = SIZE_LABELS_SCHUH
        else:
            errors.append(f"Artikel nicht gefunden.")
            return render_template('index.html', errors=errors, results=results)

        record = stock[edv]

        results["EDV"] = record["EDV"]
        FB = results["FB"] = record["FB"]  # Farbe
        SZ = results["SZ"] = record["SZ"]  # Sortimentsziffer
        results["size_labels"] = size_labels[SZ]
        results["sizes"] = {
                "Bestand": [tonum(record[key]) for key in CHARS],
                "Verkauf": [tonum(record[key + "1"]) for key in CHARS],
                "Sonstiges": [tonum(record[key + "2"]) for key in CHARS],
        }

    return render_template('index.html', errors=errors, results=results)


def tonum(x):
    if x is None:
        return 0
    return x


def fullsizes(lower, upper):
    sizes = []
    for s in range(lower, upper+1):
        sizes.append(f"{s}")
    return sizes


def halfsizes(lower, upper):
    sizes = []
    for s in range(lower, upper+1):
        sizes.append(f"{s}")
        if s != upper:
            sizes.append(f"-")
    return sizes


CHARS = "ABCDEFGHIKLMNOPQRSU"
SIZE_LABELS_SCHUH = {
    '1': halfsizes(1, 10),
    '2': halfsizes(34, 43),
    '3': fullsizes(30, 48),
    '4': halfsizes(5, 14),
    '5': halfsizes(39, 47) + ["48", "49"],
    '6': fullsizes(15, 33),
    '7': fullsizes(25, 43),
    '8': halfsizes(3, 12)
}
SIZE_LABELS_SPORT = {
    '1': [70, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 150, 160, 165, 170, 175],
    '2': [150, 160, 165, 170, 175, 180, 185, 190, 195, 197, 200, 203, 205, 207, 210, 213, 215, 220, 225],
    '3': ["00", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "XXS", "XS", "S", "M", "L", "XL", "XXL"],
    '4': [250, 260, 270, 280, 290, 295, 300, 305, 310, 315, 320, 325, 330, 335, 340, 345, 350, 355, 360],
    '5': [230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320],
    '6': halfsizes(3, 12),
    '7': [30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66],
    '8': ["", 86, 92, 98, 104, 110, 116, 122, 128, 134, 140, 146, 152, 158, 164, 170, 176, 182, 188]
}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
