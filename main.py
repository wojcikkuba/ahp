from flask import Flask, request, jsonify, json
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        user_name = data.get('userName', 'Unknown')
        kategorie = data.get('kategorie', [])
        warianty = data.get('warianty', [])
        answers = data['answers']

        # Grupowanie odpowiedzi według kryteriów i tworzenie macierzy AHP
        grouped_answers = {}
        grouped_matrices = {}
        for answer in answers:
            criterion = answer['criterion']
            if criterion not in grouped_answers:
                grouped_answers[criterion] = []
            grouped_answers[criterion].append(answer)

        for criterion, criterion_answers in grouped_answers.items():
            matrix = create_ahp_matrix_from_answers(criterion_answers)
            grouped_matrices[criterion] = matrix

        # Obliczenia dla każdego kryterium
        results = {}
        consistency_ratios = {}
        inconsistent_criteria = []
        for criterion, matrix in grouped_matrices.items():
            weights = calculate_priority_vector(matrix)
            results[criterion] = weights.tolist()

            # Obliczanie wskaźnika spójności
            eigenvalues, _ = np.linalg.eig(matrix)
            cr = calculate_consistency_ratio(matrix, eigenvalues)
            consistency_ratios[criterion] = cr

            if cr > 0.1:
                inconsistent_criteria.append(criterion)

        # Synteza wyników
        final_scores = np.sum([np.array(weights) for weights in results.values()], axis=0)
        best_variant = int(np.argmax(final_scores)) + 1

        # Przygotowanie struktury JSON z wynikami
        survey_results = []

        for criterion in kategorie:
            survey_result = {
                'ankieta': "Ankieta 1",  # Możesz dostosować to pole na podstawie danych wejściowych
                'kategorie': [criterion],
                'warianty': warianty,
                'najlepszy_wariant': {criterion: best_variant},
                'wyniki': []
            }

            for answer in answers:
                user_result = {
                    'uzytkownik': user_name,
                    'oceny': {criterion: results[criterion]},
                    'is_consistent': consistency_ratios[criterion] <= 0.1
                }
                survey_result['wyniki'].append(user_result)

            survey_result['scores'] = final_scores.tolist()
            survey_results.append(survey_result)

        # Odczyt i zapis do pliku JSON
        file_name = 'results.json'
        try:
            with open(file_name, 'r') as file:
                results_data = json.load(file)
        except FileNotFoundError:
            results_data = {'najlepszy_wariant': None, 'Ankiety': []}

        results_data['Ankiety'].extend(survey_results)

        # Agregacja wyników
        najlepszy_wariant = aggregate_results(results_data['Ankiety'])
        results_data['najlepszy_wariant'] = najlepszy_wariant

        with open(file_name, 'w') as file:
            json.dump(results_data, file, indent=4)

        return jsonify(survey_results)

    except ValueError:
        return jsonify({"error": "Invalid data format"}), 400


def create_ahp_matrix_from_answers(answers):
    # Funkcja tworząca macierz AHP na podstawie odpowiedzi z JSONa
    # (Zakładamy tutaj, że mamy 3 opcje, więc macierz będzie miała wymiary 3x3)
    matrix = np.ones((3, 3))
    # Mapowanie nazw wariantów do indeksów macierzy
    variant_map = {answer['varinat1']: i for i, answer in enumerate(answers)}
    variant_map.update({answer['variant2']: i for i, answer in enumerate(answers)})

    for answer in answers:
        i = variant_map[answer['varinat1']]
        j = variant_map[answer['variant2']]
        count = answer['count']
        matrix[i, j] = count
        matrix[j, i] = 1 / count if count != 0 else 1

    return matrix


def calculate_priority_vector(matrix):
    # Obliczanie wartości własnych i wektorów własnych
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_index = np.argmax(np.real(eigenvalues))
    max_eigenvector = np.real(eigenvectors[:, max_index])

    # Normalizacja wektora własnego do uzyskania wag
    return max_eigenvector / np.sum(max_eigenvector)


def calculate_consistency_ratio(matrix, eigenvalues):
    n = matrix.shape[0]
    lambda_max = np.real(np.max(eigenvalues))
    ci = (lambda_max - n) / (n - 1)  # Wskaźnik spójności (Consistency Index)
    ri = 0.58 if n == 3 else 0  # Losowy wskaźnik spójności dla macierzy 3x3
    cr = ci / ri if ri != 0 else 0  # Współczynnik spójności
    return cr


def aggregate_results(surveys):
    suma_wag = {}
    liczba_wag = {}

    # Agregacja wyników
    for ankieta in surveys:
        for kategoria, wagi in ankieta['results'].items():
            if kategoria not in suma_wag:
                suma_wag[kategoria] = np.zeros(len(wagi))
                liczba_wag[kategoria] = 0

            mnoznik = 0.5 if not ankieta['is_consistent'] else 1
            suma_wag[kategoria] += np.array(wagi) * mnoznik
            liczba_wag[kategoria] += mnoznik

    # Obliczanie średnich ważonych i wybór najlepszego wariantu
    najlepszy_wariant = {}
    for kategoria, suma in suma_wag.items():
        srednia = suma / liczba_wag[kategoria]
        najlepszy_wariant[kategoria] = np.argmax(srednia) + 1  # +1, ponieważ indeksowanie zaczyna się od 0

    return najlepszy_wariant



if __name__ == '__main__':
    app.run(debug=True)
