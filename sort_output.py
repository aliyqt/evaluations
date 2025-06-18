import json

# Load the JSON file
with open("tiny_chart_result.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Load the reference file
type_data_set = {}
with open("sorted_charts_output_pew_test.txt", "r", encoding="utf-8") as file:
    for line in file:
        ref_data = json.loads(line)
        chart_type = ref_data["type"]
        for item in data:
            if item["id"] == ref_data["id"]:
                data_id = item["id"]
                actual = item["actual"].replace("\n", " ").strip()
                if chart_type not in type_data_set:
                    type_data_set[chart_type] = []
                type_data_set[chart_type].append(data_id + " | " + actual)
                break

print(len(type_data_set), type_data_set.keys())

# Split into separated files regarding chart types
for type_data in type_data_set.keys():
    count = 0
    with open("tinychart_pew_"+type_data+".txt", "w") as outfile:
        for line in type_data_set[type_data]:
            outfile.write(line+"\n")
            count += 1
    print(type_data,":",count)

# Iterate through each item and print in the desired format
output_data = []
for item in data:
    id = item["id"]
    actual = item["actual"].replace("\n", " ").strip()
    output_data.append(id + " | " + actual)

total_count = 0
with open("tinychart_pew_all.txt", "w") as outfile:
    for line in output_data:
        outfile.write(line+"\n")
        total_count += 1
print("Total:",total_count)