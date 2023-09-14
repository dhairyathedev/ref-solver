from flask import Flask, render_template, request
from fractions import Fraction
import numpy as np

app = Flask(__name__)


def row_echelon_form(matrix):
    m, n = matrix.shape
    steps = []

    for col in range(n):
        # Find the pivot row
        pivot_row = -1
        for row in range(col, m):
            if matrix[row, col] != 0:
                pivot_row = row
                break

        if pivot_row == -1:
            continue  # No pivot element in this column, move to the next column

        # Swap the pivot row with the current row (if needed)
        if pivot_row != col:
            matrix[[pivot_row, col]] = matrix[[col, pivot_row]]
            steps.append(f"Swap rows {pivot_row + 1} and {col + 1}:")

        # Make the pivot element 1
        pivot_element = matrix[col, col]
        if pivot_element != 1:
            matrix[col] /= pivot_element
            steps.append(f"Scale row {col + 1} by {Fraction(1 / pivot_element).limit_denominator()}:")

        # Eliminate all entries below the pivot
        for row in range(col + 1, m):
            factor = matrix[row, col]
            if factor != 0:
                matrix[row] -= factor * matrix[col]
                steps.append(f"Subtract {factor} times row {col + 1} from row {row + 1}:")

    return matrix, steps


@app.route("/", methods=["GET", "POST"])
def index():
    matrix = np.array([
        [1, 2, 3],
        [3, 4, 4],
        [7, 20, 12]
    ], dtype=float)

    # Initialize rows and cols with default values
    rows = matrix.shape[0]
    cols = matrix.shape[1]

    if request.method == "POST":
        try:
            rows = int(request.form["rows"])
            cols = int(request.form["cols"])

            matrix = np.zeros((rows, cols), dtype=float)

            for i in range(rows):
                for j in range(cols):
                    key = f"element_{i}_{j}"
                    matrix[i][j] = float(request.form[key])

        except Exception as e:
            error_message = f"Error processing matrix: {str(e)}"
            return render_template("index.html", matrix=matrix, error_message=error_message)

    matrix_copy = matrix.copy()
    matrix_ref, steps = row_echelon_form(matrix_copy)

    return render_template("index.html", matrix=matrix, matrix_ref=matrix_ref, steps=steps, rows=rows, cols=cols)


if __name__ == "__main__":
    app.run(debug=True)
