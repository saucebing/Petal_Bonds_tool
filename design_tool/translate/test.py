import argparse
import json
import logging as logger
import os
import random
import sys
import threading
import time

import requests
from openai import OpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

url = 'http://0.0.0.0:4000/stream'
headers = {"User-Agent": "Test Client"}

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:4000/v1"

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai_api_key,
    base_url=openai_api_base,
)


models = client.models.list()
print(models)
model = models.data[0].id

def data_loader(path: str):
    """
    load
    :param path: 样本路径
    :return:
    """
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = json.load(f)
            return data
    else:
        logger.info(f'该数据文件的路径{path}不存在.')
        return None


def output_result_dir(filename, result_list, output_dir):
    result_path = os.path.join(output_dir, filename)
    result_df = pd.DataFrame(result_list)
    result_df.to_csv(result_path)


def calc_infer_tokens_sec(test_data_path: str, total_result: dict):
    current_thread = threading.current_thread()
    thread_name = current_thread.name

    time_total = 0
    token_num_total = 0
    first_time_list = []

    user_input = "你好"
    #test_data = data_loader(test_data_path)
    prompt = f"A chat between a curious user and an artificial intelligence assistant named Security GPT, " \
             f"which is trained by 深信服科技(Sangfor Technologies) using massive data in the fields of " \
             f"computer science and network security. The Security GPT gives helpful, detailed, and " \
             f"polite answers to the user's questions. USER: {user_input}. Assistant: "
    # 获取所有的键并随机打乱它们的顺序
    #keys = list(test_data.keys())
    #random.shuffle(keys)
    #for _ in test_data:
    for _ in range(0, 1):
        #random_key = keys.pop()  # 从列表末尾移除一个键并返回它
        #text = prompt + test_data[random_key]
        text = prompt
        print(f'输入： {text}\n')
        t_flag = False
        output_token_len = 0
        data = {
            #"model": "/mnt/afs/data/model/open_source_data/Qwen/Qwen1.5-32B-Chat/",
            #"model": model,
            "stream": True,
            "metrics": False,
            "n": 1,
            #"stop_token_ids": [7],
            #"max_tokens": 2048,
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ]
        }
        start_time = time.time()
        response = requests.post(url, headers=headers, json=data, stream=True)
        total_rsp = ''
        for line in response.iter_lines(delimiter=b"\n", decode_unicode=False, ):
            if len(line) == 0:
                continue
            output_token_len += 1
            lines = line.decode("utf-8").replace('\x00', '').replace('\\n\\n', '\\n')
            # 去掉"data: "前缀
            print(f"lines = {lines}")
            json_data = lines.split("data: ")[1]
            # 解析JSON字符串
            try:
                data = json.loads(json_data)
            except:
                data = {}
            # 提取choices列表
            choices = data.get("choices", [])
            # 遍历choices列表，提取每个元素的delta字典中的content值
            contents = [choice["delta"]["content"] for choice in choices if
                        "delta" in choice and "content" in choice["delta"]]
            # 打印一个线程的模型推理输出，避免串流
            if thread_name == "thread-0" and len(contents) > 0:
                print(contents[0], end='')
            if not t_flag and len(contents) > 0:
                first_time = time.time()
                first_time_list.append(first_time - start_time)
                print(f"开始输出时间：{first_time - start_time}")  # 输出第一个字符的时间
                t_flag = True

        end_time = time.time()
        print(f"整体输出时间：{end_time - start_time} ")
        total = end_time - start_time
        print("output token : ", output_token_len)
        print("total token / s : ", output_token_len / total)

        print(f"-----------------------------------------------------\n")

        if output_token_len > 0:
            print(f"该问题的推理耗时：{total} s\n")
            print(f"该问题的推理速度：{output_token_len / (end_time - start_time)} token/s\n")

            time_total += end_time - start_time
            token_num_total += output_token_len
    throughput = token_num_total / time_total
    print(f"线程名: {thread_name}，平均吞吐：{throughput}token/s\n")
    print(f"每组问答首字符耗时：{first_time_list}\n")
    if not first_time_list:
        return
    print("平均首token时延: ", sum(first_time_list) / len(first_time_list))

    total_result[thread_name] = {
            "线程名": thread_name,
            "吞吐token/s": throughput,
            "每组首字符耗时": first_time_list,
            "平均首token时延": sum(first_time_list) / len(first_time_list),
        }


def stream_chat(args: argparse.Namespace):
    results = {}
    threads = []
    # 根据并行推理数量，创建子线程推理
    for idx in range(0, args.batch_size):
        t = threading.Thread(
            target=calc_infer_tokens_sec, name=f"thread-{idx}",
            args=(args.dataset, results)
        )
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\n***************  TEST OVER  ***************\n")
    total_throughput = 0.0
    avg_first_token_delay = 0.0
    for result in results.values():
        total_throughput += result["吞吐token/s"]
        avg_first_token_delay += result["平均首token时延"]/len(results)
    print(f"测试总吞吐为{total_throughput} tokens/s")
    print(f"测试平均首token时延为{avg_first_token_delay} s")
    # 输出测试结果至CSV
    filename = f"stream_chat_csv_batch{args.batch_size}.csv"
    #output_result_dir(filename, list(results.values()), args.output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmark the online serving throughput.")
    parser.add_argument("--dataset", type=str, required=False,
                        help="Path to the dataset.")
    parser.add_argument("--output_dir", type=str, required=False, default='./',
                        help="Path to save the results.")
    parser.add_argument("--batch_size", type=int, default=1,
                        help="Number of requests per second.")
    args = parser.parse_args()
    stream_chat(args)
    time.sleep(5)
