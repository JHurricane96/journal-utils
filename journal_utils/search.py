import re
import time
from pathlib import Path

import fasttext
import fasttext.util


def search_tags(query: str, cfg):
    start = time.time()
    fasttext.util.download_model("en", if_exists="ignore")
    print(f"Downloaded model in {time.time() - start}s")

    start = time.time()
    model = fasttext.load_model("cc.en.300.bin")
    print(f"Loaded model in {time.time() - start}s")

    # Get all the markdown files in the journal directory
    journal_dir = Path(cfg["journal_path"])
    journal_files = journal_dir.glob("**/*.md")
    journal_files = [str(f) for f in journal_files]

    # Initialize a list to store the similar tags
    similar_tags = []

    # Initialize a regex pattern to find tags
    tag_pattern = re.compile(r"@(\w+)")

    # Iterate over each markdown file
    for file in journal_files:
        with open(file, "r") as f:
            content = f.read()
            # Find all tags in the content
            tags = tag_pattern.findall(content)
            # Compare each tag to the query using the fasttext model
            for tag in tags:
                similarity = model.get_sentence_vector(tag).dot(
                    model.get_sentence_vector(query)
                )
                # Add the tag to the list if it is similar to the query
                if similarity > 0.5:
                    similar_tags.append((tag, file, similarity))

    # Return the top similar tags
    similar_tags.sort(key=lambda x: x[2], reverse=True)
    for tag, file, similarity in similar_tags[:10]:
        print(f"@{tag} in {file} with similarity {similarity}")


def search(args, cfg):
    search_type: str = args.type
    if search_type == "tag":
        search_tags(args.query, cfg)
