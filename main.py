from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)


@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Tworzenie macierzy AHP dla każdego kryterium
        matrix_cena = create_ahp_matrix(
            float(request.form['cena_vw_audi']),
            float(request.form['cena_vw_skoda']),
            float(request.form['cena_audi_skoda'])
        )

        matrix_osiagi = create_ahp_matrix(
            float(request.form['osiagi_vw_audi']),
            float(request.form['osiagi_vw_skoda']),
            float(request.form['osiagi_audi_skoda'])
        )

        matrix_wyglad = create_ahp_matrix(
            float(request.form['wyglad_vw_audi']),
            float(request.form['wyglad_vw_skoda']),
            float(request.form['wyglad_audi_skoda'])
        )

        # Obliczanie wag priorytetowych dla każdej macierzy
        wagi_cena = calculate_priority_vector(matrix_cena)
        wagi_osiagi = calculate_priority_vector(matrix_osiagi)
        wagi_wyglad = calculate_priority_vector(matrix_wyglad)

        # Synteza wyników
        final_scores = wagi_cena + wagi_osiagi + wagi_wyglad
        best_variant = np.argmax(final_scores) + 1  # +1, ponieważ indeksowanie zaczyna się od 0

    except ValueError:
        return "Proszę wprowadzić poprawne wartości liczbowe.", 400

    # Przekazywanie wyników do szablonu HTML
    return render_template(
        'results.html',
        best_variant=best_variant,
        scores=final_scores,
        matrix_cena=matrix_cena,
        wagi_cena=wagi_cena,
        matrix_osiagi=matrix_osiagi,
        wagi_osiagi=wagi_osiagi,
        matrix_wyglad=matrix_wyglad,
        wagi_wyglad=wagi_wyglad
    )


def create_ahp_matrix(a, b, c):
    # Tworzenie macierzy AHP na podstawie wprowadzonych ocen
    return np.array([
        [1, a, b],
        [1 / a, 1, c],
        [1 / b, 1 / c, 1]
    ])


def calculate_priority_vector(matrix):
    # Obliczanie wartości własnych i wektorów własnych
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_eigenvector = eigenvectors[:, np.argmax(eigenvalues)]

    # Normalizacja wektora własnego do uzyskania wag
    return max_eigenvector / np.sum(max_eigenvector)


if __name__ == '__main__':
    app.run(debug=True)
