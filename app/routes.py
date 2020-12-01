from app import app
from flask import render_template, flash, request, redirect, url_for
from app.forms import LoginForm
from src.test import Generator, all_slots, GeneratorZH, all_slots_zh
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
# generator = Generator(checkpoint='src/checkpoint.pth')
# print('finish loading generator')

TABLE_ZH = json.load(open('data/zh_data.json'))

NAMES_ZH = ['【STEIFF】熊頭童裝 長袖T恤',
'【Footer】輕壓力單色足弓襪',
'【ILEY 伊蕾】100%縲縈碎花長版洋裝',
'【初色】休閒條紋拼接上衣-藏藍色',
'【RIVER WOODS】簡約質感V領長袖針織衫',
'【MON’S】浪漫花版修身洋裝',
'【XLARGE】XLARGE S/S TEE REFLECTOR DRAWING OG短袖T恤',
'【Jessica Red】氣質素色圓領綁帶造型上衣',
'【SNOOPY 史努比】史努比穿毛衣寬版大學T'
]
"""
@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    product = request.args.get('product')
    table = {}
    description = ""
    print('damn')
    # if form.validate_on_submit():
    #     print('fff')
    #     return render_template('index.html', form=form, table=tuples, description=description, product_list=NAMES)

    try:
        print('pro', product)
        num = int(product)
        table = TABLE[num-1]
        name = NAMES[num-1]
        global_table = table
    except:
        if product == 'submit':
            print('ggg')
            ### handle table here ###
            
            # print(request.form)
            num_form = (len(request.form))//2
            table = {}
            form_table = request.form.to_dict(flat=False)
            # print(form_table)
            for i in range(num_form):
                # print(form_table['attr-%d'%i], form_table['value-%d'%i])
                if not request.form['attr-%d'%i]:
                    continue
                table[request.form['attr-%d'%i]] = request.form['value-%d'%i]

            if table:
                print('table', table)
                # description = generator.test(table) 
                description = "sleghsefs"
                print(description)
        tuples = list(table.items())
        return render_template('index.html', form=form, table=tuples, description=description, product_list=NAMES)

    tuples = list(table.items())
    return render_template('index.html', form=form, table=tuples, description=description, product_list=NAMES)

@app.route('/attr', methods=['GET', 'POST'])
def attr():
    return render_template('attr.html', slots=all_slots)

"""


generator_zh = GeneratorZH(checkpoint='src/checkpoint.zh.pth')
print('finish loading generator')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    product = request.args.get('product')
    table = {}
    description = ""
    print('damn')
    ds = []
    # if form.validate_on_submit():
    #     print('fff')
    #     return render_template('index.html', form=form, table=tuples, description=description, product_list=NAMES)

    try:
        print('pro', product)
        num = int(product)
        table = TABLE_ZH[num-1]
        name = NAMES_ZH[num-1]
        global_table = table
    except:
        if product == 'submit':
            print('ggg')
            ### handle table here ###
            
            # print(request.form)
            num_form = (len(request.form))//2
            table = {}
            form_table = request.form.to_dict(flat=False)
            # print(form_table)
            for i in range(num_form):
                # print(form_table['attr-%d'%i], form_table['value-%d'%i])
                if not request.form['attr-%d'%i]:
                    continue
                table[request.form['attr-%d'%i]] = request.form['value-%d'%i]

            if table:
                print('table', table)
                description = generator_zh.test(table) 
                # description = "sleghsefs"
                print(description)
                ds = description.split('\n')
                description = ""
        tuples = list(table.items())
        return render_template('index.html', form=form, table=tuples, description=description, product_list=NAMES_ZH, ds=ds)

    tuples = list(table.items())
    return render_template('index.html', form=form, table=tuples, description=description, product_list=NAMES_ZH, ds=ds)

@app.route('/attr', methods=['GET', 'POST'])
def attr():
    return render_template('attr.html', slots=all_slots_zh)



