import time
#from beam_search import beam_search


n = 7


def dfs():

    #    start = prime
    start = [format(0, f"0{n}b")]
    path = start
    path_can = n-1
    completed_length = {}
    max = 0
    start_time = time.time()
    done = False
    complete = False
    while not complete:
        while not done:
            end_node = path[-1]
            if end_node in completed_length:
                redun_check = completed_length[end_node]
            else:
                redun_check = n-1

            for x in range(redun_check, path_can-1, -1):
                #            print(x)
                # print(path)
                test_node = list(end_node)
                if test_node[x] == "0":
                    test_node[x] = "1"
                else:
                    test_node[x] = "0"
                test_node = ''.join(test_node)

                illegal = 0
                m = path.copy()
                m.append(test_node)

                if test_node in path:
                    illegal = 1
                # elif m in paths or m in deadends:
                #     illegal = 1
                else:
                    for k in range(0, n):
                        neighbour_check = list(test_node)
                        if neighbour_check[k] == "0":
                            neighbour_check[k] = "1"
                        else:
                            neighbour_check[k] = "0"
                        neighbour_check = ''.join(neighbour_check)

                        if neighbour_check in path and \
                           neighbour_check != path[-1]:
                            illegal = 1

                if illegal == 0:
                    path = m
    #                if test_node in completed_length:
                    completed_length[end_node] = x - 1
                    if x == path_can and path_can > 0:
                        path_can -= 1
                    break
            if illegal == 1:
                done = True

    #    print(len(path), path)
        if len(path) > max:
            max = len(path)
            print(max)
            print(time.time() - start_time)
#        print(completed_length)
    #    deadends.append(path)
        # if no possible move
        if path[-1] in completed_length:
            del completed_length[path[-1]]
        del path[-1]
        done = False


dfs()
