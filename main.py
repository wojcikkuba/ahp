from flask import Flask, request, jsonify, json
import numpy as np

app = Flask(__name__)


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
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
        for criterion, matrix in grouped_matrices.items():
            weights = calculate_priority_vector(matrix)
            results[criterion] = weights.tolist()

            # Obliczanie wskaźnika spójności
            eigenvalues, _ = np.linalg.eig(matrix)
            CR = calculate_consistency_ratio(matrix, eigenvalues)
            consistency_ratios[criterion] = CR

        # Sprawdzanie, czy którykolwiek CR przekracza próg 0.1
        inconsistent_criteria = [criterion for criterion, CR in consistency_ratios.items() if CR > 0.1]
        if inconsistent_criteria:
            return jsonify({"error": "Inconsistent answers for criteria: " + ", ".join(inconsistent_criteria)}), 400

        # Synteza wyników
        final_scores = np.sum([np.array(weights) for weights in results.values()], axis=0)
        best_variant = int(np.argmax(final_scores)) + 1

        # Odczyt i zapis do pliku JSON
        file_name = 'results.json'
        user_name = data.get('userName', 'Unknown')  # pobieranie nazwy użytkownika z danych JSON

        try:
            # Odczytanie istniejących danych z pliku, jeśli plik istnieje
            with open(file_name, 'r') as file:
                results_data = json.load(file)
        except FileNotFoundError:
            results_data = {}

        # Dodanie nowych wyników
        results_data[user_name] = {
            'best_variant': best_variant,
            'results': results,
            'scores': final_scores.tolist(),
            'consistency_ratios': consistency_ratios
        }

        # Zapisanie zmodyfikowanych danych do pliku
        with open(file_name, 'w') as file:
            json.dump(results_data, file, indent=4)

        # Zwracanie wyników jako odpowiedź API
        return jsonify({
            'best_variant': best_variant,
            'scores': final_scores.tolist(),
            'results': results,
            'consistency_ratios': consistency_ratios
        })

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


if __name__ == '__main__':
    app.run(debug=True)
