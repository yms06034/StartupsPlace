from flask import Blueprint, render_template, request
import requests
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import json

NAME = 'place'
DB_CONNECT_PATH = 'mysql+pymysql://root:password@localhost:3307/gokaap?charset=utf8'

engine = create_engine(DB_CONNECT_PATH)
conn = engine.connect()


place_bp = Blueprint(NAME, __name__)
@place_bp.route('/place', methods=['GET', 'POST'])

def place_html():
    return render_template('place.html')