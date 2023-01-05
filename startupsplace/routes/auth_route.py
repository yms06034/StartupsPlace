from flask import Blueprint, render_template, url_for, redirect, flash, session, request, g
from startupsplace.forms.auth_form import LoginForm, RegisterForm
from startupsplace.models.user import User as UserModel
from werkzeug import security

NAME = 'auth'

auth_bp = Blueprint(NAME, __name__, url_prefix='/auth')

@auth_bp.before_app_request
def before_app_request():
    g.user = None
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            g.user = user
        else:
            session.pop('user_id', None)
            

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.data.get('user_id')
        password = form.data.get('password')

        user = UserModel.find_one_by_user_id(user_id)
        if user:
            if not security.check_password_hash(user.password, password):
                flash('비밀번호가 일치하지 않습니다')
            else:
                session['user_id'] = user.user_id
                return redirect(url_for('base.index'))
        else:
            flash('아이디가 없거나 일치하지 않습니다')
    else:
        flash_form_errors(form)

    return render_template(f'{NAME}/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = form.data.get('user_id')
        user_name = form.data.get('user_name')
        password = form.data.get('password')
        repassword = form.data.get('repassword')

        user = UserModel.find_one_by_user_id(user_id)
        if user:
            flash('이미 존재하는 USER ID 입니다.')
            return redirect(request.path)
        else:
            g.db.add(
                UserModel(
                    user_id = user_id,
                    user_name = user_name,
                    password = security.generate_password_hash(password)
                )
            )
            g.db.commit()
            session['user_id'] = user_id
            return redirect(url_for('base.index'))
    else:
        flash_form_errors(form)

    return render_template(f'{NAME}/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('base.index'))

def flash_form_errors(form):
    for _, errors in form.errors.items():
        for e in errors:
            flash(e)