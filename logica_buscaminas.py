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


def get_minas(id_tablero):
    minas = Celda.get_minas_en_celdas(id_tablero)
    minas_list = []
    
    for mina in minas:
        minas_list.append(
            (mina.nro_celda, mina.fila.nro_fila))
        return minas_list


def revelar_casillero(tablero_id, x, y):
    tablero = Tablero.query.get(tablero_id)

    # Comienza en None, lo pongo en 0
    if not tablero.casilleros_revelados:
        tablero.casilleros_revelados = 0
        db.session.commit()

    if tablero.filas[y].celdas[x].contenido == 1:
        tablero.game_over = True
        return False
    else:
        tablero.filas[y].celdas[x].estado = 1
        tablero.casilleros_revelados += 1

        db.session.commit()
        casilla = coord_a_num(tablero.id, x, y)
        casillas = get_casillas_al_rededor(casilla, tablero.id)
        if casillas:
            for c in casillas:
                tablero.filas[c[1]].celdas[c[0]].estado = 1
                tablero.casilleros_revelados += 1

            db.session.commit()
        return True


def coord_a_num(id_tablero, x, y):
    tablero = Tablero.query.filter_by(id=id_tablero).first()
    return tablero.cantidad_x*y+x


def num_a_coord(id_tablero, numero):
    tablero = Tablero.query.filter_by(id=id_tablero).first()
    return (numero%tablero.cantidad_x, numero//tablero.cantidad_x)


def get_casillas_al_rededor(casilla, tablero_id):
    minas = get_minas(tablero_id)
    tablero = Tablero.query.get(tablero_id)

    x, y = num_a_coord(tablero_id, casilla)
    casilleros_adyacentes = []
    casilleros_minados = []
    if x > 0:
        casilleros_adyacentes.append(
            num_a_coord(tablero_id, casilla - 1))

        if y > 0:
            casilleros_adyacentes.append(
                num_a_coord(
                    tablero_id, casilla - tablero.cantidad_x - 1))

        if y < 0:
            casilleros_adyacentes.append(
                num_a_coord(
                    tablero_id, casilla + tablero.cantidad_x - 1))

    if x < tablero.cantidad_x - 1:
        casilleros_adyacentes.append(
            num_a_coord(tablero_id, casilla + 1))

        if y > 0:
            casilleros_adyacentes.append(
                num_a_coord(
                    tablero_id, casilla - tablero.cantidad_x + 1))

        if y < tablero.cantidad_x - 1:
            casilleros_adyacentes.append(
                num_a_coord(
                    tablero_id, casilla + tablero.cantidad_x + 1))

    if y > 0:
        casilleros_adyacentes.append(
            num_a_coord(
                tablero_id, casilla - tablero.cantidad_x))

    if y < tablero.cantidad_x - 1:
        casilleros_adyacentes.append(
            num_a_coord(
                tablero_id, casilla + tablero.cantidad_x))

    casilleros_minados = [
            casillero for casillero in casilleros_adyacentes \
            for mina in minas if casillero == mina
            ]

    casilleros_no_minados = [
            casillero for casillero in casilleros_adyacentes \
            for mina in minas if casillero != mina
                ]

    if casilleros_minados:
        set_casilleros_no_minados = set(casilleros_no_minados)
        lista_casilleros_no_minados = list(set_casilleros_no_minados)
        
        return lista_casilleros_no_minados
    else:
        return None