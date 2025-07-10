import json
# import jsonschema as js
from linkml.validator import validate

dataset_file = '../data/define-lzzt-template.json'
schema_file = './define_template.yaml'

with open(dataset_file, mode='r', encoding='utf-8') as d:
    template = json.load(d)


report = validate(template, schema="define_template.yaml", target_class="DefineTemplate")
if report.results:
    print(f'Validation failed for {dataset_file}')
    error = str(report.results[0])
    print(f"Error: {error[0:2000]}")
    # for count, result in enumerate(report.results):
    #     print(f'{result}')
    #     if count > 0:
    #         break
else:
    print("Success! The dataset is valid.")