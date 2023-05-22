import json


def new_recipe_parser(data):
    # title, ingredients, instructions for preparation, cook time and relevant tags
    parsing_result = {}
    errors = {}
    for key in ['title', 'ingredients', 'instructions', 'cook_time', 'tags']:
        if key not in data:
            errors[key] = f'{key} is required'
            continue
        parsing_result[key] = str(data['key'])

    if errors != {}:
        return errors, parsing_result

    if not parsing_result['cook_time'].isdecimal():
        errors['cook_time'] = 'cook_time must be integer'
    else:
        parsing_result['cook_time'] = int(parsing_result['cook_time'])

    try:
        parsing_result['tags'] = json.loads(parsing_result['tags'])
        if not isinstance(parsing_result['tags'], list):
            errors['tags'] = 'tags must be array'
    except json.JSONDecodeError:
        errors['tags'] = 'tags must be integer array'

    return errors, parsing_result
