import random
import time
import numpy

def beam_search(n, beam_width):

    start = format(0, f"0{n}b")
    paths = [[start]]
    canonical_check = [n-1]
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
        if len(new_paths) == 0:
            print("time:", time.time()-start_time)
            return len(paths[-1]), paths[-1]
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

                del new_paths[c]
                del new_can_check[c]

        paths = new_paths.copy()
        canonical_check = new_can_check.copy()
    print("time:", time.time()-start_time)
    return len(paths[-1]), paths[-1]


print(beam_search(7, 800))
