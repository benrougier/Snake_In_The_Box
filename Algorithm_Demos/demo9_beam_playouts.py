import random
import time


def beam_search(n, beam_width, start, c_check, stop):

    #    start = format(0, f"0{n}b")
    paths = start  # [[start]]
    canonical_check = c_check  # [n-1]
    start_time = time.time()

    while time.time() - start_time < 30000:
        new_paths = []
        new_can_check = []
        for p in range(0, len(paths)):
            i = paths[p]
            can_check = canonical_check[paths.index(i)]
            for x in range(can_check, n):

                new_node = list(i[-1])

                if new_node[x] == "0":
                    new_node[x] = "1"
                else:
                    new_node[x] = "0"

                new_node = ''.join(new_node)

                illegal = 0
                m = i.copy()
                m.append(new_node)
    #            print("m", m)
        #        print(k)

                if new_node in i:
                    illegal = 1

                else:
                    for k in range(can_check, n):
                        neighbour_check = list(new_node)
                        if neighbour_check[k] == "0":
                            neighbour_check[k] = "1"
                        else:
                            neighbour_check[k] = "0"
                        neighbour_check = ''.join(neighbour_check)

                        if neighbour_check in i and neighbour_check != i[-1]:
                            illegal = 1

                if illegal == 0:
                    #                    print("not illegal")
                    #            print(m)
                    new_paths.append(m)
                    if x == can_check and can_check > 0:
                        can_check -= 1
#                        print("can_lower")
                    new_can_check.append(can_check)
        print(len(new_paths))
#        print("new_paths", new_paths)
        if len(new_paths) == 0 or len(new_paths[-1]) == stop:
            print("time:", time.time()-start_time)
            return len(paths[-1]), paths  # [-1], len(paths)
        else:
            print("length:", len(new_paths[-1]))

        # start pruning new paths

        while len(new_paths) > beam_width:

            # generate random indexes

            randomsample = random.sample(range(0, len(new_paths)), 50)
            chopping_block = []
            chopping_score = []
            for x in randomsample:

                score, path, check = bias_search(
                    new_paths[x][-1], new_paths[x][:-1], new_can_check[x], n)
                if len(chopping_block) < 10:
                    chopping_block.append(x)
                    chopping_score.append(score)

                else:
                    if score < max(chopping_score):
                        del chopping_block[chopping_score.index(
                            max(chopping_score))]
                        chopping_block.append(x)
                        chopping_score.remove(max(chopping_score))
                        chopping_score.append(score)

            chopping_block.sort(reverse=True)
            for c in chopping_block:
                #                print("c:", c)
                #                print("len new_paths:", len(new_paths))

                del new_paths[c]
                del new_can_check[c]

        paths = new_paths.copy()
        canonical_check = new_can_check.copy()
    print("time:", time.time()-start_time)
    return len(paths[-1]), paths  # [-1]


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
#        print(visited)
#        print(canonical_check)
#        print(bias_or_rand)

        # if random search step
        if bias_or_rand <= 0:
            count = 0
            fail = 1
            next_change = random.randint(canonical_check, n-1)
            while count <= n and fail == 1:

                fail = 0
    #            count = 0
                if next_change < canonical_check:
                    next_change = canonical_check
                # next_change = random.randint(canonical_check, n-1)
    #            print("next change here", next_change)

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


#print(beam_search(8, 200))

n = 7
leng, primer = beam_search(n, 700, [["0000000"]], [n-1], 100)

print(len(primer[-1]))
