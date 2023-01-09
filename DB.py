import sqlite3

connect = sqlite3.connect('Info.sqlite3')
cur = connect.cursor()


def get_points():
    a = cur.execute(f"""select points from lines order by id""").fetchall()
    res = a[0][0]
    return res


def get_line(station=None):
    if station:
        a = cur.execute(f"""select lines from stations where name = '{station}' order by id""").fetchall()
        res = [i[0] for i in a]
    else:
        a = cur.execute(f"""select name from lines order by id""").fetchall()
        res = [i[0] for i in a]
    return res


def get_stations(line=None):
    """return list of stations"""
    if line:
        a = cur.execute(f"""select name from stations where lines = '{line}' order by id""").fetchall()
        res = [i[0] for i in a]
    else:
        a = cur.execute(f"""select name from stations order by id""").fetchall()
        res = [i[0] for i in a]
    return res


def station_transfer_to_line(station: str):
    """return line \n
    Ex: Луговая-1(Кольцевая) return: Эгершельд(Луговая-2)"""
    a = cur.execute(f"""select transfer from stations where name = '{station}' order by id""").fetchall()
    res = [i[0] for i in a][0]
    return res


def station_transfer_to_station(station: str):
    """return station \n
    Ex: Луговая-1 return: Луговая-2"""
    a = cur.execute(f"""select transfer_to from stations where name = '{station}' order by id""").fetchall()
    res = [i[0] for i in a][0]
    return res

