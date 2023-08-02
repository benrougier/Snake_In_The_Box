import time
from statistics import mean


def nph_search(current_node, i, canonical_check):

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


best_score = 0
min_score = 1000
best_path = []
lengths = []
start_time = time.time()
for o in range(10):
    score, path, can_num = nph_search("0000001", ["0000000"], n-2)
    lengths.append(score)

    if score > best_score:
        best_score = score
        best_path = path.copy()
        print("new best:", best_score)
    if score < min_score:
        min_score = score
    #    print("min score: ", score)

print("n = ", n)
print("Time:", time.time() - start_time)
print(best_score)
print(best_path)
print("min score: ", min_score)
print("number of lists is:", len(lengths))

print("mean score is: ", mean(lengths))
