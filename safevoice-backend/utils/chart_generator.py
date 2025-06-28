# utils/chart_generator.py
import matplotlib
matplotlib.use("Agg")  # headless backend
import matplotlib.pyplot as plt


def save_emotion_bar(overall_emotions: list, out_path: str = "emotion_chart.png"):
    """
    overall_emotions: list of dicts from HF pipeline
        e.g. [{'label': 'anger', 'score': 0.62}, ...]
    Saves a horizontal bar chart image (PNG) for embedding in PDF.
    Returns the path.
    """
    labels = [e["label"] for e in overall_emotions]
    values = [round(e["score"] * 100, 1) for e in overall_emotions]

    plt.figure(figsize=(6, 3))
    bars = plt.barh(labels, values)
    plt.xlabel("Intensity (%)")
    plt.xlim(0, 100)
    plt.title("Overall Emotion Scores")

    # add text labels
    for bar, val in zip(bars, values):
        plt.text(val + 1, bar.get_y() + bar.get_height() / 2,
                 f"{val}%", va="center")

    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    plt.close()
    return out_path
