import os
from flask import Flask, render_template, url_for, redirect, request
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
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'projectSARmail@gmail.com',
    MAIL_PASSWORD = 'rhutuja1234'
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

@app.route('/')
def homepage():
    products = Products.query.all()
    return render_template("homepage.html", products = products)

@app.route('/show-product/<int:product_id>')
def showproduct(product_id):
    product = Products.query.filter_by(id=product_id).one()
    return render_template("ShowProduct.html", product=product)

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    form = ContactUsForm(request.form)
 
    if form.validate_on_submit():
       msg = Message(form.yourname.data,
        sender="projectSARmail@gmail.com",
        recipients=['greataakarshan@gmail.com'])
       msg.body = 'By '+form.yourname.data+',\n'+form.feedback.data           
       mail.send(msg)
       return render_template('mailsent.html')
    return render_template('contactus.html', form=form) 

db.create_all()

admin.add_view(ModelView(Products, db.session))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

