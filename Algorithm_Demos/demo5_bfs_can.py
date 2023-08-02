# import random
import time


def create_tree(selected_path, can_num, level, n):
    # , paths):
    nested_tree = [selected_path]
    can_tree = [can_num]
    start_time = time.time()
    while level > 0:
        #        print("level", level)
        next_level = []
        next_can = []
        # print("trees: ", nested_tree)
        # print("trees can: ", can_tree)
        for i in range(0, len(nested_tree)):
            end_node = nested_tree[i][-1]
            can_check = can_tree[i]

            for x in range(can_check, n):
                test_node = list(end_node)
                if test_node[x] == "0":
                    test_node[x] = "1"
                else:
                    test_node[x] = "0"
                test_node = ''.join(test_node)

                illegal = 0
                m = nested_tree[i].copy()
                m.append(test_node)

                if test_node in nested_tree[i]:
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

                        if neighbour_check in nested_tree[i] and \
                           neighbour_check != nested_tree[i][-1]:
                            illegal = 1

                if illegal == 0:
                    next_level.append(m)
                    if x == can_check and can_check > 0:
                        can_check -= 1
                    next_can.append(can_check)
                    can_check = can_tree[i]

        if next_level == []:
            print("time:", time.time() - start_time)
            return nested_tree, can_tree
        nested_tree = next_level.copy()
        can_tree = next_can.copy()
        level -= 1
        print("len path:", len(nested_tree[-1]))
        print("num options", len(nested_tree))
        print("time:", time.time() - start_time)
    print("time:", time.time() - start_time)
    return nested_tree, can_tree


n = 6

print(create_tree(["0000000"], n-1, 50, n))
