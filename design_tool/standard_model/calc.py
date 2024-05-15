from collections import OrderedDict
def calc_z(n, x, y):
    z = 4 * n * (4 * n - y) / (x - 4)
    return z

status = OrderedDict()
for n in range(1, 12): #multiple 4
    x_max = 4 * n * 2
    y_max = 4 * 4
    print(f"Standard Model:")
    print(f"{n}: {n * 4} {4} {n * 4}")
    if n == 1:
        status[0] = {'text': f'standard model, , , , ,', 'loc': n}
        status[1] = {'text': f'Cost {n}, {n * 4}, {4}, {n * 4}, ,', 'loc': n}
        status[2] = {'text': f' , , , , ,', 'loc': n}
    else:
        status[0] = {'text': status[0]['text'] + f'standard model, , , , ,', 'loc': n}
        status[1] = {'text': status[1]['text'] + f'Cost {n}, {n * 4}, {4}, {n * 4}, ,', 'loc': n}
        status[2] = {'text': status[2]['text'] + f' , , , , ,', 'loc': n}
    ind = 3
    for x in range(0, x_max, 1):
        for y in range(0, y_max, 1):
            try:
                z = calc_z(n, x, y)
                if x >= 0 and y >= 0 and z >= 0:
                    string = f"Cost {n}, {x}, {y}, {int(z)}, ,"
                    if len(status) <= ind:
                        padding = " , , , , ," * (n - 1)
                        status[ind] = {'text': padding + string, 'loc': n}
                    else:
                        padding = " , , , , ," * ((n - 1) - status[ind]['loc'])
                        status[ind] = {'text': status[ind]['text'] + padding + string, 'loc': n}
                    #print(f"{n}: {x} {y} {int(z)}")
                    ind += 1
            except ZeroDivisionError:
                pass
                #print(f"{n}: {x} {y}")
    #y = 4
    #z = calc_z(n, 12, y)

f = open('cost_data.csv', 'w')
for k in status:
    f.write(status[k]['text'] + '\n')
f.close()
