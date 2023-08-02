import random
import time
from collections import Counter


def beam_search(n, beam_width):

    start = format(0, f"0{n}b")
    paths = [[start]]
    canonical_check = [n-1]
    start_time = time.time()
    best_coil = []
    best_coil_score = 0

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
        for h in new_paths:
            changed = 0
            best_coil, best_coil_score, changed = coil_check(
                h, n, best_coil, best_coil_score, changed)

            if changed == 1:
                break

        if len(new_paths) == 0:
            print("time:", time.time()-start_time)
            return best_coil_score, best_coil
        else:
            print("length:", len(new_paths[-1]))
        # start pruning new paths
        while len(new_paths) > beam_width:
            # generate random indexes
            randomsample = random.sample(range(0, len(new_paths)), 50)
            chopping_block = []
            chopping_score = []
            for x in randomsample:
                neighbours = []
                for p in new_paths[x]:
                    for j in range(new_can_check[x], n):
                        neighbour_p = list(p)

                        if neighbour_p[j] == "0":
                            neighbour_p[j] = "1"
                        else:
                            neighbour_p[j] = "0"

                        neighbour_p = ''.join(neighbour_p)

                        if neighbour_p not in neighbours:
                            neighbours.append(neighbour_p)

                if len(chopping_block) < 5:
                    chopping_block.append(x)
                    chopping_score.append(len(neighbours))
                else:
                    if len(neighbours) > min(chopping_score):
                        del chopping_block[chopping_score.index(
                            min(chopping_score))]
                        chopping_block.append(x)
                        chopping_score.remove(min(chopping_score))
                        chopping_score.append(len(neighbours))

            chopping_block.sort(reverse=True)
            for c in chopping_block:
                #                print("c:", c)
                #                print("len new_paths:", len(new_paths))

                del new_paths[c]
                del new_can_check[c]

        paths = new_paths.copy()
        canonical_check = new_can_check.copy()
    print("time:", time.time()-start_time)
    return len(paths[-1]), paths


def coil_check(patho, n, best_coil, best_coil_score, changed):
    end_node = patho[-1]
    counts = Counter(end_node)

    if counts["1"] == 2:
        #        print("yolo", patho)

        posits = [pos for pos, char in enumerate(end_node) if char == "1"]

        for numb in posits:
            neigh_check = list(end_node)

            neigh_check[numb] = "0"

            neigh_check = ''.join(neigh_check)

            legal = 0

            for k in range(0, n):
                neighbour_check = list(neigh_check)
                if neighbour_check[k] == "0":
                    neighbour_check[k] = "1"
                else:
                    neighbour_check[k] = "0"
                neighbour_check = ''.join(neighbour_check)

                if neighbour_check in patho and neighbour_check != end_node and neighbour_check != format(0, f"0{n}b"):
                    legal = 1

            if legal == 0:
                coil = patho.copy()
                coil.append(neigh_check)
                coil.append(format(0, f"0{n}b"))

                if len(coil) > best_coil_score:
                    print("coil", coil)
                    print("coil length:", len(coil))
                    changed = 1
                    return coil, len(coil), changed

                else:
                    return best_coil, best_coil_score, changed

        return best_coil, best_coil_score, changed

    else:
        return best_coil, best_coil_score, changed


print(beam_search(7, 1000))
