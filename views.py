from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json
import forms as form
from logica_buscaminas import generar_tablero
from models import Tablero, filas_schema, celdas_schema 

app = Flask(__name__)
api = Api(app)


def obtener_datos_tablero():
    data = request.data
    if data:
        data = request.data
        buscaminas_form = form.TableroForm.from_json(data)

    return buscaminas_form


class GenerarTablero(Resource):
    def put(self, id_partida):
        '''
            Esta función generara un tablero de buscaminas a partir de un id de partida.
            (El id se generara en el cliente y se asignara a un usuario)
        '''
        tablero_form = obtener_datos_tablero()

        if tablero_form.validate():
            # Retornamos las filas con las columnas.
            filas = generar_tablero(
                    id_partida,
                    tablero_form.cantidad_minas.data,
                    tablero_form.celdas_y.data,
                    tablero_form.celdas_y.data
            )

        if filas:
            filas = filas_schema.dump(filas).data
            
            return jsonify({'Filas': filas })

        else:
            return jsonify({'Mensaje': 'Error.'})


api.add_resource(GenerarTablero, '/partida/<int:id_partida>/generar_tablero')

if __name__ == '__main__':
    app.run(debug=False)