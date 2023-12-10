from flask import Flask, request, jsonify, json
import numpy as np

app = Flask(__name__)


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        answers = data['answers']

        # Grupowanie odpowiedzi według kryteriów
        grouped_answers = {}
        for answer in answers:
            criterion = answer['criterion']
            if criterion not in grouped_answers:
                grouped_answers[criterion] = []
            grouped_answers[criterion].append(answer)

        results = {}
        for criterion, criterion_answers in grouped_answers.items():
            # Tworzenie macierzy AHP dla danego kryterium
            matrix = create_ahp_matrix_from_answers(criterion_answers)
            # Obliczanie wag priorytetowych
            weights = calculate_priority_vector(matrix)
            results[criterion] = weights.tolist()

        # Synteza wyników
        final_scores = np.sum([np.array(weights) for weights in results.values()], axis=0)
        best_variant = int(np.argmax(final_scores)) + 1  # Konwersja na typ podstawowy Pythona

        # Odczyt i zapis do pliku JSON
        file_name = 'C:/Users/kuba0/OneDrive/Desktop/results.json'
        user_name = data.get('userName', 'Unknown')  # pobieranie nazwy użytkownika z danych JSON

        try:
            # Odczytanie istniejących danych z pliku, jeśli plik istnieje
            try:
                with open(file_name, 'r') as file:
                    results_data = json.load(file)
            except FileNotFoundError:
                results_data = {}

            # Dodanie nowych wyników
            results_data[user_name] = {
                'best_variant': best_variant,
                'results': {criterion: np.array(weights).tolist() for criterion, weights in results.items()},
                'scores': final_scores.tolist()
            }

            # Zapisanie zmodyfikowanych danych do pliku
            with open(file_name, 'w') as file:
                json.dump(results_data, file, indent=4)

        except Exception as e:
            return jsonify({"error": f"Error writing to file: {str(e)}"}), 500

        # Zwracanie wyników jako odpowiedź API
        return jsonify({
            'best_variant': best_variant,
            'scores': final_scores.tolist(),  # Konwersja na listę typów podstawowych
            'results': {criterion: np.array(weights).tolist() for criterion, weights in results.items()}
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


if __name__ == '__main__':
    app.run(debug=True)
