from transformers import pipeline

# Load the abuse detection model
toxicity_model = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    top_k=None  # Return all abuse category scores
)

def detect_abuse(text):
    """
    Analyze the input text for multiple categories of toxic behavior.
    Returns:
        - is_abusive (bool): True if any category exceeds threshold.
        - categories (list): List of abusive labels with their scores.
    """
    results = toxicity_model(text)
    abuse_categories = []

    for result in results[0]:  # result is a list of dicts
        if result['score'] >= 0.6:  # adjustable threshold
            abuse_categories.append({
                "label": result["label"],
                "score": round(result["score"], 2)
            })

    is_abusive = len(abuse_categories) > 0

    return {
        "is_abusive": is_abusive,
        "categories": abuse_categories
    }
