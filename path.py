import heapq

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

