from app import app
from flask import render_template, flash, request, redirect, url_for
from app.forms import LoginForm
from src.test import Generator
# from app.control import ctrl
import json

TABLE = json.load(open('data/new_table.json'))

NAMES = ['Dell Laptop Latitude E6440', 
         'Dell Vostro 3458', 
         'Apple iMac 27', 
         'HP Z820 Workstation', 
         'iBUYPOWER Gamer Supreme', 
         'Toshiba Tecra C50-B1503', 
         'Asus Z91', 
         'Lenovo T530'
         ]
generator = Generator(checkpoint='src/checkpoint.pth')
print('finish loading generator')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    product = request.args.get('product')
    table = {}
    description = ""
    print('damn')
    try:
        print('pro', product)
        num = int(product)
        table = TABLE[num-1]
        name = NAMES[num-1]

    except:
        print('ggg')
        return render_template('base.html', form=form, table=table, description=description, product_list=NAMES)

    print('table')
    description = generator.test(table) 
    table = list(table.items())
    if form.validate_on_submit():
        print('fff')
        print(description)
               
        return render_template('base.html', form=form, table=table, description=description, product_list=NAMES)
    return render_template('base.html', form=form, table=table, description=description, product_list=NAMES)
