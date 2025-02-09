import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from IPython.core.display import HTML
from time import time
from tqdm import tqdm


class GeneEvolutionRenderer:
    def __init__(self, **kwargs):
        self.interval = kwargs.get("interval", 500)
        self.fps = kwargs.get("fps", 2)
        self.figsize = kwargs.get("figsize", (10, 5))
        self.bar_color = kwargs.get("bar_color", "blue")
        self.title_template = kwargs.get(
            "title", "Gene Evolution - Generation {generation}"
        )
        self.independent_ylim = kwargs.get("independent_ylim", False)

    def visualize(self, collected_data, **kwargs):
        time0 = time()
        num_tribes, num_chromosomes = collected_data[0]["genes"].shape
        fig, axes = plt.subplots(1, num_tribes, figsize=self.figsize)
        if num_tribes == 1:
            axes = [axes]

        progress_bar = tqdm(
            total=len(collected_data),
            desc="Rendering Frames",
            unit="frame",
            leave=False,
        )

        def update(frame):
            progress_bar.update(1)
            if kwargs.get("print_updates", False):
                print(f"[{time() - time0:.6f}] handling frame {frame}")
            data = collected_data[frame]
            genes = data["genes"]
            evaluations = data["evaluations"]
            fig.suptitle(self.title_template.format(generation=frame), fontsize=16)

            for tribe_idx, (ax, gene, evaluation) in enumerate(
                zip(axes, genes, evaluations)
            ):
                ax.clear()
                ax.bar(range(num_chromosomes), gene, color=self.bar_color)
                if self.independent_ylim:
                    ax.set_ylim(gene.min() * 0.9, gene.max() * 1.1)
                else:
                    ax.set_ylim(0.0, 1.0)
                ax.set_title(f"Tribe {tribe_idx + 1}")
                ax.set_xlabel("")
                ax.set_ylabel(f"Value: {evaluation:.2f}")
                ax.set_xticks(range(num_chromosomes))

        ani = FuncAnimation(
            fig, update, frames=len(collected_data), interval=self.interval, blit=False
        )

        output_path = kwargs.get("output_path", None)
        if output_path is None:
            html = HTML(ani.to_jshtml())
            progress_bar.close()
            return html
        else:
            ani.save(output_path, writer=PillowWriter(fps=self.fps))
            plt.close(fig)
            progress_bar.close()
            print(f"GIF saved to {output_path}")
