from app import app
from flask import render_template, flash, request, redirect, url_for
from app.forms import LoginForm
from src.test import Generator, all_slots, GeneratorZH, all_slots_zh
import json
from app.control import Controller
ctrl = Controller('app/pattern/intent_pattern.json', 'app/pattern/entity_info.json', 'app/pattern/styleme_new.tsv', 'app/pattern/effect2ids.json', 'app/pattern/response.json')

# some selected example table for user to click on 
TABLE = json.load(open('data/new_table.json'))
# names displayed on the website for the examples
NAMES = ['Dell Laptop Latitude E6440', 
         'Dell Vostro 3458', 
         'Apple iMac 27', 
         'HP Z820 Workstation', 
         'iBUYPOWER Gamer Supreme', 
         'Toshiba Tecra C50-B1503', 
         'Asus Z91', 
         'Lenovo T530'
         ]

# some selected example table (chinese) for user to click on
TABLE_ZH = json.load(open('data/zh_data.json'))
# names displayed on the website for the examples
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

# init generator for chinese
generator_zh = GeneratorZH(checkpoint='src/checkpoint.zh.pth')
print('finish loading generator')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    product = request.args.get('product')  # the id of selected example product

    table = {}
    description = ""
    ds = []

    try:
        print('pro', product)
        num = int(product)                 # the id of selected example product -> if this line works, means it is int
                                           # means user have clicked on some example -> need to display the attr table
        # get the table and example name
        table = TABLE_ZH[num-1]
        name = NAMES_ZH[num-1]
        global_table = table
    except:
        if product == 'submit':
            ### handle table here ###
            num_form = (len(request.form)-1)//2
            table = {}
            form_table = request.form.to_dict(flat=False)  # convert table into a dictionary

            # get the input table through a form (displayed as a modifiable table)
            # pass to python code using request.form
            for i in range(num_form):   # fill the attribute and value to table
                if not request.form['attr-%d'%i]:
                    continue
                table[request.form['attr-%d'%i]] = request.form['value-%d'%i]

            if table:
                if request.values["des"] != "" and request.values["action"] == 'submit_des':
                    description = request.values['des']
                else:
                ######################################
                # generate a description based on the table
                ######################################
                    description = generator_zh.test(table)

                ds = description.split('\n') # description per line (momo format -> bullet points)
                # description = ""
        # elif product == "submit2":
        #     description = request.values['des']
        tuples = list(table.items())  # turn table into tuples of 2 elements

        # if product == "submit":
        #     print(table)
        #     print(description)
        #     return render_template('index2.html', form=form, table=tuples, description=description, product_list=NAMES_ZH, ds=ds)
        # else:

        print(description)
        return render_template('index2.html', form=form, table=tuples, description=description,
                               product_list=NAMES_ZH, ds=ds)

    tuples = list(table.items())
    return render_template('index2.html', form=form, table=tuples, description=description, product_list=NAMES_ZH, ds=ds)

# display all possible attributes
@app.route('/attr', methods=['GET', 'POST'])
def attr():
    return render_template('attr.html', slots=all_slots_zh)


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    desText = request.args.get('des')
    intent_string, pattern_string, get_item, item_list, resp_string = ctrl.control(userText)
    print(intent_string)
    print(resp_string)
    return "使用者輸入:" + userText + "; description:" + desText
