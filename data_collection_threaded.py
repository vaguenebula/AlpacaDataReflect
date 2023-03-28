import openai
import os 
import json
import time
import threading
import concurrent.futures

# Create a thread pool with a maximum of 10 worker threads
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
openai.api_key = "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"

f = open('alpaca_data_cleaned.json', encoding='utf-8')
data = json.load(f)

with open("alpaca_reflect.json", "r", encoding='utf-8') as f:
    global existing_data
    if f.read().strip() == "":
        # If the file is empty, set the existing data to an empty list
        existing_data = []
    else:
        # If the file is not empty, move the file pointer to the beginning of the file
        f.seek(0)
        # Load existing data from file
        existing_data = json.load(f)

existing_instructions = [i['instruction'] for i in existing_data]

right_index = [x for x, i in enumerate(data) if i['instruction'] == "In one sentence summarize the text."]
print(right_index)
context = """
User: [Topic or question]

Input: [Input]

Assistant Hypothetical Response: [Brief or simplified answer to the topic or question]

Agent Reflection: [Critique of the hypothetical response, highlighting the limitations, inaccuracies, or areas that need improvement or expansion, while providing guidance on how to address these issues in the revised response]

Revised Response: [The natural and contextually appropriate answer to the topic or question, as generated by the advanced language model, which incorporates the suggestions and improvements from the agent reflection for a more comprehensive and accurate response. Do not mention the ]"""

# Create a lock object
lock = threading.Lock()

def run_query(i):

    print(f"Asking {i['instruction']}")
    input = f"""
User: {i['instruction']}

Input: {i['input']}

Assistant Hypothetical Response: {i['output']}"""
    try: 

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": input},
            ]
        )

        output= response['choices'][0]['message']['content']

        # print(output)

        response_data = {
            "instruction": i['instruction'],
            "input": i['input'],
            "output": i['output'],
            "reflection": output.split("Agent Reflection:")[1].split("Revised Response:")[0],
            "corrected": output.split("Revised Response:")[1]
        }
        
        with lock:
            # Acquire the lock before accessing the shared data
            with open("alpaca_reflect.json", "w+") as f:
                existing_data.append(response_data) 
                json.dump(existing_data, f, indent=4)

    except Exception as e:
        print(e)

# Submit all tasks to the thread pool
futures = [executor.submit(run_query, i) for i in data[right_index[0]:] if i['instruction'] not in existing_instructions]

# Wait for all tasks to complete
concurrent.futures.wait(futures)

# threads = []
# for i in data[right_index[0]:]:
#     if i['instruction'] not in existing_instructions:
#         t = threading.Thread(target=run_query, args=(i,))
#         threads.append(t)
#         t.start()

# for t in threads:
#     t.join()

f.close()
