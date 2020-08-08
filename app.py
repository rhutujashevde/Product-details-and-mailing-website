import os
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

BASEDIR=os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='thisisasecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(BASEDIR,'database.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'dummyflaskmail@gmail.com',
    MAIL_PASSWORD = '#######'
    )

mail = Mail(app)
admin = Admin(app, name='Upgrad', template_mode='bootstrap3')
db=SQLAlchemy(app)

class Products(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        description = db.Column(db.String(400), nullable=False)
        price = db.Column(db.Integer, nullable=False)
        manufacturer = db.Column(db.String(50), nullable=False)
        image_path = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    products = Products.query.all()
    if request.method == 'POST':
        search = Products.query.filter_by(name = request.form['prod']).first()
        return redirect(url_for('showproduct', product_id = search.id))
    return render_template("homepage.html", products = products)

@app.route('/show-product/<int:product_id>', methods=['GET', 'POST'])
def showproduct(product_id):
    product = Products.query.filter_by(id=product_id).one()
    if request.method == 'POST':
        msg = Message("Product Details",
        sender="dummyflaskmail@gmail.com",
        recipients=[request.form['emailid']])
        msg.body = '<h1>Hey '+ request.form['name'] + '</h1>'     
        mail.send(msg)
        flash("Mail sent!!")
        return render_template("ShowProduct.html", product=product) 
    return render_template("ShowProduct.html", product=product)

db.create_all()

admin.add_view(ModelView(Products, db.session))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

