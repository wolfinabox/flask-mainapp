#mhw stuff
from .wiki.lookup import get_effects_from_horn,get_horns_from_effects,get_horn_list,get_melody_list,can_play,get_horn_info
from flask import render_template, request, url_for, flash, redirect, send_from_directory,jsonify
from flask_cors import cross_origin
import json
from app import app




#Lookups
@app.route('/mhw_horn_generator/api/v1/get_melody_list',methods=['GET'])
@cross_origin()
def req_get_melody_list():
    return jsonify({'response':get_melody_list()})

@app.route('/mhw_horn_generator/api/v1/get_horn_list',methods=['GET'])
@cross_origin()
def req_get_horn_list():
    return jsonify({'response':get_horn_list()})

@app.route('/mhw_horn_generator/api/v1/get_horns_from_effects',methods=['GET'])
@cross_origin()
def req_get_horns_from_effects():
    melodies:tuple=tuple(json.loads(request.args.get('melodies','[]')))
    horn_list=get_horn_list()
    horns=get_horns_from_effects(melodies)
    response={'horns':horns,'note_icon_url':horn_list['note_icon_url'],'parse_time':horn_list['parse_time']}
    return jsonify({'response':response})

@app.route('/mhw_horn_generator/api/v1/get_effects_from_horn',methods=['GET'])
@cross_origin()
def req_get_effects_from_horn():
    horn:str=json.loads(request.args.get('horn','""'))
    horn_list=get_horn_list()
    effects=get_effects_from_horn(horn)
    response={'effects':effects,'note_icon_url':horn_list['note_icon_url'],'parse_time':horn_list['parse_time']}
    return jsonify({'response':response})

@app.route('/mhw_horn_generator/api/v1/horn_can_play_melody',methods=['GET'])
@cross_origin()
def req_horn_notes_can_play_melody():
    horn_notes:tuple=tuple(json.loads(request.args.get('horn_notes','[]')))
    melody:tuple=tuple(json.loads(request.args.get('melody','[]')))
    return jsonify({'response':can_play(horn_notes,melody)})


@app.route('/mhw_horn_generator/api/v1/get_horn_info',methods=['GET'])
@cross_origin()
def req_get_horn_info():
    horn:str=json.loads(request.args.get('horn','""'))
    info=get_horn_info(horn)
    return jsonify({'response':{'info':info}})