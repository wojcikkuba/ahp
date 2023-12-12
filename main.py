from flask import Flask, request, jsonify, json
import numpy as np

from flask_cors import CORS
# from itertools import combinations

app = Flask(__name__)
CORS(app)

survey_count = 0

@app.route('/data', methods=['GET'])
def get_data():
    try:
        with open('results.json', 'r') as file:
            data = json.load(file)
            return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


@app.route('/calculate', methods=['POST'])
def calculate():
    new_data = request.get_json()
    user_name = new_data.get('userName', 'Unknown')
    new_answers = new_data.get('answers', [])

    if not new_answers:
        return jsonify({"error": "No answers provided"}), 400

    try:
        with open('results.json', 'r') as file:
            results_data = json.load(file)
    except FileNotFoundError:
        results_data = []

    # Sprawdzenie, czy istnieje ankieta z takimi samymi kryteriami i wariantami
    current_survey = None
    for survey in results_data:
        if set(survey['kategorie']) == set(answer['criterion'] for answer in new_answers) and \
           set(survey['warianty']) == set(answer['variant1'] for answer in new_answers) | set(answer['variant2'] for answer in new_answers):
            current_survey = survey
            break

    if not current_survey:
        current_survey = create_new_survey_structure()
        results_data.append(current_survey)

    update_survey_with_new_answers(current_survey, user_name, new_answers)

    last_user_result = current_survey['wyniki'][-1]
    if not last_user_result["is_consistent"]:
        return jsonify({"error": "Inconsistent answers provided"}), 400

    aggregate_results(current_survey)

    with open('results.json', 'w') as file:
        json.dump(results_data, file, indent=4)

    return jsonify(results_data)

def create_new_survey_structure():
    global survey_count
    survey_count += 1
    return {
        "ankieta": f"Ankieta {survey_count}",
        "kategorie": [],
        "warianty": [],
        "najlepszy_wariant": {},
        "wyniki": []
    }

def update_survey_with_new_answers(survey, user_name, new_answers):
    user_result = {
        "uzytkownik": user_name,
        "oceny": {kategoria: [] for kategoria in survey['kategorie']},
        "is_consistent": True
    }

    for answer in new_answers:
        criterion = answer['criterion']
        user_result["oceny"].setdefault(criterion, []).append(answer)

        if criterion not in survey['kategorie']:
            survey['kategorie'].append(criterion)

        if answer['variant1'] not in survey['warianty']:
            survey['warianty'].append(answer['variant1'])
        if answer['variant2'] not in survey['warianty']:
            survey['warianty'].append(answer['variant2'])

    for kategoria in survey['kategorie']:
        matrix = np.ones((len(survey['warianty']), len(survey['warianty'])))
        for answer in user_result["oceny"].get(kategoria, []):
            idx1 = survey['warianty'].index(answer['variant1'])
            idx2 = survey['warianty'].index(answer['variant2'])
            count = answer['count']
            matrix[idx1, idx2] = count
            matrix[idx2, idx1] = 1 / count if count != 0 else 1

        cr = calculate_consistency_ratio(matrix)
        if cr >= 0.1:
            user_result["is_consistent"] = False
            break   

    survey['wyniki'].append(user_result)

def aggregate_results(survey):
    kategorie = survey['kategorie']
    warianty = survey['warianty']
    survey['scores'] = [0] * len(warianty)

    for kategoria in kategorie:
        matrix = np.ones((len(warianty), len(warianty)))

        for user_result in survey['wyniki']:
            weight = 0.5 if not user_result['is_consistent'] else 1
            for answer in user_result["oceny"].get(kategoria, []):
                idx1 = warianty.index(answer['variant1'])
                idx2 = warianty.index(answer['variant2'])
                count = answer['count'] * weight
                matrix[idx1, idx2] *= count
                matrix[idx2, idx1] *= 1 / count if count != 0 else 1

        weights = calculate_priority_vector(matrix)
        best_variant_index = np.argmax(weights)
        survey['najlepszy_wariant'][kategoria] = warianty[best_variant_index]
        for idx, weight in enumerate(weights):
            survey['scores'][idx] += weight

    # Konwersja scores do średniej ważonej dla każdego wariantu
    survey['scores'] = [score / len(kategorie) for score in survey['scores']]

def calculate_priority_vector(matrix):
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_eigval_index = np.argmax(eigvals)
    max_eigvec = np.real(eigvecs[:, max_eigval_index])
    return max_eigvec / max_eigvec.sum()

def calculate_consistency_ratio(matrix):
    n = matrix.shape[0]
    eigvals, _ = np.linalg.eig(matrix)
    lambda_max = np.max(np.real(eigvals))
    ci = (lambda_max - n) / (n - 1)
    ri = [0, 0, 0.58, 0.9][n-1]  # Przykładowe wartości RI
    return ci / ri if ri != 0 else 0

if __name__ == '__main__':
    app.run(debug=True)