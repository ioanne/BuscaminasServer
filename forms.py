from wtforms import Form
from wtforms.fields import IntegerField
import wtforms_json

wtforms_json.init()

class TableroForm(Form):
    cantidad_minas = IntegerField('Cantidad de Minas', default=10)
    celdas_x = IntegerField('X', default=10)
    celdas_y = IntegerField('Y', default=10)