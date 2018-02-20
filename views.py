from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json
import forms as form
from logica_buscaminas import generar_tablero
from models import Tablero, filas_schema, celdas_schema, db, Celda, Fila

app = Flask(__name__)
api = Api(app)


def obtener_datos_tablero():
    data = request.data.decode()
    if data:
        data_dict = ast.literal_eval(data)
        buscaminas_form = form.TableroForm.from_json(data_dict)
    else:
        data = request.data
        buscaminas_form = form.TableroForm.from_json(data)

    return buscaminas_form


class ChequearCasillero(Resource):
    '''
        Esta función chequea los casilleros.
        Te informa si hay una mina en el casillero a revelar
        Y retorna Game Over.
        Tambien valida si hay otros casilleros para revelar.
    '''
    def post(self, id_partida, x, y):
        tablero = Tablero.query.filter_by(id_partida=id_partida).first()
        if tablero:
            revelado = revelar_casillero(tablero.id, x, y)
            if revelado:
                tablero_json = filas_schema.dump(tablero.filas).data
                return {'Tablero': tablero_json}
            else:
                return {'Message': 'Game Over'}


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


class ObtenerTablero(Resource):
    def get(self, id_partida):
        tablero = Tablero.query.filter_by(id_partida=id_partida).first()

        if tablero:
            tablero_json = filas_schema.dump(tablero.filas).data
            return {'Tablero': tablero_json}
        else:
            return {'Mensaje': 'Error'}

api.add_resource(GenerarTablero, '/partida/<int:id_partida>/generar_tablero')
api.add_resource(ObtenerTablero, '/partida/<int:id_partida>')
api.add_resource(ChequearCasillero, '/partida/<int:id_partida>/chequear_casillero/x/<int:x>/y/<int:y>')

if __name__ == '__main__':
    app.run(debug=False, port=5555)