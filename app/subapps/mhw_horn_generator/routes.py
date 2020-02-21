#mhw stuff
from flask import render_template, request, url_for, flash, redirect, send_from_directory,jsonify
from flask_cors import cross_origin
import json
from app import app
from .wiki.lookup import get_melody_list,get_horn_list,get_horns_from_effects,get_effects_from_horn,reset_data,get_horn_names,get_melody_names

@app.route('/mhw_horn_generator')
@cross_origin()
def mhw_horn_generator():
    return redirect('https://wolfinabox.github.io/mhw-horn-generator/')

#Lookups
@app.route('/mhw_horn_generator/api/v1/get_melody_names',methods=['GET'])
@cross_origin()
def req_get_melody_names():
    return jsonify({'response':get_melody_names()})

@app.route('/mhw_horn_generator/api/v1/get_horn_names',methods=['GET'])
@cross_origin()
def req_get_horns():
    return jsonify({'response':get_horn_names()})


@app.route('/mhw_horn_generator/api/v1/get_melody_list',methods=['GET'])
@cross_origin()
def req_get_melody_name_list():
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
    response={'horns':horns,'note_img_urls':horn_list['note_img_urls'],'parse_time':horn_list['parse_time']}
    return jsonify({'response':response})

@app.route('/mhw_horn_generator/api/v1/get_effects_from_horn',methods=['GET'])
@cross_origin()
def req_get_effects_from_horn():
    horn:str=json.loads(request.args.get('horn','""'))
    horn_list=get_horn_list()
    effects=get_effects_from_horn(horn)
    response={'effects':effects,'note_img_urls':horn_list['note_img_urls'],'parse_time':horn_list['parse_time']}
    return jsonify({'response':response})

# @app.route('/mhw_horn_generator/api/v1/horn_can_play_melody',methods=['GET'])
# @cross_origin()
# def req_horn_notes_can_play_melody():
#     horn_notes:tuple=tuple(json.loads(request.args.get('horn_notes','[]')))
#     melody:tuple=tuple(json.loads(request.args.get('melody','[]')))
#     return jsonify({'response':can_play(horn_notes,melody)})


# @app.route('/mhw_horn_generator/api/v1/get_horn_info',methods=['GET'])
# @cross_origin()
# def req_get_horn_info():
#     horn:str=json.loads(request.args.get('horn','""'))
#     info=get_horn_info(horn)
#     return jsonify({'response':{'info':info}})

#misc
@app.route('/mhw_horn_generator/api/v1/endpoints',methods=['GET'])
@cross_origin()
def req_endpoints():
    func=lambda r:r.rule
    endpoints=[func(r) for r in iter( app.url_map.iter_rules() ) if '/mhw_horn_generator/api/' in func(r) and 'admin' not in func(r)]
    return jsonify({'response':endpoints})


#admin
@app.route('/mhw_horn_generator/api/v1/admin/reset_data',methods=['GET'])
@cross_origin()
def req_reset_data():
    reset_data()
    parse_time=get_horn_list()['parse_time']
    return jsonify({'response':parse_time})
    
