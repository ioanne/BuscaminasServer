from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)


def obtener_datos_tablero():
    data = request.data
    
    return data

class GenerarTablero(Resource):
    def put(self, id_partida):
        '''
            Esta función generara un tablero de buscaminas a partir de un id de partida.
            (El id se generara en el cliente y se asignara a un usuario)
        '''
        tablero_form = obtener_datos_tablero()

        if tablero_form.validate():
            pass
        


api.add_resource(GenerarTablero, '/partida/<int:id_partida>/generar_tablero')

if __name__ == '__main__':
    app.run(debug=False)