import openai
import os 
import json
import time
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

# f_aug = open('alpaca_reflect.json', 'w+', encoding='utf-8')
existing_instructions = [i['instruction'] for i in existing_data]

# right_index = [x for x, i in enumerate(data) if i['instruction'] == "Name one example of a non-human primate"]
context = """
You are a helpful assistant that is given a Question/Command, a corresponding input, and an answer. You reflect thoughtfully on the answer given and how it can be improved. Then, you provide a new response based on your reflection. If the answer cannot be improved, corrected answer should be N/A.
Your response must adhere to the following format:
Reflection: 
{reflection}
Corrected Answer:
{corrected answer}"""

for i in data:
    if i['instruction'] not in existing_instructions:
        print(f"Asking {i['instruction']}")
        input = f"""
Question: 
{i['instruction']} Input: "{i['input']}"

Answer: 
{i['output']}"""
        try: 

            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": input},
                ]
            )
            print(context)
            print(input)

            output= response['choices'][0]['message']['content']

            print(output)


        
            response_data = {
                "instruction": i['instruction'],
                "input": i['input'],
                "output": i['output'],
                "reflection": output.split("Reflection:")[1].split("Corrected Answer:")[0],
                "corrected": output.split("Corrected Answer:")[1]
            }
            
            

            with open("alpaca_reflect.json", "w+") as f:
                existing_data.append(response_data) 
                json.dump(existing_data, f, indent=4)

        except Exception as e:
            print(e)
        
    else:
        print("Skipping\n")
        
f.close()
