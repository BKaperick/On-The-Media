import word2vec as w2v
from pprint import pprint

#w2v.word2phrase('./text8', './text8-phrases', verbose=True) 
w2v.word2phrase('combined', './text8-phrases', verbose=True) 
w2v.word2vec('text8-phrases', 'text8.bin', size=100, verbose=True)

model = w2v.load('text8.bin')


while True:
    word = input()
    indexes, metrics = model.cosine(word)
    model.vocab[indexes]
    print("\n")

    for word,dist in model.generate_response(indexes, metrics).tolist():
        print(word,dist)
