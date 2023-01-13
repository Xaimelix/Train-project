from path import dijkstra

stations_indexes = {1: 'Мыс Чуркин', 2: 'Мальцевская',
                    3: 'Луговая-2', 4: 'Авангард',
                    5: 'Набережная Цесаревича', 6: 'Рыбный рынок',
                    7: 'Морской вокзал', 8: 'Казанский мост',
                    9: 'Луговая-1', 10: '3ая Рабочая',
                    11: 'Военное шоссе', 12: 'Первая речка',
                    13: 'Кунгасный', 14: 'Ресторанная',
                    15: 'Площадь', 16: 'Деревенский рынок',
                    17: 'Военный городок', 18: 'Снеговая',
                    19: 'Моргородок', 20: 'Вторая речка',
                    21: 'Заря'}
C_1 = stations_indexes[1]
C_2 = stations_indexes[2]
C_3 = stations_indexes[3]
C_4 = stations_indexes[4]
C_5 = stations_indexes[5]
C_6 = stations_indexes[6]
C_7 = stations_indexes[7]
C_8 = stations_indexes[8]
C_9 = stations_indexes[9]
C_10 = stations_indexes[10]
C_11 = stations_indexes[11]
C_12 = stations_indexes[12]
C_13 = stations_indexes[13]
C_14 = stations_indexes[14]
C_15 = stations_indexes[15]
C_16 = stations_indexes[16]
C_17 = stations_indexes[17]
C_18 = stations_indexes[18]
C_19 = stations_indexes[19]
C_20 = stations_indexes[20]
C_21 = stations_indexes[21]

graph = {C_1: [(3.3, C_2)], C_2: [(3.3, C_1), (3.8, C_3), (4.1, C_9)],
         C_3: [(3.8, C_2), (3.1, C_4), (0.7, C_9)], C_4: [(3.1, C_3), (2.8, C_5)],
         C_5: [(2.2, C_6), (2.8, C_4)], C_6: [(2.2, C_5), (2.5, C_7)],
         C_7: [(2.5, C_6), (4.7, C_8), (1.8, C_15)], C_8: [(4.7, C_7)],
         C_9: [(3.9, C_10), (0.7, C_3), (4.1, C_2)], C_10: [(2.1, C_11), (3.9, C_9)],
         C_11: [(2.8, C_12), (2.1, C_10)], C_12: [(3.8, C_13), (2.8, C_11), (4.4, C_19), (4.8, C_16)],
         C_13: [(3.8, C_12), (3.3, C_14)], C_14: [(3.3, C_13), (2.1, C_15)],
         C_15: [(2.1, C_14), (1.8, C_7)], C_16: [(4.8, C_12), (4.3, C_17)],
         C_17: [(4.3, C_16), (2.7, C_18)], C_18: [(2.7, C_17)],
         C_19: [(4.4, C_12), (4.0, C_20)], C_20: [(4.0, C_19), (4.8, C_21)],
         C_21: [(4.8, C_20)]}

print(dijkstra(C_1, C_21, graph))
