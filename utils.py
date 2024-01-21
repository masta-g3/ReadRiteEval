from typing import Tuple, List, Dict, Optional
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

plot_title_map = {
    "sequence_logic_puzzle": "Sequence Logic Puzzle",
    "spatial_reasoning": "Spatial Reasoning",
    "dependency_cascades": "Dependency Cascades",
    "hypothesis_testing": "Hypothesis Testing",
    "contextual_dissonance": "Contextual Dissonance",
}

def delete_score(scores: list, model_name: str, test_name: str):
    new_scores = [s for s in scores if not (s.test == test_name and s.model == model_name)]
    print(f"Deleted {len(scores) - len(new_scores)} scores.")
    return new_scores


def plot_scores(
    test_name: str,
    scores: List,
    model_sizes: Dict[str, float],
    bad_models: Optional[List[str]] = None,
) -> Tuple[plt.Figure, plt.Axes]:
    # Filter scores based on the test name and bad models
    filtered_scores = [
        score for score in scores
        if score.test == test_name and (bad_models is None or score.model not in bad_models)
    ]

    # Calculate proportions and confidence intervals for each candidate
    z = 1.96  # z-score for 95% confidence
    proportions = {}
    conf_intervals = {}

    for score in filtered_scores:
        n_questions = len(score.full_answers)  # Number of questions for each candidate
        p = score.total_score
        proportions[score.model] = p
        conf_intervals[score.model] = (
            p - z * np.sqrt(p * (1 - p) / n_questions),  # lower bound
            p + z * np.sqrt(p * (1 - p) / n_questions)   # upper bound
        )

    # Sorting models based on scores
    sorted_models = sorted(proportions, key=proportions.get)

    # Determine colors based on model sizes
    bin_breakpoints = [13.5, 70.5, 1000]
    bin_colors = ["#77dd77", "#ffb347", "#ff6961"]
    model_colors = {
        model: bin_colors[sum([model_sizes[model] >= breakpoint for breakpoint in bin_breakpoints])]
        for model in sorted_models
    }

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))
    for model in sorted_models:
        ax.errorbar(
            model,
            proportions[model],
            yerr=[[proportions[model] - conf_intervals[model][0]],
                  [conf_intervals[model][1] - proportions[model]]],
            fmt='o',
            ecolor=model_colors[model],
            capsize=5,
            markersize=8,
            markeredgewidth=4,
            color=model_colors[model]
        )

    ax.set_xticks(range(len(sorted_models)))
    ax.set_xticklabels(sorted_models, rotation=90)
    ax.set_title(plot_title_map[test_name])


    ax.set_ylabel("Proportion of Correct Answers")
    fig.tight_layout()

    return fig, ax


###########################
## TEXT COMPARISON TOOLS ##
###########################

def simple_tokenize(sentence):
    """ Tokenize a sentence into words, removing punctuation."""
    return re.findall(r'\b\w+\b', sentence.lower())


def normalize_text(text):
    """Convert text to lowercase and remove punctuation."""
    return re.sub(r'[^\w\s]', '', text.lower())


def sentences_match(answer, proposed_answer, tolerance=2):
    """ Check if two sentences match, allowing for some tolerance in the number of words."""
    answer_set = set(simple_tokenize(answer))
    proposed_answer_set = set(simple_tokenize(proposed_answer))
    return abs(len(answer_set) - len(proposed_answer_set)) <= tolerance and \
           (answer_set.issubset(proposed_answer_set) or proposed_answer_set.issubset(answer_set))


def tfidf_embedding_similarity(answer, proposed_answer):
    """ Calculate the cosine similarity between two sentences using TF-IDF embeddings."""
    vectorizer = TfidfVectorizer()
    vectorizer.fit([answer, proposed_answer])
    vectors = vectorizer.transform([answer, proposed_answer]).toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]


def hf_embedding_similarity(answer, proposed_answer, model_name="TaylorAI/gte-tiny"):
    """ Calculate the cosine similarity between two sentences using a HuggingFace embedding model."""
    model = SentenceTransformer(model_name)
    embeddings = model.encode([answer, proposed_answer])
    return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]


def subword_cosine_similarity(answer: str, proposed_answer: str):
    """ Normalizes and compares the answers using sub-word vectorization and cosine similarity. """
    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 3), use_idf=False,  preprocessor=normalize_text)
    vectors = vectorizer.fit_transform([normalize_text(answer), normalize_text(proposed_answer)])
    return cosine_similarity(vectors[0], vectors[1])[0][0]
