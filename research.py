import json
import os
import time

config_file = '/usr/local/nebula/etc/nebula-storaged.conf'
rocksdb_block_cache_prefix = '--rocksdb_block_cache='
enable_storage_cache_prefix = '--enable_storage_cache='
storage_cache_capacity_prefix = '--storage_cache_capacity='
enable_vertex_pool_prefix = '--enable_vertex_pool='
vertex_pool_capacity_prefix = '--vertex_pool_capacity='

result_output = "research_output.txt"

fetch1Step_output = "output/result_Fetch1Step.json"
result_file = open(result_output, mode='w', encoding='utf-8')

def clear_memory():
    

def init():
    os.system('ulimit -n 130000')


def start_bench():
    os.system('/usr/local/nebula/scripts/nebula.service start all')
    time.sleep(5)
    os.system('python3 run.py stress run -scenario fetch.Fetch1Step --args=\'-u 100 -d 1m\'')
    time.sleep(10)


def read_output_file(output_file):
    with open(output_file, 'r') as load_f:
        result = json.load(load_f)
        result_file.write(str(result['metrics']['latency']) + "\n")
        result_file.flush()


def change_config(rocksdb_block_cache, storage_cache_capacity, vertex_pool_capacity):
    os.system('/usr/local/nebula/scripts/nebula.service stop all')
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
        if index != len(arr) - 1:
            file.write(arr[index] + "\n")
        else:
            file.write(arr[index])
    file.close()
    time.sleep(5)


if __name__ == '__main__':
    init()
    slice_num = 1
    while slice_num <= 8:
        mem_total = slice_num * 512
        block_cache = mem_total
        while block_cache >= 0:
            vertex_pool = mem_total - block_cache
            storage_cache = int(vertex_pool * 1.2)
            change_config(block_cache, storage_cache, vertex_pool)
            result_file.write(str(block_cache) + " " + str(storage_cache) + " " + str(vertex_pool) + "\n")
            start_bench()
            read_output_file(fetch1Step_output)
            block_cache -= int(mem_total / 8)
        slice_num += 1
    result_file.close()
