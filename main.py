from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hostelDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Visit_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(255), nullable=False)
    coming_or_leave = db.Column(db.Boolean, default=True)
    visit_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    # text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'{self.id}'


@app.route('/')
def index():
    items = Visit_list.query.order_by(Visit_list.id).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        fio = request.form['fio']
        coming_or_leave = False
        if request.form.get('coming_or_leave') != None:
            coming_or_leave = True

        visit = Visit_list(fio=fio, coming_or_leave=coming_or_leave)
        try:
            db.session.add(visit)
            db.session.commit()
            return redirect('/')
        except:
            return 'Получилась ошибка'
    else:
        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True,
            # host='0.0.0.0'
            )
