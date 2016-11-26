#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template, abort, Blueprint

mode = Blueprint('user', __name__, template_folder='templates')

@mode.route('/')
def index():
	return render_template('index.html')

@mode.route('/gomoku')
def gomoku():
	return render_template('gomoku.html')