from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_chunks(file_text, chunk_size=100):

    words = file_text.split()

    chunks = []

    for start in range(0, len(words), chunk_size):

        end = start + chunk_size

        chunk = " ".join(words[max(0, (start-20)):end])

        if chunk.strip():

            chunks.append(chunk)

    return chunks


# Find the Most Relevant Resume Sections

def retrieve_chunks(chunks, question, top_k=6):

    chunk_texts = []

    for chunk in chunks:

        chunk_texts.append(
            chunk["text"]
        )
    all_documents = [question] + chunk_texts

    vectorizer = TfidfVectorizer(
        stop_words="english",
         ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(
        all_documents
    )

    question_vector = vectors[0:1]

    document_vectors = vectors[1:]

    similarity_scores = cosine_similarity(
        question_vector,
        document_vectors
    )[0]

    top_k = min(
        top_k,
        len(chunks)
    )

    best_indexes = similarity_scores.argsort()[
        -top_k:
    ][::-1]

    retrieved_results = []

    for index in best_indexes:

        retrieved_results.append(
            {
                "chunk": chunks[index]["text"],

                "score": float(
                    similarity_scores[index]
                ),

                "source": chunks[index]["source"],

                "page": chunks[index]["page"]
            })


    return retrieved_results
