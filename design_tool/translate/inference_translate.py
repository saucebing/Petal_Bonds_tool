from openai import OpenAI
import re
from collections import OrderedDict
import threading

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

def chat(client, model, translate_dict, translate_ind):
    prompt = translate_dict[translate_ind]['prompt']
    # Completion API
    stream = True
    completion = client.chat.completions.create(
        model=model,
        messages=[
          {"role": "user", "content": prompt}
        ],
        n=1,
        stream=stream,
        temperature=0.1,
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
        translate_dict[translate_ind]['text_zh'] = total_res.strip()
        #return total_res
    else:
        print(completion)

(client, model) = get_model()
#fname = 'design_prompt.txt'
fname = 'CardText.txt'
f = open(fname, 'r')
ind = 1001000000001
lines = f.readlines()
translate_dict = OrderedDict()
translate_ind = 0
for line_ind, line in enumerate(lines):
    print('Stage prompt: %d/%d' % (line_ind, len(lines)))
    if line.strip() == '':
        continue
    else:
        prompt = line + ' 以上是一款卡牌游戏的技能描述。您是一名专业的翻译，请将以上单词或句子翻译成中文，请直接写出翻译的中文，不需要解释您的思考过程，也不需要解释结果，请不要出现“可以翻译为“，”表示”等表达，直接输出翻译结果就可以了，请保证翻译的准确性'
        text_en = line.strip()
        #prompt = 'Hello'
        translate_dict[translate_ind] = {"prompt": prompt, "text_en": text_en, 'ind': ind}
        translate_ind += 1
        ind += 1

translate_total = translate_ind
translate_ind = 0
for translate_ind in range(0, translate_total):
    print('Stage inference Begin: %d/%d' % (translate_ind, translate_total))
    prompt = translate_dict[translate_ind]['prompt']
    t = threading.Thread(target=chat, args=(client, model, translate_dict, translate_ind))
    translate_dict[translate_ind]['thread'] = t
    #res = chat(client, model, tranlate_dict, translate_ind)

for translate_ind in range(0, translate_total):
    print('Stage inference Run: %d/%d' % (translate_ind, translate_total))
    translate_dict[translate_ind]['thread'].start()

for translate_ind in range(0, translate_total):
    print('Stage inference Join: %d/%d' % (translate_ind, translate_total))
    translate_dict[translate_ind]['thread'].join()

f2 = open('CardText.csv', 'w')
for translate_ind in range(0, translate_total):
    ind = translate_dict[translate_ind]['ind']
    text_en = translate_dict[translate_ind]['text_en']
    pat = re.compile(r'<t>(.*)</t>')
    text_zh = translate_dict[translate_ind]['text_zh']
    #print('text_zh: ', text_zh)
    #text_zh2 = pat.findall(text_zh)[0]
    translated = '"%s",%d,"%s","%s"' % (text_en, ind, text_zh, text_en)
    print(translated)
    
    f2.write(translated + '\n')
    #f2.write(text_zh + '\n')
    #print(res)

f2.close()
f.close()
