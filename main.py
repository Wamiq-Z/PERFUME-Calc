from flask import jsonify, redirect, render_template, request, session, url_for
from config import app, db
from models import Compound


@app.route("/")
def index():
    compound = Compound.query.order_by(Compound.name.asc()).all()
    calc_ids = session.get("calculator", [])
    return render_template("index.html", compounds=compound, calc_ids=calc_ids)


@app.route("/add", methods=["GET", "POST"])
def add_compound():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price_perkg"])
        max_id = db.session.query(db.func.max(Compound.id)).scalar() or 0
        next_id = max_id + 1
        new_com = Compound(id=next_id, name=name, price_perkg=price)
        try:
            db.session.add(new_com)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": str(e)}), 400

        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    compound = Compound.query.get_or_404(id)
    if request.method == "POST":
        compound.name = request.form["name"]
        compound.price_perkg = float(request.form["price"])
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", compound=compound)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    compound = Compound.query.get_or_404(id)
    db.session.delete(compound)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/calc", methods=["GET", "POST"])
def calc():
    calc_ids = session.get("calculator", [])
    remove_id = request.form.get("remove_id")
    if remove_id:
        remove_id = int(remove_id)
        if remove_id in calc_ids:
            calc_ids.remove(remove_id)
            session["calculator"] = calc_ids
        return redirect(url_for("calc"))

    compounds = Compound.query.filter(Compound.id.in_(calc_ids)).order_by(Compound.name.asc()).all()
    selected = []
    total_price = 0
    total_quantity = 0

    if request.method == "POST":
        for compound in compounds:
            qty = request.form.get(str(compound.id))
            if qty and float(qty) > 0:
                qty = float(qty)
                price = qty * compound.price_perkg
                selected.append((compound.name, qty, compound.price_perkg, price))
                total_price += price
                total_quantity += qty
    avg_price_per_kg = total_price / total_quantity if total_quantity > 0 else 0
    total_qty_g = total_quantity * 1000
    return render_template(
        "calc.html",
        compounds=compounds,
        selected=selected,
        total=total_price,
        total_quantity=total_quantity,
        avg_price_per_kg=avg_price_per_kg,
        total_qty_g=total_qty_g,
    )


@app.route("/add_to_calculator/<int:id>")
def add_to_calculator(id):
    # get current calculator list from session
    calculator = session.get("calculator", [])

    if id not in calculator:
        calculator.append(id)  # add compound id
        session["calculator"] = calculator

    return redirect(url_for("index"))


@app.route("/remove_from_calculator/<int:id>", methods=["POST"])
def remove_from_calculator(id):
    calc_ids = session.get("calculator", [])
    if id in calc_ids:
        calc_ids.remove(id)
        session["calculator"] = calc_ids
    return redirect(url_for("calc"))


@app.route("/remove_from_hs/<int:id>", methods=["POST"])
def remove_from_hs(id):
    calc_ids = session.get("calculator", [])
    remove_id = request.form.get("remove_id")
    if id in calc_ids:
        remove_id = int(remove_id)
        if remove_id in calc_ids:
            calc_ids.remove(remove_id)
            session["calculator"] = calc_ids
        return redirect(url_for("index"))


@app.route("/search_compounds")
def search_compounds():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])

    results = Compound.query.filter(Compound.name.ilike(f"%{query}%")).all()
    added_ids = set(session.get("calculator", []))
    print(added_ids)
    return jsonify(
        [
            {
                "id": c.id,
                "name": c.name,
                "price": c.price_perkg,
                "added": c.id in added_ids,
            }
            for c in results
        ]
    )


@app.route("/add_search", methods=["POST"])
def add_search():
    data = request.get_json()
    compound_id = data.get("id")

    compound = Compound.query.get(compound_id)
    if not compound:
        return jsonify({"message": "Compound not found"}), 404

    compounds = session.get("calculator", [])
    if compound.id not in compounds:
        compounds.append(compound.id)
        session["calculator"] = compounds
        session.modified = True
    else:
        return jsonify({"message": "Already added"})

    return jsonify(success=True)


# @app.route("/perf")
# def perf():

#     return jsonify({"message:":"Hi lav jain"})

if __name__ == "__main__":

    app.run(debug=True)
