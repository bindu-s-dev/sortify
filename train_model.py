import pickle

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Training examples for Sortify
training_data = [
    # Organic waste
    ("banana peel", "Organic Waste"),
    ("apple core", "Organic Waste"),
    ("food scraps", "Organic Waste"),
    ("vegetable waste", "Organic Waste"),
    ("dry leaves", "Organic Waste"),
    ("grass clippings", "Organic Waste"),
    ("flower waste", "Organic Waste"),
    ("fruit peels", "Organic Waste"),
    ("eggshells", "Organic Waste"),
    ("garden leaves", "Organic Waste"),
    ("coffee grounds", "Organic Waste"),
    ("tea bags", "Organic Waste"),
    ("leftover food", "Organic Waste"),
    ("spoiled fruits", "Organic Waste"),
    ("spoiled vegetables", "Organic Waste"),
    ("bread crusts", "Organic Waste"),
    ("citrus peels", "Organic Waste"),

    # Paper waste
    ("newspaper", "Paper Waste"),
    ("cardboard box", "Paper Waste"),
    ("paper sheets", "Paper Waste"),
    ("paper bag", "Paper Waste"),
    ("magazine", "Paper Waste"),
    ("old books", "Paper Waste"),
    ("office paper", "Paper Waste"),

    # Plastic waste
    ("plastic bottle", "Plastic Waste"),
    ("plastic bag", "Plastic Waste"),
    ("plastic wrapper", "Plastic Waste"),
    ("plastic container", "Plastic Waste"),
    ("shampoo bottle", "Plastic Waste"),
    ("plastic packaging", "Plastic Waste"),

    # Glass waste
    ("glass bottle", "Glass Waste"),
    ("broken glass", "Glass Waste"),
    ("glass jar", "Glass Waste"),
    ("glass container", "Glass Waste"),

    # Metal waste
    ("aluminium can", "Metal Waste"),
    ("steel can", "Metal Waste"),
    ("metal tin", "Metal Waste"),
    ("scrap metal", "Metal Waste"),

    # Electronic waste
    ("old mobile phone", "Electronic Waste"),
    ("broken laptop", "Electronic Waste"),
    ("old computer", "Electronic Waste"),
    ("old charger", "Electronic Waste"),
    ("broken headphones", "Electronic Waste"),
    ("computer keyboard", "Electronic Waste"),

    # Hazardous waste
    ("used battery", "Hazardous Waste"),
    ("household battery", "Hazardous Waste"),
    ("paint thinner", "Hazardous Waste"),
    ("chemical cleaner", "Hazardous Waste"),
    ("pesticide residue", "Hazardous Waste"),
]

texts = [item for item, category in training_data]
labels = [category for item, category in training_data]

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(texts, labels)

with open("sortify_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Sortify ML model trained successfully!")

print("\nSample predictions:")

test_items = [
    "dry leaves",
    "old laptop",
    "plastic bottle",
    "banana peel"
]

for item in test_items:
    prediction = model.predict([item])[0]
    print(f"{item} -> {prediction}")