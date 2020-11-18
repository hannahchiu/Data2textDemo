from app import app
from flask import render_template, flash, request, redirect, url_for
from app.forms import LoginForm
from app.control import ctrl


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    pattern_string = ""

    pattern = request.args.get('pattern')
    suggestions = []
    if pattern:
        sug = ctrl.intent_pattern[pattern]
        for s in sug:
            if s.find('name') == -1:
                suggestions.append(s)

    if form.validate_on_submit():
        print('fff')
        command = form.inputtext.data
        flash('已輸入指令: {}'.format(command))
        cmd_string, pattern_string = ctrl.control(command)
        zh_string = ""
        for k in CMD_LIST:
            if k[0] == cmd_string:
                zh_string = k[1]
        flash('Pattern: [{} {}] {}'.format(cmd_string, zh_string, pattern_string))
        # return redirect(url_for(cmd_string))
        print(cmd_string)
        return render_template('index.html', title='Intention Demo', form=form, cmd=cmd_string, cmd_list=CMD_LIST, suggestions=suggestions)
    return render_template('index.html', title='Intention Demo', form=form, cmd="", cmd_list=CMD_LIST, suggestions=suggestions)
