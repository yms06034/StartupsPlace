from flask import Blueprint, render_template, request, g
from sqlalchemy import create_engine


DB_CONNECT_PATH = 'mysql+pymysql://root:password@localhost:3307/gokaap?charset=utf8'

engine = create_engine(DB_CONNECT_PATH)
conn = engine.connect()


