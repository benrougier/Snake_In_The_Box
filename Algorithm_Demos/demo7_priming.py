import time
#from beam_search import beam_search
import random


n = 7

#score, prime = beam_search(7, 2000)


def dfs(start):

    #    start = prime
    #    start = [format(0, f"0{n}b")]
    pathy = start
    path_can = 0
    completed_length = {}
    max = 0
    start_time = time.time()
#    deadends = []
#    completed_length[start[-1]] = n-1
    done = False
    complete = False
    while time.time() - start_time < 100:
        while not done:
            end_node = pathy[-1]
            if end_node in completed_length:
                redun_check = completed_length[end_node]
            else:
                redun_check = n-1
    #        for x in range(n-1, path_can-1, -1):
    #        print(redun_check)
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
                m = pathy.copy()
                m.append(test_node)

                if test_node in pathy:
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

                        if neighbour_check in pathy and \
                           neighbour_check != pathy[-1]:
                            illegal = 1

                if illegal == 0:
                    pathy = m
    #                if test_node in completed_length:
                    completed_length[end_node] = x - 1
                    if x == path_can and path_can > 0:
                        path_can -= 1
                    break
            if illegal == 1:
                done = True

    #    print(len(path), path)
    #    print(max)
    #     print(type(pathy))
    # #    print(len(path))
    #     print("path", pathy)
    #     print(len(pathy))
    #    path = list(path)
        if len(pathy) > max:
            max = len(pathy)
            print(max)
            print(time.time() - start_time)
#        print(completed_length)
    #    deadends.append(path)
        # if no possible move
        if pathy[-1] in completed_length:
            del completed_length[pathy[-1]]
        del pathy[-1]
        done = False
    #    exit()


def beam_search(n, beam_width, stop):

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
        if len(new_paths) == 0 or len(new_paths[-1]) == stop:
            print("time:", time.time()-start_time)
            return len(paths[-1]), paths, len(paths)
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


primero = ['00000000', '00000010', '00000110', '00001110', '00011110', '00111110', '01111110', '01101110', '01100110', '01100010', '01100000', '01110000', '01111000', '00111000', '00101000', '00101100', '00100100', '00110100', '00010100', '01010100', '01000100', '01001100', '01001000', '01001010', '01011010',
           '01010010', '11010010', '11000010', '11000110', '11001110', '11011110', '11011100', '10011100', '10001100', '10001000', '10001010', '10011010', '10111010', '11111010', '11101010', '11101000', '11101100', '11100100', '11110100', '11110110', '10110110', '10100110', '10100010', '10100000', '10110000', '10010000']

print(len(primero))

dfs(primero[:20])
