from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/buscaminas.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

ma = Marshmallow(app)


class Tablero(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    cantidad_minas = db.Column(db.Integer)
    cantidad_x = db.Column(db.Integer)
    cantidad_y = db.Column(db.Integer)
    casilleros_revelados = db.Column(db.Integer)
    estado = db.Column(db.Integer)
    id_partida = db.Column(db.Integer, unique=True)
    game_over = db.Column(db.Boolean, default=False)

    filas = db.relationship('Fila', back_populates='tablero')
    celdas = db.relationship('Celda', back_populates='tablero')

    def get_by_id_partida(id_partida):
        tablero = Tablero.query.filter_by(
            id_partida=id_partida).first()

        return tablero


class Fila(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    id_tablero = db.Column(db.Integer, db.ForeignKey('tablero.id'))
    nro_fila = db.Column(db.Integer)

    tablero = db.relationship('Tablero', back_populates='filas')
    celdas = db.relationship('Celda', back_populates='fila')

    def get_by_id_tablero(id_tablero):
        filas = Fila.query.filter_by(
            id_tablero=id_tablero).order_by(
            Fila.nro_fila).all()
        return filas


class Celda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nro_celda = db.Column(db.Integer)
    estado = db.Column(db.Integer)
    contenido = db.Column(db.Integer)
    bandera = db.Column(db.Boolean)
    id_tablero = db.Column(db.Integer, db.ForeignKey('tablero.id'))
    id_fila = db.Column(db.Integer, db.ForeignKey('fila.id'))
    
    fila = db.relationship('Fila', back_populates='celdas')
    tablero = db.relationship('Tablero', back_populates='celdas')

    def get_minas_en_celdas(id_tablero):
        minas = Celda.query.filter_by(
            id_tablero=id_tablero).filter_by(
            contenido=1).all()
        return minas


class CeldaSchema(ma.Schema):
    id_fila = fields.Int()
    nro_celda = fields.Int()
    estado = fields.Int()
    contenido = fields.Int()
    bandera = fields.Bool()
    id_tablero = fields.Int()


class FilaSchema(ma.Schema):
    id_tablero = fields.Int()
    nro_fila = fields.Int()
    celdas = fields.List(fields.Nested(CeldaSchema))


fila_schema = FilaSchema()
celda_schema = CeldaSchema()
filas_schema = FilaSchema(many=True)
celdas_schema = CeldaSchema(many=True)


if __name__ == '__main__':
    manager.run()