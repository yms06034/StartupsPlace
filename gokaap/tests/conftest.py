import sys
sys.path.append('.')

from gokaap.configs import TestingConfig
from gokaap import create_app, db
from gokaap.models.user import User as UserModel
import pytest
import os

@pytest.fixture(scope='session')
def user_data():
    yield dict (
        user_id = 'tester_1',
        user_name = 'tester_1',
        password = 'tester_1'
    )


@pytest.fixture(scope='session')
def app(user_data):
    app = create_app(TestingConfig())
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(UserModel(**user_data))
        db.session.commit()
        yield app
        # sqlite drop
        db.drop_all()
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace(
            'sqlite:///',
            ''
        )
        if os.path.isfile(db_path):
            os.remove(db_path)



@pytest.fixture(scope='session')
def client(app, user_data):
    with app.test_client() as client:
        # NOTE : 세션 입혀주기
        with client.session_transaction() as session:
            session['user_id'] = user_data.get('user_id')
        yield client