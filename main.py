import json
import oyaml
import yaml



def update_class_name(c, oas):
    pass

oas = oyaml.load(open("./example/in/TMF648-Quote-v5.0.0.oas.yaml").read())
rules = oyaml.load(open("./example/in/TMF648_Quote.rules.yaml").read())
meta = {}
for res in rules['api']['resources']:
    excluded = []
    required = []
    if not "supportedHttpMethods" in res:
        continue
    meta[res['name']] = {}
    for meth in res['supportedHttpMethods']:

        if not "parameterRestrictions" in res['supportedHttpMethods'][meth]:
            continue
        meta[res['name']][meth] = {}
        if "excludedParameters" in res['supportedHttpMethods'][meth]['parameterRestrictions']:
            meta[res['name']][meth]['excluded'] = res['supportedHttpMethods'][meth]['parameterRestrictions']['excludedParameters']
        if "requiredParameters" in res['supportedHttpMethods'][meth]:
            meta[res['name']][meth]['required'] = res['supportedHttpMethods'][meth]['requiredParameters']


for schema in oas['components']['schemas']:

    if "required" in oas['components']['schemas'][schema]:
        del(oas['components']['schemas'][schema]['required'])
    if 'allOf' in oas['components']['schemas'][schema]:
        for i, ao in enumerate(oas['components']['schemas'][schema]['allOf']):
            if "required" in ao:
                del(ao['required'])
            oas['components']['schemas'][schema]['allOf'][i] = ao
    if "_Create" in schema:
        oas['components']['schemas'][schema.replace("_Create","_LVO")] = oas['components']['schemas'][schema]
        del(oas['components']['schemas'][schema])
        oas['components']['schemas'][schema.replace("_Create","_LVO")]['required'] = ["@type"]
    if "_Update" in schema:
        new_name = schema.replace("_Update","_UVO")
        oas['components']['schemas'][new_name] = oas['components']['schemas'][schema]
        del(oas['components']['schemas'][schema])
       
for reqBody in oas['components']['requestBodies']:
    if "content" in oas['components']['requestBodies'][reqBody]:
        for cont in oas['components']['requestBodies'][reqBody]['content']:
            if "schema" in oas['components']['requestBodies'][reqBody]['content'][cont]:
                if "$ref" in oas['components']['requestBodies'][reqBody]['content'][cont]['schema']:
                    if "_Create" in oas['components']['requestBodies'][reqBody]['content'][cont]['schema']['$ref']:
                        oas['components']['requestBodies'][reqBody]['content'][cont]['schema']['$ref'] = oas['components']['requestBodies'][reqBody]['content'][cont]['schema']['$ref'].replace('_Create', "_LVO")

                    if "_Update" in oas['components']['requestBodies'][reqBody]['content'][cont]['schema']['$ref']:
                        oas['components']['requestBodies'][reqBody]['content'][cont]['schema']['$ref'] = oas['components']['requestBodies'][reqBody]['content'][cont]['schema']['$ref'].replace('_Update', "_UVO")

print(meta)
open('example/out/TMF648-Quote-v5.0.0_PATCHED.oas.json',"w+").write(json.dumps(oas, indent=4))
open('example/out/TMF648-Quote-v5.0.0_ORIGINAL.oas.json',"w+").write(json.dumps(oyaml.load(open("./example/in/TMF648-Quote-v5.0.0.oas.yaml").read()), indent=4))