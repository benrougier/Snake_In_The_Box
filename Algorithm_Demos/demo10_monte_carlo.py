import random
from statistics import mean
import time

# n = 6
# chosen_level = 4


def nested_mc(start, n, level, can_start):

    #    start = format(0, f"0{n}b")
    #    start = ['0000000', '0000001', '0000011', '0000111']
    paths = [start]
    act_paths = [start]
    paths_can = [can_start]
    all_paths = []
    all_paths_best_play = []
    all_paths_cans = []
    black_list = []
    scores = []
    level_mem = level
    best_option = []
    best_opt_can = []
    deadends = []
    best_score = 0
    best_score_ever = 0
    best_path = []
    best_path_already_in = 0
    prev_length = 0
    start_time = time.time()
    length_of_path_that_made = 0

    while time.time() - start_time < 1800:

        #        print("paths:", paths)
        #    print("len path:", len(paths[-1]))
        if len(paths[-1]) == prev_length:

            index = scores.index(max(scores))
            paths = [all_paths[index]]
            length_of_path_that_made = len(paths[0])
            paths_can = [all_paths_cans[index]]
            best_score = scores[index]
    #        print("starting score", best_score)
            best_path = all_paths_best_play[index]
            del all_paths[index]
            del all_paths_cans[index]
            del scores[index]
            del all_paths_best_play[index]
#            break
#        print("path_can:", paths_can[-1])

        # selection
        selected_path, can_num = selection(
            paths, best_opt_can, best_option, paths_can, n)
#        print(selected_path)
        # create k level search tree
        level = level_mem
        possible_options, poss_options_can = create_tree(selected_path, can_num,
                                                         1, paths, n)

        if possible_options == []:
            break
#            deadends.append(selected_path)
        else:

            playout_scores = []
            playout_paths = possible_options.copy()
            playouts = []

            for u in range(len(possible_options)):
                possible_paths, poss_paths_can = create_tree(possible_options[u], poss_options_can[u],
                                                             level-1, paths, n)
                best_score_this_option = 0
                best_path_this_option = []
    #        best_score_this_it = 0
                for p in range(0, len(possible_paths)):
                    snake = possible_paths[p]
                    score, path, check = bias_search(snake[-1], snake[:-1],
                                                     poss_paths_can[p], n)

                    if score > best_score_this_option:
                        best_score_this_option = score
                        best_path_this_option = path
                    if score > best_score_ever:
                        best_score_ever = score
                        print("best ever", best_score_ever)
                        print("time:", time.time() - start_time)
                        print("best path:", path)
                        print("length of starting path:",
                              length_of_path_that_made)
                        # if score == 27:
                        #     exit()
                    if score > best_score:
                        best_path = path
                        best_score = score
                        best_option = snake

                playout_scores.append(best_score_this_option)
                playouts.append(best_path_this_option)

            prev_length = len(paths[0])

            to_select = best_path[:prev_length+1]
#            print("selection", to_select)

            for x in range(len(playout_paths)):
                if playout_paths[x] != to_select and len(playout_paths[x]) < w:
                    # if playout_paths[x] in black_list:
                    #     print("mistake!!")
                    all_paths.append(playout_paths[x])
                    all_paths_cans.append(poss_options_can[x])
                    scores.append(playout_scores[x])
                    all_paths_best_play.append(playouts[x])

            paths = [to_select]
            if to_select[-1][paths_can[-1]] == "1" and paths_can[-1] > 0:
                paths_can[-1] -= 1

    print("time:", time.time()-start_time)
#     print("number of deadends:", len(deadends))
    return best_score, best_path


def create_tree(selected_path, can_num, level, paths, n):
    nested_tree = [selected_path]
    can_tree = [can_num]
    while level > 0:
        next_level = []
        next_can = []
        # print("trees: ", nested_tree)
        # print("trees can: ", can_tree)
        for i in range(0, len(nested_tree)):
            end_node = nested_tree[i][-1]
            can_check = can_tree[i]
            # print("snake:", nested_tree[i])
            # print("end node: ", end_node)
            # print("can_check: ", can_check)
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
    #            print("next level:", next_level)
        if next_level == []:
            return nested_tree, can_tree
        nested_tree = next_level.copy()
        can_tree = next_can.copy()
        level -= 1
    return nested_tree, can_tree


def selection(paths, best_opt_can, best_option, paths_can, n):
    if paths == [[format(0, f"0{n}b")]]:
        return [format(0, f"0{n}b")], n-1
    else:
        # best_option[:-1], best_opt_can  # [:-1]
        return paths[-1], paths_can[-1]


def bias_search(current_node, i, canonical_check, n):

    # nodes = Dict.empty(key_type=types.unicode_type, value_type=types.int64,)
    nodes = {}
    number_of_vertices = 2**n
    for m in range(0, number_of_vertices):
        bin_m = format(m, f"0{n}b")
        nodes[bin_m] = 0

    start = current_node
    visited = i + [start]
