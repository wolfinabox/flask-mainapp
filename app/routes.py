from flask import render_template, request, url_for, flash, redirect, send_from_directory,jsonify
from flask_cors import cross_origin
import os
from app import app

import json

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    return "<h1>What're you doing here? :)</h1>"

#Static
@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory(os.path.join('.','static'), path)


import importlib
imported_subapps=[]
#Import all subapps
from app.utils import local_path
subapp_path=local_path('subapps')
for dir in os.listdir(subapp_path):
    full_path=os.path.join(subapp_path,dir)
    if not os.path.isdir(full_path):continue
    if dir.lower().startswith('disabled'):continue
    if not os.path.exists(os.path.join(full_path,'routes.py')):continue
    mod_name=os.path.relpath(os.path.join(full_path,'routes')).replace('\\','.')

    importlib.import_module(mod_name)
    imported_subapps.append(dir)

print(f' * Imported subapps: {", ".join(imported_subapps)}')