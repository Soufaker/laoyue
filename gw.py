import os

#获取h1主域名和查询用地址
os.system('./bbscope h1 -t NkMrjyBYbH79EhWANy/gBED4nKDKOSRaJIofGOpFimQ= -u soufaker -b -o t > h1.txt')
os.system('./bbscope h1 -t NkMrjyBYbH79EhWANy/gBED4nKDKOSRaJIofGOpFimQ= -u soufaker -b -o tdu > h1_check.txt')


# #获取bugcrowd主域名
os.system('./bbscope bc -t VzNtVzl2c0Z2YVBsSjhWakZvS3FES2MvVmVHN1hXRnVadjZUR0RpYzJLeVRMekxJQnZneGpqRExCaFE5UHhhNzN1RUE5R085U2EwZkVtb3llZjd2TTM0bzRBcUJOS1VOYm9yN3FUYWFFbDEvYTQzemNUZkg2OFdYRVZzb05pVFV3dHU5ek1WR241R1lxcDM5eU5pcUcwWmE1WlRLOVFsQ0dVUjFvRnVITE1TRjRuTmcrbVZXbmxKL1FxaVpFYVNMaHIrTjZCS2VKYWVBamlMS1RRQ3VXSHlHc0ZiSlF2RjZqWUd5MVN3dThyS2Zsd2hlQll0YzdwelZ0L3kydG5xdS0tTHYrblJjOFVBTXkxbXREUitRNVVZZz09--36be118fe392cf2c40c753b1582a13fd07f70af5 -b -o t > bc.txt')
os.system('./bbscope bc -t VzNtVzl2c0Z2YVBsSjhWakZvS3FES2MvVmVHN1hXRnVadjZUR0RpYzJLeVRMekxJQnZneGpqRExCaFE5UHhhNzN1RUE5R085U2EwZkVtb3llZjd2TTM0bzRBcUJOS1VOYm9yN3FUYWFFbDEvYTQzemNUZkg2OFdYRVZzb05pVFV3dHU5ek1WR241R1lxcDM5eU5pcUcwWmE1WlRLOVFsQ0dVUjFvRnVITE1TRjRuTmcrbVZXbmxKL1FxaVpFYVNMaHIrTjZCS2VKYWVBamlMS1RRQ3VXSHlHc0ZiSlF2RjZqWUd5MVN3dThyS2Zsd2hlQll0YzdwelZ0L3kydG5xdS0tTHYrblJjOFVBTXkxbXREUitRNVVZZz09--36be118fe392cf2c40c753b1582a13fd07f70af5 -b -o tdu > bc_check.txt')


def get_domain(txt):
    d = open(txt, 'r', encoding='utf-8').read().split('\n')
    domain = []
    for i in d:
        if i[0] == "*":
            domain.append(i)

    with open('domain'+txt,'w') as f:
        for d in domain:
            f.writelines(d+'\n')

get_domain('h1.txt')
get_domain('bc.txt')