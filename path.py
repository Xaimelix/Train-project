import heapq

graph = {'A': [(1, 'B')], 'B': [(3, 'C'), (2, 'E'), (1, 'A')], 'C': [(2, 'D'), (3, 'B')],
         'D': [(2, 'E'), (2, 'C')], 'E': [(3, 'F'), (2, 'B')], 'F': [(3, 'E')]}


def dijkstra(start, end, graph):
    queue = []
    heapq.heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heapq.heappop(queue)
        if cur_node == end:
            break

        for next_node in graph[cur_node]:
            neighbor_cost, neighbor_node = next_node
            new_cost = cost_visited[cur_node] + neighbor_cost

            if neighbor_node not in cost_visited or new_cost < cost_visited[neighbor_node]:
                heapq.heappush(queue, (new_cost, neighbor_node))
                cost_visited[neighbor_node] = new_cost
                visited[neighbor_node] = cur_node

    return visited


# visited = dijkstra('A', 'F', graph)
#
# cur_n = 'F'
# while cur_n != 'A':
#     cur_n = visited[cur_n]
#     print(cur_n)
