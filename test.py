from DB import *
from collections import deque

all_lines = get_line()
a = 'Снеговая'
b = 'Мыс Чуркин'

line_start = get_line(a)[0]
line_stop = get_line(b)[0]

graph = {'Луговая-2': get_stations('Кольцевая'), 'Луговая-1': get_stations('Эгершельд'),
         'Площадь': get_stations('Эгершельд'),
         'Морской вокзал': get_stations('Кольцевая'),
         'Первая речка': [get_stations('Снеговая'), get_stations('Заря'), get_stations('Кольцевая')]}


def find_path(start, end):
    path = []
    if start == end:
        return True
    else:
        if get_line(start) == get_line(end):
            write = False
            print('same line')
            line = get_stations(*get_line(start))
            for elem in line:
                if elem == start:
                    write = True
                if write:
                    path.append(elem)
                if elem == end:
                    write = False
            print('found', path)
        else:
            line = get_stations(*get_line(start))
            if len(line) // (line.index(start) + 1) < len(line) // 2:
                line.reverse()
            need_transfer = False
            for elem in line:
                path.append(elem)
                if station_transfer_to_line(elem) == get_line(end)[0]:
                    print('1 transfer', elem)
                    need_transfer = elem
                    break
            if need_transfer:
                if get_line(end)[0] == station_transfer_to_line(need_transfer):
                    line = get_stations(station_transfer_to_line(need_transfer))
                    if len(line) // (line.index(station_transfer_to_station(need_transfer)) + 1) < len(line) // 2:
                        line.reverse()
                    transfer_line_start_from_index = line.index(station_transfer_to_station(need_transfer))
                    for elem in line[transfer_line_start_from_index:]:
                        path.append(elem)
                        if elem == end:
                            break
                print('found', path)
            else:
                queue = []
                for elem in line:
                    st = elem.split('-')[0]
                    # print(elem)
                    if st in graph:
                        # path.append(elem)
                        for i in graph[st]:
                            for j in i:
                                if station_transfer_to_line(j) == line_stop:
                                    need_transfer = station_transfer_to_line(j)
                                    line = get_stations(need_transfer)
                                    if len(line) // (line.index(station_transfer_to_station(j)) + 1) < len(
                                            line) // 2:
                                        line.reverse()
                                    for k in line:
                                        path.append(k)
                            # if i not in path:
                            #     path.append(elem)
                            if i != line_start and i not in queue:
                                queue.append(i)
                while queue:
                    new_line = queue.pop(0)
                    for elem in new_line:
                        if station_transfer_to_line(elem) == line_stop:
                            for i in get_stations(station_transfer_to_line(elem)):
                                # if i not in path:
                                #     path.append(i)
                                pass
                print(path)
                # print(queue)



def transfer_path(station, stop):
    path = []
    line = station_transfer_to_line(station)
    for current in get_stations(line):
        if current == stop:
            path.append(current)
            return path
        else:
            path.append(current)


find_path(a, b)
