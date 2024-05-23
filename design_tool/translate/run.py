# -*- coding: utf-8 -*-
from openai import OpenAI

def stream_completion(prompt):
    client = OpenAI(
    	base_url="http://localhost:4000/v1",
    	api_key="",
    )
    
    response = client.chat.completions.create(
      model="Qwen1.5-32B-Chat-GPTQ-Int4",
      messages=[
    	{"role": "user", "content": "Hello!"}
      ],
      temperature=0.7,
      stream=True,  # 这里开启流式传输
    )
    
    for chunk in response:
        # 检查是否是结束标记，如果是则跳出循环
        if chunk['choices'][0]['finish_reason'] == 'stop':
            break
        # 获取并处理当前的token
        delta = chunk['choices'][0]['delta']
        if 'content' in delta:
            print(delta['content'], end='', flush=True)

prompt = "请介绍一下人工智能的历史。"
stream_completion(prompt)
