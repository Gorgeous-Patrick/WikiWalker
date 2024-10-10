import torch
import torch.nn as nn
from gensim.models import Word2Vec
from torch.nn.utils.rnn import pad_sequence

import nltk


def calculate(prev, text, damping_factor=0.5):
    nltk.download("punkt_tab")  # Download necessary tokenizer data

    # Split the text into words
    words = nltk.word_tokenize(text)

    # Step 1: Train or load pre-trained Word2Vec embeddings
    word2vec_model = Word2Vec(
        words, vector_size=1000, window=50, min_count=1, workers=4
    )

    # Step 2: Prepare input embeddings
    embeddings = [
        word2vec_model.wv[word] for word in words if word in word2vec_model.wv
    ]
    embeddings = pad_sequence(
        [torch.tensor(sentence) for sentence in embeddings], batch_first=True
    )

    # Step 3: Define LSTM model
    class LSTMModel(nn.Module):
        def __init__(self, embedding_dim, hidden_dim, output_dim, num_layers=1):
            super(LSTMModel, self).__init__()
            self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers, batch_first=True)
            self.fc = nn.Linear(hidden_dim, output_dim)

        def forward(self, x):
            lstm_out, _ = self.lstm(x)
            lstm_out = lstm_out[-1, :]
            output = self.fc(lstm_out)
            return output

    embedding_dim = 1000
    hidden_dim = 1024
    output_dim = 1000
    model = LSTMModel(embedding_dim, hidden_dim, output_dim, num_layers=2)

    # Step 4: Pass embeddings through LSTM
    with torch.no_grad():
        contextual_embedding = model(embeddings)
        return (1 - damping_factor) * contextual_embedding + damping_factor * prev
