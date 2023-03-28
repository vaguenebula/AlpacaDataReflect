import json

f = open('alpaca_reflect.json', 'r', encoding='utf-8')

data = json.load(f)

bad_phrases = ['Here\'s a revised', 'Here is a revised', 'Here is the revised', 'updated code', 'revised response', 'more comprehensive', 'N/A',
               'updated response', 'Here\'s an updated snippet', 'This updated version', 'revised program', 'agent reflection',
               'Here is a more detailed', 'suggested improvements']

bad_data = []
for eachEntry in data:
    # print(eachEntry)
    output = eachEntry['corrected']

    for eachPhrase in bad_phrases:
        if eachPhrase.lower() in output.lower():
            bad_data.append(output)
            break
        elif 'here is a more' in output.lower() and 'there is a more' not in output:
            bad_data.append(output)
            break

for x in bad_data:
    print(x)

print(len(bad_data))