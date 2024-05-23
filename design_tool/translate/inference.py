from openai import OpenAI
import re

# Modify OpenAI's API key and API base to use vLLM's API server.
def get_model():
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
    return (client, model)

def chat(client, model, prompt):
    # Completion API
    stream = True
    completion = client.chat.completions.create(
        model=model,
        messages=[
          {"role": "user", "content": prompt}
        ],
        n=1,
        stream=stream,
        temperature=0.3,
        presence_penalty=1.0,
        frequency_penalty=1.0,
        max_tokens=512)

    print("Completion results:")
    total_res = ""
    if stream:
        output_token_cnt = 0
        last_completion = None
        for c in completion:
            output_token_cnt += 1
            res = c.choices[0].delta.content
            if res:
                print(res, end = '')
                total_res += res
            last_completion = c
        print('')
        print(last_completion.usage)
        return total_res
    else:
        print(completion)

(client, model) = get_model()
#fname = 'design_prompt.txt'
fname = 'qa_prompt.txt'
f = open(fname, 'r')
prompt = f.read()

pattern = r'.*回答：(.*?)；?亲密度：(.).*'
pat = re.compile(pattern)
for i in range(0, 1):
    res = chat(client, model, prompt)
    t = pat.findall(res)
    print(t)
