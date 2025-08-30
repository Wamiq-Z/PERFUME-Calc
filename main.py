from flask import redirect, render_template, request, url_for
from config import app,db
from models import Compound

@app.route("/")
def index():
    compound = Compound.query.all()
    print(compound)
    return render_template("index.html",compounds=compound)

@app.route("/add", methods=["GET","POST"])
def add_compound():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price_perkg"])
        new_com = Compound(name=name,price_perkg=price)
        db.session.add(new_com)
        db.session.commit()
        
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    compound = Compound.query.get_or_404(id)
    if request.method == "POST":
        compound.name = (request.form["name"],compound.name)
        compound.price_perkg = (request.form["price"],compound.price)
        db.session.commit()
        return redirect(url_for(index))
    return render_template("edit.html",compound=compound)
    
@app.route("/delete/<int:id>",methods=["POST"])
def delete(id):
    compound = Compound.query.get_or_404(id)
    db.session.delete(compound)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/calc",methods=["GET","POST"])
def calc():
    compounds = Compound.query.all()
    selected = []
    total_price = 0

    if request.method == "POST":
        for compound in compounds:
            qty = request.form.get(str(compound.id))
            if qty and float(qty) > 0:
                qty = float(qty)
                price = qty * compound.price_perkg
                selected.append((compound.name, qty, compound.price_perkg, price))
                total_price += price

    return render_template("calc.html", compounds=compounds, selected=selected, total=total_price)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)