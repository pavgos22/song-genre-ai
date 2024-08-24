import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import matplotlib.pyplot as plt
import pickle

from lemmatization import manage_lyrics


def output_window(song, window):
    new_window = tk.Toplevel(window)
    new_window.title("Song Genre AI")
    new_window.geometry("700x500")
    label = tk.Label(new_window, text="The genre of this song is: " + song)
    label.pack(pady=(10, 10))
    image = Image.open("plots/plot.jpg")
    image = image.resize((640, 420))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(new_window, image=photo)
    label.pack()
    new_window.mainloop()


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    entry.delete(0, tk.END)
    entry.insert(tk.END, file_path)


def submit_file():
    global song
    print("File submitted successfully")
    path = entry.get()
    with open(path, 'r') as file:
        content = file.read()
    with open("instance.pickle", "rb") as file:
        data = pickle.load(file)
    data.deserialize_dictionaries('compressed_data.json.gz')
    lyric = manage_lyrics(content)

    probabilities = data.calculate_one_song(lyric)
    min_prob = min(probabilities.values())
    for prob in probabilities:
        probabilities[prob] -= min_prob

    total = sum(probabilities.values())
    for prob in probabilities:
        probabilities[prob] = round(probabilities[prob] / total * 100, 2)

    max_prob = max(probabilities.values())
    for key, value in probabilities.items():
        if value == max_prob:
            song = key

    plt.figure(figsize=(12, 6))
    plt.bar(probabilities.keys(), probabilities.values())
    plt.xlabel("Genre")
    plt.ylabel("Probability")
    plt.savefig('plots/plot.jpg', format='jpg')
    plt.show()

    output_window(song, window)


window = tk.Tk()
window.title("Song Genre AI")
window.geometry("700x500")

image = Image.open("logo/logo.png")
image = image.resize((300, 225))
photo = ImageTk.PhotoImage(image)

label = tk.Label(window, image=photo)
label.pack()

label = tk.Label(window, text="Choose txt file:")
label.pack(pady=(10, 10))

button = tk.Button(window, text="Browse files", command=browse_file)
button.pack(pady=(10, 10))

entry = tk.Entry(window, width=50)
entry.pack(pady=(10, 10))

button = tk.Button(window, text="Submit", command=submit_file)
button.pack(pady=(10, 10))

window.mainloop()
