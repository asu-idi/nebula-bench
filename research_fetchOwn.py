import json
import os
import time
import operator

config_file = '/usr/local/nebula/etc/nebula-storaged.conf'
rocksdb_block_cache_prefix = '--rocksdb_block_cache='
enable_storage_cache_prefix = '--enable_storage_cache='
storage_cache_capacity_prefix = '--storage_cache_capacity='
enable_vertex_pool_prefix = '--enable_vertex_pool='
vertex_pool_capacity_prefix = '--vertex_pool_capacity='
empty_key_pool_capacity_prefix = '--empty_key_pool_capacity='

result_output = "research_output.txt"

fetchOwn_output = "output/result_FetchOwn.json"
result_file = open(result_output, mode='w', encoding='utf-8')

query_times = 0


def init():
    os.system('ulimit -n 130000')


def clear_memory():
    os.system('sync')
    time.sleep(2)
    os.system('sudo sh -c "echo 1 > /proc/sys/vm/drop_caches"')

    os.system('sync')
    time.sleep(2)
    os.system('sudo sh -c "echo 2 > /proc/sys/vm/drop_caches"')

    os.system('sync')
    time.sleep(2)
    os.system('sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"')


def start_bench():
    os.system('/usr/local/nebula/scripts/nebula.service start all')
    time.sleep(5)
    os.system('python3 run.py stress run -scenario fetch.FetchOwn --args=\'-u 100 -d 1m\'')
    time.sleep(10)


def read_output_file(output_file):
    global query_times
    with open(output_file, 'r') as load_f:
        result = json.load(load_f)
        metricMap = result['metrics']['latency']
        metricMap = dict(sorted(metricMap.items(), key=operator.itemgetter(0)))
        result_file.write("latency: " + str(metricMap) + "\n")
        checkMap = result['metrics']['checks']
        query_times = int(result['metrics']['checks']['passes'])
        checkMap = dict(sorted(checkMap.items(), key=operator.itemgetter(0)))
        result_file.write("check: " + str(checkMap) + "\n")
        result_file.flush()


def change_config(rocksdb_block_cache, storage_cache_capacity, vertex_pool_capacity, empty_key_pool_capacity):
    os.system('/usr/local/nebula/scripts/nebula.service stop all')
    time.sleep(5)
    clear_memory()
    time.sleep(5)
    file = open(config_file, mode='r', encoding='utf-8')
    content = file.read()
    file.close()
    arr = content.split("\n")
    file = open(config_file, mode='w', encoding='utf-8')
    for index in range(len(arr)):
        if arr[index].startswith(rocksdb_block_cache_prefix):
            arr[index] = rocksdb_block_cache_prefix + str(rocksdb_block_cache)
        elif arr[index].startswith(storage_cache_capacity_prefix):
            arr[index] = storage_cache_capacity_prefix + str(storage_cache_capacity)
        elif arr[index].startswith(vertex_pool_capacity_prefix):
            arr[index] = vertex_pool_capacity_prefix + str(vertex_pool_capacity)
        elif arr[index].startswith(enable_vertex_pool_prefix):
            if vertex_pool_capacity == 0:
                arr[index] = enable_vertex_pool_prefix + "false"
            else:
                arr[index] = enable_vertex_pool_prefix + "true"

        elif arr[index].startswith(enable_storage_cache_prefix):
            if vertex_pool_capacity == 0:
                arr[index] = enable_storage_cache_prefix + "false"
            else:
                arr[index] = enable_storage_cache_prefix + "true"
        elif arr[index].startswith(empty_key_pool_capacity_prefix):
            arr[index] = empty_key_pool_capacity_prefix + str(empty_key_pool_capacity)
        if index != len(arr) - 1:
            file.write(arr[index] + "\n")
        else:
            file.write(arr[index])
    file.close()
    time.sleep(5)


if __name__ == '__main__':
    init()
    slice_num = 1
    while slice_num <= 16:
        mem_total = slice_num * 256
        block_cache = mem_total
        while block_cache >= 0:
            vertex_pool = int((mem_total - block_cache) * 0.7)
            empty_pool = int((mem_total - block_cache) * 0.3)
            storage_cache = int((vertex_pool + empty_pool) * 1.3)
            change_config(block_cache, storage_cache, vertex_pool, empty_pool)
            result_file.write(str(block_cache) + " " + str(storage_cache) + " " + str(vertex_pool) + "\n")

            time_start = time.time()
            start_bench()
            time_end = time.time()

            read_output_file(fetchOwn_output)
            qps = query_times / (time_end - time_start)
            result_file.write("qps: " + str(qps) + "\n\n")
            result_file.flush()
            block_cache -= int(mem_total / 8)
        slice_num += 1
    result_file.close()
