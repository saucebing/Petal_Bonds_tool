import os
import datetime
from openai import OpenAI

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:4000/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


def qwen_chat_api(messages, model=None, tokenizer=None):
    chat_response = client.chat.completions.create(
        model="myvllm",
        #model="Qwen1.5-32B-Chat-GPTQ-Int4",
        messages=messages
    )
    response = chat_response.choices[0].message.content
    return response


def data_loader():
    df = pd.read_excel('Prompt_incident_read_qwen.xlsx', usecols=['prompt'], engine='openpyxl')
    prompt_list = df['prompt'].tolist()

    return prompt_list


if __name__ == "__main__":
    #prompt_list = data_loader()
    result_list = []
    idx = 0
    if True:
    #for prompt in prompt_list:
        #j = idx + 2
        #idx += 1
        #if j not in [2,6,7,10,11,12,13,14,15,16,18,20,21,22,25,26,30]:
        #    continue
        #prompt = "你好！"
        prompt = open('qa_prompt.txt', 'r').read()
        messages = [{'role': 'user', 'content': prompt}]
        start_time = datetime.datetime.now()
        try:
            pred_res_gpt4 = qwen_chat_api(messages)
        except Exception as e:
            print(f"An error occurred: {e}")
            pred_res_gpt4 = ''
        end_time = datetime.datetime.now()
        print("耗时：{}".format(end_time - start_time))
        #print(f"{j} \n {pred_res_gpt4}")
        print(f"\n {pred_res_gpt4}")
        # idx += 1
        result_list.append({
            "question": prompt,
            "answer": pred_res_gpt4
        })

    #result_path = os.path.join('./', "openai-72B-QPTQ-4bit.csv")
    #result_df = pd.DataFrame(result_list)
    #result_df.to_csv(result_path)

