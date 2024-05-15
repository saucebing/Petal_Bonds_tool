# python3
# 请先安装 OpenAI SDK：`pip3 install openai`
from openai import OpenAI

client = OpenAI(api_key="sk-aa169d2c7f164b10a4c4f3766d7f2fc7", base_url="https://api.deepseek.com")

stream = True

def chat(text):
    completion = client.chat.completions.create(
        model = "deepseek-chat",
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": text},
        ],
        frequency_penalty = 0,
        max_tokens = 4096,
        presence_penalty = 0,
        stop = None,
        stream = stream,
        temperature = 1,
        top_p = 1,
        logprobs = False,
        top_logprobs = None
    )


    print("Completion results:")
    if stream:
        output_token_cnt = 0
        last_completion = None
        for c in completion:
            output_token_cnt += 1
            res = c.choices[0].delta.content
            if res:
                print(res, end = '')
            last_completion = c
        print('')
        print(last_completion.usage)
    else:
        print(completion.choices[0].message.content)

if __name__ == "__main__":
    #f = open('qa_prompt.txt', 'r')
    #text = f.read()
    #f.close()
    chat("你好")
