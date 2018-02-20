from models import Tablero, Fila
import random


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

            for x in range(tablero.cantidad_x):
                celda = Celda(
                    id_fila=fila.id,
                    id_tablero=tablero.id,
                    nro_celda=x
                )
                db.session.add(celda)
                db.session.commit()

        filas = Fila.get_by_id_tablero(tablero.id)
        minas = generar_minas(
                    cantidad_minas,
                    celdas_x,
                    celdas_y)

        for mina in minas:
            filas[mina[0]].celdas[mina[1]].contenido = 1
        db.session.commit()
        return filas
    else:
        return tablero


def generar_minas(cantidad, celdas_x, celdas_y):
    contenedor_minas = set()
    while len(contenedor_minas) <= cantidad -1:
        x = random.randint(0, celdas_x - 1)
        y = random.randint(0, celdas_y - 1)
        contenedor_minas.add((x,y))
    return contenedor_minas