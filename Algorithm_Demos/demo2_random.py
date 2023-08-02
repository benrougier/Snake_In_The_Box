import random
import time
from statistics import mean


def random_search(current_node, i, canonical_check):

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

            return len(visited), visited, canonical_check


n = 8

best_score = 0
min_score = 1000
best_path = []
lengths = []
start_time = time.time()
for o in range(10000):
    score, path, can_num = random_search("00000001", ["00000000"], n-2)
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
