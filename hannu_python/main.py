import json

def getUPCFromData(data):
    result = []
    if isinstance(data, list):
        for element in data:
            result += (getUPCFromData(element))
    else:
        if 'sub_rows' in data:
            response = getUPCFromData(data['sub_rows'])
            if 'level' in data:
                result += map(lambda sub_row: sub_row | {data['level']: data['name']}, 
                            response)
            elif len(data['data']) > 0:
                result += map(lambda sub_row: sub_row | {data['data'][0]['level']: data['name']}, 
                            response)
            else:
                result += response
        elif 'data' in data:
            result += getUPCFromData(data['data'])
        else:
            result.append(data)
    return result


# Scenario of input.json where you can either query for MFF or customer using index number
with open('input.json') as input_file:
    payload = json.loads(input_file.read())

result = getUPCFromData(payload[2])

with open("output.json", "w") as outfile:
    json.dump(result, outfile, indent= 2)
    
# Scenario of old_input.json where you query for MFF using index number of data property
with open('old_input.json') as input_file:
    payload = json.loads(input_file.read())

result = getUPCFromData(payload['data'][2])

with open("old_output.json", "w") as outfile:
    json.dump(result, outfile, indent= 2)