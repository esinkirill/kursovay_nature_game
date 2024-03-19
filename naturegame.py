# -*- coding: windows-1251 -*-

import tkinter as tk
from tkinter import ttk, messagebox

class MatrixGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Game")


        self.rows_label = ttk.Label(root, text="Строки:")
        self.rows_label.grid(row=0, column=0, padx=10, pady=10)

        self.rows_entry = ttk.Entry(root)
        self.rows_entry.grid(row=0, column=1, padx=10, pady=10)

        self.cols_label = ttk.Label(root, text="Столбцы:")
        self.cols_label.grid(row=1, column=0, padx=10, pady=10)

        self.cols_entry = ttk.Entry(root)
        self.cols_entry.grid(row=1, column=1, padx=10, pady=10)

        
        self.alpha_label = ttk.Label(root, text="Альфа:")
        self.alpha_label.grid(row=3, column=0, padx=10, pady=10)
        
        
        # self.alpha_label = ttk.Label(root, text="")
        # self.alpha_label.grid(row=2, column=0, padx=10, pady=10)
        self.alpha_entry = ttk.Entry(root)
        self.alpha_entry.grid(row=3, column=1, padx=10, pady=10)

        self.probability_label = ttk.Label(root, text="Вероятность (через пробел):")
        self.probability_label.grid(row=4, column=0, padx=10, pady=10)
        
        self.probability_entry = ttk.Entry(root)
        self.probability_entry.grid(row=4, column=1, padx=10, pady=10)

        self.add_matrix_button = ttk.Button(root, text="Add Matrix", command=self.add_matrix)
        self.add_matrix_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.matrix_canvas = None

        self.calculate_button = ttk.Button(root, text="Calculate", command=self.calculate_criteria, state=tk.DISABLED)
        self.calculate_button.grid(row=6, column=0, columnspan=2, pady=10)
        
   
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=50, column=0, columnspan=2, pady=10)

        self.tab_result = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_result, text="Results")

        self.result_label = ttk.Label(self.tab_result, text="", wraplength=400)
        self.result_label.pack(padx=100, pady=10)


        self.matrix_entries = []

    def add_matrix(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for rows and columns.")
            return

        if self.matrix_canvas:
            # If canvas already exists, destroy it before creating a new one
            self.matrix_canvas.destroy()

        self.matrix_canvas = tk.Canvas(self.root)
        self.matrix_canvas.grid(row=5, column=0, columnspan=2, pady=1)

        entry_width = 5
        entry_height = 1
        padding = 5

        self.matrix_entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ttk.Entry(self.matrix_canvas, width=entry_width)
                entry.grid(row=i, column=j, padx=padding, pady=padding)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        self.calculate_button["state"] = tk.NORMAL

    def calculate_criteria(self):
        result_matrix = []
        for row_entries in self.matrix_entries:
            result_row = []
            for entry in row_entries:
                entry_value_str = entry.get().strip()
                try:
                    entry_value = float(entry_value_str)
                    result_row.append(entry_value)
                except ValueError:
                    messagebox.showerror("Error", "Matrix entries must be numbers.")
                    return
            result_matrix.append(result_row)

        wald_criterion, wald_optimal_strategies = self.calculate_wald_criterion(result_matrix)
        savage_criterion, savage_optimal_strategies = self.calculate_savage_criterion(result_matrix)

        alpha = self.get_alpha_value()
        if alpha is None:
            alpha = 0.5

        gurvitz_criterion, gurvitz_optimal_strategies = self.calculate_gurvitz_criterion(result_matrix, alpha)

        user_probabilities_str = self.probability_entry.get().strip()
        if user_probabilities_str:
            try:
                user_probabilities = [float(prob) for prob in user_probabilities_str.split()]
                if sum(user_probabilities) != 1:
                    messagebox.showerror("Error", "Probabilities must sum to 1.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid probability format.")
                return

            laplace_criterion, laplace_optimal_strategies = self.calculate_laplace_criterion(result_matrix, user_probabilities)
        else:
            laplace_criterion, laplace_optimal_strategies = self.calculate_laplace_criterion(result_matrix)

        
        result_text = "------------------------------------------------------\n"

        # result_text += f"Критерий Вальда: {wald_criterion}\nОптимальная стратегия по Вальду: {', '.join(wald_optimal_strategies)}\n\n"
        # result_text += f"Критерий Сэвиджа: {savage_criterion}\nОптимальная стратегия по Сэвиджу: {', '.join(savage_optimal_strategies)}\n\n"
        # result_text += f"Критерий Гурвица: {gurvitz_criterion}\nОптимальная стратегия по Гувицу: {', '.join(gurvitz_optimal_strategies)}\n\n"
        # result_text += f"Критерий Лапласса: {round(laplace_criterion, 2)}\nОптимальная стратегия по Лаплассу: {', '.join(laplace_optimal_strategies)}"
        
        result_text += f"Оптимальная стратегия по Вальду: {', '.join(wald_optimal_strategies)}\n\n"
        result_text += f"Оптимальная стратегия по Сэвиджу: {', '.join(savage_optimal_strategies)}\n\n"
        result_text += f"Оптимальная стратегия по Гувицу: {', '.join(gurvitz_optimal_strategies)}\n\n"
        result_text += f"Оптимальная стратегия по Лаплассу: {', '.join(laplace_optimal_strategies)}"

        result_text += "\n------------------------------------------------------\n"
        
        strategy_counts = {}
        for strategy in wald_optimal_strategies + savage_optimal_strategies + gurvitz_optimal_strategies + laplace_optimal_strategies:
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        most_common_strategy = max(strategy_counts, key=strategy_counts.get)

        result_text += f"\n\nОптимальная стратегия игры: {most_common_strategy}"
        
        self.notebook.select(self.tab_result)
        
        self.result_label["text"] = result_text
        
    def matrix_to_string(self, matrix):
        return "\n".join(["\t".join(map(str, row)) for row in matrix])

    def calculate_wald_criterion(self, matrix):
        if not matrix or not matrix[0]:
            return None, []

        player1_payoffs = [min(row) for row in matrix]
        max_payoff = max(player1_payoffs)
        optimal_strategies = [f'A{i + 1}' for i, payoff in enumerate(player1_payoffs) if payoff == max_payoff]
        return max_payoff, optimal_strategies

    def calculate_savage_criterion(self, matrix):
        if not matrix or not matrix[0]:
            return None, []

        max_values_per_column = [max(col) for col in zip(*matrix)]
        risk_matrix = [[max_value - value if max_value - value >= 0 else 0 for value, max_value in zip(row, max_values_per_column)] for row in matrix]

        if not risk_matrix or not risk_matrix[0]:
            return None, []

        max_values_per_row = [max(row) for row in risk_matrix]
        min_max_loss = min(max_values_per_row)

        optimal_strategies = [f'A{i + 1}' for i, loss in enumerate(max_values_per_row) if loss == min_max_loss]
        
        return min_max_loss, optimal_strategies

    def calculate_gurvitz_criterion(self, matrix, alpha):
        if not matrix or not matrix[0]:
            return None, []

        max_values_per_column = [max(col) for col in zip(*matrix)]
        gurvitz_values = [alpha * min(row) + (1 - alpha) * max(row) for row in matrix]
        max_gurvitz_value = max(gurvitz_values)
        optimal_strategies = [f'A{i + 1}' for i, value in enumerate(gurvitz_values) if value == max_gurvitz_value]
        return max_gurvitz_value, optimal_strategies

    def calculate_laplace_criterion(self, matrix, probabilities=None):
        if not matrix or not matrix[0]:
            return None, []

        if probabilities is None:
            probabilities = [1 / len(matrix[0]) for _ in range(len(matrix[0]))]

        laplace_values = [sum(prob * payoff for prob, payoff in zip(probabilities, row)) for row in matrix]
        max_laplace_value = max(laplace_values)
        optimal_strategies = [f'A{i + 1}' for i, value in enumerate(laplace_values) if value == max_laplace_value]
        return max_laplace_value, optimal_strategies

    def get_alpha_value(self):
        alpha_str = self.alpha_entry.get().strip()
        if alpha_str:
            try:
                alpha = float(alpha_str)
                if 0 <= alpha <= 1:
                    return alpha
                else:
                    messagebox.showerror("Error", "Alpha must be in the range [0, 1].")
            except ValueError:
                messagebox.showerror("Error", "Invalid alpha format.")
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixGameApp(root)
    root.mainloop()