#    print(i)

    for p in i:
        nodes[p] = 1
        for j in range(0, n):

            neighbour_p = list(p)

            if neighbour_p[j] == "0":
                neighbour_p[j] = "1"
            else:
                neighbour_p[j] = "0"

            neighbour_p = ''.join(neighbour_p)

            nodes[neighbour_p] = 1
    done = False
#    print(nodes)
    nodes[start] = 1

    # canonical_check = n - 2

    while not done:

        bias_or_rand = random.uniform(0, 1)

        if bias_or_rand <= prob:
            count = 0
            fail = 1
            next_change = random.randint(canonical_check, n-1)
            while count <= n and fail == 1:

                fail = 0
    #            count = 0
                if next_change < canonical_check:
                    next_change = canonical_check

                old_node = current_node
                current_node = list(current_node)

                if current_node[next_change] == "0":
                    current_node[next_change] = "1"
                else:
                    current_node[next_change] = "0"

                current_node = ''.join(current_node)

                # Check if valid
                if nodes[current_node] == 0:
                    # change node value to 1
                    nodes[current_node] = 1
                    # change old neighbour node values
                    for i in range(0, n):
                        old_node = list(old_node)

                        if old_node[i] == "0":
                            old_node[i] = "1"
                            old_node = ''.join(old_node)
                            nodes[old_node] = 1
                            old_node = list(old_node)
                            old_node[i] = "0"
                            old_node = ''.join(old_node)

                        elif old_node[i] == "1":
                            old_node[i] = "0"
                            old_node = ''.join(old_node)
                            nodes[old_node] = 1
                            old_node = list(old_node)
                            old_node[i] = "1"
                            old_node = ''.join(old_node)
#                    print("random next change:", next_change)
                    if next_change == canonical_check and canonical_check > 0:
                        canonical_check -= 1
                    visited.append(current_node)

                else:
                    current_node = old_node
                    next_change = (next_change + 1) % n
                    count += 1
                    fail = 1
        #            print("count is ", count)

            if fail == 1:

                done = True
    #            print("reaching random")

                return len(visited), visited, canonical_check

    # if nph step
        else:

            number_free_nodes = 0
            current_best_choice = 0
            current_best_score = 2**n
            no_legal = 0
            old_node = current_node

            for i in range(canonical_check, len(current_node)):
                #                print("i is:", i)
                number_free_nodes = 0

                test_string = list(current_node)

                if test_string[i] == "1":
                    test_string[i] = "0"
                else:
                    test_string[i] = "1"

                test_string = ''.join(test_string)

                if nodes[test_string] == 0:
                    for j in range(0, len(current_node)):
                        testing = list(test_string)

                        if testing[j] == "1":
                            testing[j] = "0"

                        else:
                            testing[j] = "1"

                        testing = ''.join(testing)
        #                print(testing)
                        if nodes[testing] == 0:
                            number_free_nodes += 1

                if number_free_nodes > 0 and \
                   number_free_nodes < current_best_score:

                    current_best_choice = i

                    current_best_score = number_free_nodes
#                    print("current_best_choice", current_best_choice)

                else:
                    no_legal += 1

            if no_legal != n:
                # add new to visited
                next_change = current_best_choice
#                print("nph next change", next_change)
                current_node = list(current_node)

                if current_node[next_change] == "0":
                    current_node[next_change] = "1"
                else:
                    current_node[next_change] = "0"

                current_node = ''.join(current_node)

                visited.append(current_node)
                nodes[current_node] = 1
                # change neighbours to illegal
                for i in range(0, n):
                    old_node = list(old_node)

                    if old_node[i] == "0":
                        old_node[i] = "1"
                        old_node = ''.join(old_node)
                        nodes[old_node] = 1
                        old_node = list(old_node)
                        old_node[i] = "0"
                        old_node = ''.join(old_node)

                    elif old_node[i] == "1":
                        old_node[i] = "0"
                        old_node = ''.join(old_node)
                        nodes[old_node] = 1
                        old_node = list(old_node)
                        old_node[i] = "1"
                        old_node = ''.join(old_node)
    #            print("nph next change", next_change)
                if next_change == canonical_check and canonical_check > 0:
                    canonical_check -= 1
            else:
                done = True
#                print("reaching nph")
                return len(visited), visited, canonical_check


n = 7
chosen_level = 4
w = 30
prob = 0


formated_primer = [format(0, f"0{n}b")]

best_score = 0
best_path = []
lengths = []
for x in range(1):
    score, path = nested_mc(
        formated_primer, n, chosen_level, n-1)  # n-1
    print(score)
    lengths.append(score)
    if score > best_score:
        best_score = score
        best_path = path.copy()
        #        print(best_score)

        print(best_score)
        print(best_path)
        print("number of lists is:", len(lengths))
        #
        print("mean score is: ", mean(lengths))
