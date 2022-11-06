from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    print('run: create_app()')
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secretkey'

    if app.config['DEBUG']:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

    """ CSRF INIT """
    csrf.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    from gokaap.forms.auth_form import LoginForm, RegisterForm

    @app.route('/auth/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user_id = form.data.get('user_id')
            password = form.data.get('password')
            return f'{user_id}, {password}'
        else:
            pass
        return render_template('login.html', form=form)

    @app.route('/auth/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            user_id = form.data.get('user_id')
            user_name = form.data.get('user_name')
            password = form.data.get('password')
            repassword = form.data.get('repassword')
            return f'{user_id}, {user_name}, {password}, {repassword}'
        else:
            pass

        return render_template('register.html', form=form)

    @app.route('/auth/logout')
    def logout():
        return 'logout'

    @app.errorhandler(404)
    def page_404(error):
        return render_template('404.html')

    return app

