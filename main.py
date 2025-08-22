from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields import TimeField
from wtforms.validators import DataRequired, Length, URL
import csv


app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField("Cafe Name", validators=[DataRequired(), Length(min=2)])
    location = StringField("Location URL", validators=[DataRequired(), URL()])
    open_time = TimeField(
        "Open (24h HH:MM)",
        format="%H:%M",
        validators=[DataRequired()],
        render_kw={"lang": "en-GB", "step": "60"},
    )
    close_time = TimeField(
        "Closed (24h HH:MM)",
        format="%H:%M",
        validators=[DataRequired()],
        render_kw={"lang": "en-GB", "step": "60"},
    )
    coffee = SelectField(
        "Coffee",
        choices=[
            ("☕", "☕"),
            ("☕☕", "☕☕"),
            ("☕☕☕", "☕☕☕"),
            ("☕☕☕☕", "☕☕☕☕"),
            ("☕☕☕☕☕", "☕☕☕☕☕"),
        ],
        validators=[DataRequired()],
    )
    wifi = SelectField(
        "Wifi",
        choices=[
            ("✘", "✘"),
            ("💪", "💪"),
            ("💪💪", "💪💪"),
            ("💪💪💪", "💪💪💪"),
            ("💪💪💪💪", "💪💪💪💪"),
        ],
        validators=[DataRequired()],
    )
    power = SelectField(
        "Power",
        choices=[
            ("🔌", "🔌"),
            ("🔌🔌", "🔌🔌"),
            ("🔌🔌🔌", "🔌🔌🔌"),
            ("🔌🔌🔌🔌", "🔌🔌🔌🔌"),
            ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Ensure file ends with a newline before appending a new row
        with open("cafe-data.csv", "rb+") as f:
            f.seek(0, 2)
            if f.tell() > 0:
                f.seek(-1, 1)
                last_byte = f.read(1)
                if last_byte not in (b"\n", b"\r"):
                    f.write(b"\n")
        with open("cafe-data.csv", "a", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(
                [
                    form.cafe.data,
                    form.location.data,
                    (
                        form.open_time.data.strftime("%H:%M")
                        if form.open_time.data
                        else ""
                    ),
                    (
                        form.close_time.data.strftime("%H:%M")
                        if form.close_time.data
                        else ""
                    ),
                    form.coffee.data,
                    form.wifi.data,
                    form.power.data,
                ]
            )
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    with open("cafe-data.csv", newline="", encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template("cafes.html", cafes=list_of_rows)


if __name__ == "__main__":
    app.run(debug=True)
