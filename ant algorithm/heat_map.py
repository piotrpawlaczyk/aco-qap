from typing import List, Any

import matplotlib.pyplot as plt
import numpy as np


class AntHeatmapGenerator:
    def __init__(self, ants: List[Any]):
        if not ants:
            raise ValueError("Lista ants nie może być pusta")

        self.ants = ants
        self.num_locations = len(ants[0].assignment)
        self.num_factories = self.num_locations

    def build_matrix(self) -> np.ndarray:
        """
        Tworzy macierz [location][factory], której element określa liczbę mrówek,
        które przypisały daną fabrykę do danej lokalizacji.
        """
        matrix = np.zeros(
            (self.num_locations, self.num_factories),
            dtype=int,
        )

        for ant in self.ants:
            if len(ant.assignment) != self.num_locations:
                raise ValueError(
                    "Wszystkie obiekty Ant muszą mieć assignment tej samej długości"
                )

            for location, factory in enumerate(ant.assignment):
                if not 0 <= factory < self.num_factories:
                    raise ValueError(
                        f"Niepoprawny numer fabryki {factory} dla lokalizacji {location}"
                    )

                matrix[location, factory] += 1

        return matrix

    def plot(
        self,
        normalize: bool = False,
        figsize=(10, 8),
        cmap: str = "viridis",
        show_values: bool = True,
    ):
        matrix = self.build_matrix().astype(float)

        if normalize:
            matrix /= len(self.ants)

        fig, ax = plt.subplots(figsize=figsize)
        image = ax.imshow(matrix, cmap=cmap, aspect="auto")

        ax.set_title("Heatmap przypisań lokalizacja -> fabryka")
        ax.set_xlabel("Fabryka")
        ax.set_ylabel("Lokalizacja")

        ax.set_xticks(range(self.num_factories))
        ax.set_yticks(range(self.num_locations))

        ax.set_xticklabels([str(i) for i in range(self.num_factories)])
        ax.set_yticklabels([str(i) for i in range(self.num_locations)])

        if show_values:
            for location in range(self.num_locations):
                for factory in range(self.num_factories):
                    value = matrix[location, factory]

                    if normalize:
                        text = f"{value:.2f}"
                    else:
                        text = str(int(value))

                    ax.text(
                        factory,
                        location,
                        text,
                        ha="center",
                        va="center",
                        color="white" if value > matrix.max() / 2 else "black",
                    )

        plt.colorbar(image, ax=ax, label="Liczba przypisań")
        plt.tight_layout()
        plt.show()

