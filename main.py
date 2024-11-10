import random
from functools import reduce
from flask import Flask, jsonify, request


app = Flask(__name__)

plants = [
    {
        'item_id': 1,
        'title': 'Aloe Vera',
        'description': 'Aloe Vera benötigt wenig Wasser und bevorzugt helle, indirekte Sonnenstrahlen. Ideal für trockene Bedingungen.',
    },
    {
        'item_id': 2,
        'title': 'Ficus Benjamina',
        'description': 'Der Ficus Benjamina bevorzugt helle, indirekte Sonne und eine moderate Luftfeuchtigkeit. Bewässerung sollte regelmäßig, aber sparsam erfolgen.',
    },
    {
        'item_id': 3,
        'title': 'Monstera Deliciosa',
        'description': 'Die Monstera Deliciosa wächst am besten in hellen bis schattigen Bereichen und benötigt eine gleichmäßige Bewässerung.',
    },
    {
        'item_id': 4,
        'title': 'Lavendel',
        'description': 'Lavendel liebt direktes Sonnenlicht und trockene Erde. Er ist pflegeleicht und benötigt wenig Wasser.',
    },
    {
        'item_id': 5,
        'title': 'Basilikum',
        'description': 'Basilikum benötigt viel Licht und regelmäßig feuchte Erde. Perfekt für sonnige Fensterbänke.',
    },
    {
        'item_id': 6,
        'title': 'Sukkulenten-Mix',
        'description': 'Sukkulenten benötigen wenig Wasser und viel Sonnenlicht. Sie sind ideal für warme und trockene Orte.',
    },
    {
        'item_id': 7,
        'title': 'Orchidee',
        'description': 'Orchideen mögen indirektes Licht und hohe Luftfeuchtigkeit. Gießen Sie sie sparsam, um Wurzelfäule zu vermeiden.',
    },
    {
        'item_id': 8,
        'title': 'Farn',
        'description': 'Farne bevorzugen feuchte Umgebungen und wenig direktes Licht. Perfekt für Badezimmer oder schattige Räume.',
    },
]


def get_plants(plant, item_id):
    return any(plant['item_id'] == item_id for plant in plants)

@app.route('/plants', methods=['GET'])
def get_all_plants():
    return jsonify(plants), 200

def get_random_plant(plantso):
    return random.choice(plantso)

@app.route('/plants/random', methods=['GET'])
def random_plant():
    plant = get_random_plant(plants)
    return jsonify(plant), 200

@app.route('/plants/<int:item_id>', methods=['GET'])
def find_plant_by_id(item_id):
    for plant in plants:
        if plant['item_id'] == item_id:
            return jsonify(plant), 200

    return jsonify({'error': 'Pflanze nicht gefunden'}), 404


@app.route('/plants/description/<int:item_id>', methods=['GET'])
def get_plant_description(item_id):
    plant = next((plant for plant in plants if plant['item_id'] == item_id), None)
    description = (lambda p: p['description'] if p else 'Pflanze nicht gefunden.')(plant)
    return jsonify({'description': description}), 200


@app.route('/plants/sorted', methods=['GET'])
def sorted_plants():
    sorted_plants = sorted(plants, key=lambda x: x['title'])
    return jsonify(sorted_plants), 200

@app.route('/plants/sorted_by_word/<string:word>', methods=['GET'])
def sort_plants_by_word(word):
    sorted_plants = sorted(
        plants,
        key=lambda plant: plant['description'].lower().find(word.lower()) if word.lower() in plant['description'].lower() else float('inf')
    )
    return jsonify(sorted_plants), 200


@app.route('/plants/filtered', methods=['GET'])
def filtered_plants():
    filtered = tuple(filter(lambda plant: 'licht' in plant['description'].lower(), plants))
    return jsonify(filtered), 200

@app.route('/plants/filtered/<string:search_term>', methods=['GET'])
def filtered_plants_wort(search_term):
    filtered = tuple(filter(lambda plant: search_term.lower() in plant['description'].lower(), plants))
    return jsonify(filtered), 200


@app.route('/plants/combined', methods=['GET'])
def combined_operations():
    filtered_plantso = filter(lambda plant: 'licht' in plant['description'].lower(), plants)
    mapped_titles = map(lambda plant: plant['title'].upper(), filtered_plantso)
    total_length = reduce(lambda acc, title: acc + len(title), mapped_titles, 0)

    return jsonify({'total_title_length': total_length}), 200


@app.route('/plants/aggregate', methods=['GET'])
def aggregate_data():
    filtered_plantse = filter(lambda plant: 'licht' in plant['description'].lower(), plants)
    mapped_titles = map(lambda plant: plant['title'].upper(), filtered_plantse)
    total_title_length = reduce(lambda acc, title: acc + len(title), mapped_titles, 0)

    return jsonify({'total_title_length': total_title_length}), 200

@app.route('/plants/create', methods=['POST'])
def create_plant():
    data = request.json
    title = data.get('title')
    description = data.get('description')

    new_plant = create_plant_with_kwargs(title, description,
                                         **{k: v for k, v in data.items() if k not in ['title', 'description']})
    plants.append(new_plant)

    return jsonify(new_plant), 201


def create_plant_with_kwargs(title, description, **kwargs):
    plant = {
        'item_id': len(plants) + 1,
        'title': title,
        'description': description,
    }
    plant.update(kwargs)
    return plant


def transform_plants(plant_list, transform_func):
    return [transform_func(plant) for plant in plant_list]

def plant_summary(plant):
    return {
        'title': plant['title'],
        'description': plant['description']
    }

@app.route('/plants/summaries', methods=['GET'])
def plant_summaries():
    summaries = transform_plants(plants, plant_summary)
    return jsonify(summaries), 200


if __name__ == "__main__":
    app.run()
