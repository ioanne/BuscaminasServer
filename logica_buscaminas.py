from models import Tablero, Fila

def generar_tablero(
            id_partida,
            cantidad_minas,
            celdas_x,
            celdas_y):
    
    tablero = Tablero.get_by_id_partida(id_partida)

    if not tablero:
        tablero = Tablero(
            cantidad_minas=cantidad_minas,
            cantidad_x=celdas_x,
            cantidad_y=celdas_y,
            id_partida=id_partida)

        for y in range(tablero.cantidad_y):
            fila = Fila(
                id_tablero=tablero.id,
                nro_fila=y
            )

            db.session.add(fila)
            db.session.commit()

        

        return tablero

