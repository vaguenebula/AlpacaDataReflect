import json
from tqdm import tqdm

f = open('alpaca_reflect.json', 'r', encoding='utf-8')
data = json.load(f)

bad_phrases = ['Here\'s a revised', 'Here is a revised', 'Here is the revised', 'Here\'s the revised', 'updated code', 'revised response', 'more comprehensive', 'N/A',
               'updated response', 'Here\'s an updated snippet', 'This updated version', 'revised program', 'agent reflection',
               'Here is a more detailed', 'suggested improvements', 'hypothetical response', 'no revisions needed', 'no revision needed',
               'no revision necessary', 'here is a more', 'Here is an updated list', 'Here\'s an updated list', 'Here are some additional',
               'Here\'s an upgraded', 'Here\'s an improved', 'Here is an improved', 'Agent\'s Reflection', 'Here is an updated',
               'Here\'s an updated', 'improvements needed', 'n/a', 'original response', 'hypothetical response', 'revised',
               'updated function', 'updated algorithm', 'this updated']

def test(word):
    y=0
    for eachEntry in data:
        if word.lower() in eachEntry['corrected'].lower():
            print(eachEntry['corrected'])
            y+=1 
    print(f"{y} instances found")

def prune_data():
    bad_data = []
    for eachEntry in tqdm(data):
        reflection = eachEntry['reflection']
        corrected = eachEntry['corrected']
        while reflection[0] == " " or reflection[0] == "\n":
            reflection = reflection[1:]    
        while reflection[-1] == " " or reflection[-1] == "\n":
            reflection = reflection[:-1]  
        while corrected[0] == " " or corrected[0] == "\n":
            corrected = corrected[1:]

        eachEntry['reflection'] = reflection
        eachEntry['corrected'] = corrected
        for eachPhrase in bad_phrases:
            if eachPhrase.lower() in corrected.lower():
                bad_data.append(eachEntry)
                break
            
    print(f"Pruned {len(bad_data)} bad entries")
    return bad_data


bad = prune_data()
for eachBad in bad:
    data.remove(eachBad)

print(f"{len(data)} total revisions")

with open('alpaca_data_cleaned.json', 'r', encoding='utf-8') as file:
    original_data = json.load(file)
    data_instructions = [i['instruction'] for i in data]
    for eachEntry in original_data:
        if eachEntry['instruction'] not in data_instructions:
            response_data = {
            "instruction": eachEntry['instruction'],
            "input": eachEntry['input'],
            "output": eachEntry['output'],
            "reflection": None,
            "corrected": None,
        }
            data.append(response_data)
        
with open("alpaca_reflect_pruned.json", "w") as f:
    json.dump(data, f, indent=4)

