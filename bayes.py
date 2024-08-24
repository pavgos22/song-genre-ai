import os
from collections import Counter
import matplotlib.pyplot as plt
import json
import gzip
import math


def first_plot(right, wrong):
    plt.bar('Correct', right)
    plt.bar('Wrong', wrong)
    plt.title('Algorithm effectiveness')
    plt.ylabel("Number of songs")
    plt.show()


class Bayes:
    def __init__(self, database):
        self.train_data = database
        self.categories = ['Pop', 'Hip Hop', 'Rap', 'Rock', 'Heavy Metal', 'Country', 'R&B', 'Dance',
                           'Reggae', 'Jazz']
        self.genre_probability = {}
        self.words_genre_dictionaries = {}
        self.total_genre_words = {}
        self.generate_genre_probability()
        self.generate_word_dictionaries()

    def generate_genre_probability(self):
        total_songs = len(self.train_data)
        genre_counts = self.train_data['Genres'].value_counts()
        for genre in self.categories:
            count = genre_counts.get(genre, 0)
            self.genre_probability[genre] = count / total_songs

    def generate_word_dictionary(self, genre):
        merged_counter = Counter()
        genre_lyrics = self.train_data[self.train_data['Genres'] == genre]['Lyric']
        for lyrics in genre_lyrics:
            merged_counter.update(lyrics.split())
        self.words_genre_dictionaries[genre] = merged_counter
        self.total_genre_words[genre] = sum(merged_counter.values())

    def generate_word_dictionaries(self):
        for genre in self.categories:
            self.generate_word_dictionary(genre)

    def calculate_one_song(self, text):
        probabilities = self.genre_probability.copy()
        text_list = text.split()
        for genre in self.categories:
            total_words_genre = self.total_genre_words[genre]
            for word in text_list:
                word_count = self.words_genre_dictionaries[genre].get(word, 0)
                word_probability = (word_count + 1) / (total_words_genre + len(self.words_genre_dictionaries[genre]))
                probabilities[genre] += math.log(word_probability)
        return probabilities

    def serialize_dictionaries(self, file_name):
        serialized_data = json.dumps(self.words_genre_dictionaries).encode('utf-8')
        compressed_data = gzip.compress(serialized_data)
        with open(file_name, 'wb') as file:
            file.write(compressed_data)

    def deserialize_dictionaries(self, file_name):
        file_path = os.path.join('data', file_name)
        with open(file_path, 'rb') as file:
            compressed_data = file.read()
        decompressed_data = gzip.decompress(compressed_data)
        deserialized_data = json.loads(decompressed_data.decode('utf-8'))
        self.words_genre_dictionaries = deserialized_data

    def check_performance(self, test_data):
        right = 0
        wrong = 0
        results_to_plot = [0 for _ in range(0, 10)]
        for i, lyrics in enumerate(test_data['Lyric']):
            print(i, '/', len(test_data['Lyric']))
            results = self.calculate_one_song(lyrics)
            predicted_genre = max(results, key=results.get)
            if predicted_genre == test_data['Genres'][i]:
                right += 1
                for i in range(0, 10):
                    if self.categories[i] == predicted_genre:
                        results_to_plot[i] += 1
            else:
                wrong += 1
        print('Right:', right)
        print('Wrong:', wrong)
        first_plot(right, wrong)
        self.second_plot(results_to_plot)

    def second_plot(self, results):
        plt.figure(figsize=(12, 6))
        plt.bar(self.categories, results)
        plt.title('Algorithm effectiveness')
        plt.xlabel("Genre")
        plt.ylabel("Number of songs")
        plt.show()
