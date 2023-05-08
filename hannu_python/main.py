import json

def getUPCFromData(data, schema = []):
    result = []
    if isinstance(data, list):
        for element in data:
            result += getUPCFromData(element, schema)
    else:
        if 'sub_rows' in data or 'subRows' in data:
            if 'sub_rows' in data:
                sub_rows = 'sub_rows'
            else:
                sub_rows = 'subRows'
                
            if len(data[sub_rows]) == 0:
                return []
            if len(schema) > 0:
                result += map(lambda sub_row: sub_row | {schema[0]: data['name']}, 
                            getUPCFromData(data[sub_rows], schema[1:]))
            else:
                result += getUPCFromData(data[sub_rows], [])
        else:
            result.append(data)
    return result


with open('inputs\\1.json') as infile_1, open("outputs\\1.json", "w") as outfile_1, \
open('inputs\\2.json') as infile_2, open("outputs\\2_1.json", "w") as outfile_2_1, open("outputs\\2_2.json", "w") as outfile_2_2, \
open('inputs\\3.json') as infile_3, open("outputs\\3.json", "w") as outfile_3, \
open('inputs\\4.json') as infile_4, open("outputs\\4.json", "w") as outfile_4, \
open('inputs\\5.json') as infile_5, open("outputs\\5.json", "w") as outfile_5:
    # Just reading the files
    payload_1 = json.loads(infile_1.read())
    payload_2 = json.loads(infile_2.read())
    payload_3 = json.loads(infile_3.read())
    payload_4 = json.loads(infile_4.read())
    payload_5 = json.loads(infile_5.read())
    
    #Some setup
    general_schema = ["mff", "sub_mff"]
    lock_stock_schema = ["upc"]
    
    # Real Magic
    # General Component
    result_1 = getUPCFromData(payload_1, general_schema) 
    result_2_1 = getUPCFromData(payload_2[1], general_schema) # Here we need to send the index depending on MFF and general schema, it would be needed
    result_2_2= getUPCFromData(payload_2[2], []) # Here we send the index for Customer and no schema is needed.
    result_3 = getUPCFromData(payload_3, general_schema)
    
    # Demand to capacity component
    result_4 = getUPCFromData(payload_4, [])
    # Lock stock by site component
    result_5 = getUPCFromData(payload_5, lock_stock_schema) 
    
    #Just writing the output
    json.dump(result_1, outfile_1, indent= 2)
    json.dump(result_2_1, outfile_2_1, indent= 2)
    json.dump(result_2_2, outfile_2_2, indent= 2)
    json.dump(result_3, outfile_3, indent= 2)
    json.dump(result_4, outfile_4, indent= 2)
    json.dump(result_5, outfile_5, indent= 2)