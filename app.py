from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask('__main__')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/crud_app'
app.config['SECRET_KEY'] = 'A VERY HARD TO GUESS STRING'


db = SQLAlchemy(app)

# models


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    about = db.Column(db.Text(), nullable=False)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        about = request.form['about']

        # create new user instance
        new_user = User(name=name, about=about)

        # add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash(f"The name you entered is {name}")
        flash(f"About you: {about}")

        return redirect(url_for('index'))
    else:
        data = User.query.all()
        return render_template('index.html', data=data)

# update user


# @app.route('/update/<int:id>', methods=['POST', 'GET'])
# def update(id):
#     user_to_update = User.query.get_or_404(id)
#     if request.method == 'POST':
#         try:
#             user_to_update.name = request.form['name']
#             user_to_update.about = request.form['about']
#             db.session.commit()
#             return redirect(url_for('index'))
#         except:
#             return 'There was a problem updating {{user_to_update.name}}'
#     else:
#         return render_template('update.html', user=user_to_update)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    user_to_update = User.query.get_or_404(id)

    if request.method == 'POST':
        user_to_update.name = request.form['name']
        user_to_update.about = request.form['about']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', user=user_to_update)

# view one user queried by id


@app.route('/<int:id>')
def one_user(id):
    one_user = User.query.get_or_404(id)
    return render_template('one_user.html', user=one_user)


# delete one user queried by id
@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
