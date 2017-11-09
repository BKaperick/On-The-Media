import word2vec as w2v
import clean_articles
from pprint import pprint
import sys

if len(sys.argv) > 1 and sys.argv[1] in ['-t','-train']:
    
    # Add new articles to file
    clean_articles.clean()

    # Train new model
    w2v.word2phrase('combined', './text-phrases', verbose=True) 
    w2v.word2vec('text8-phrases', 'text.bin', size=100, verbose=True)
    w2v.word2clusters('combined', 'text-clusters.txt', 100, verbose=True)

# Initialize pre-trained model
model_old = w2v.load('text8.bin')
model = w2v.load('text.bin')
clusters = w2v.load_clusters('text-clusters.txt')
model.clusters = clusters

#ind = clusters['Trump']
#print(clusters.get_words_on_cluster(ind))
print(len(model_old.vocab))
print(len(model.vocab))

# King - man + woman : "Man is to King as Woman is to
# Trump - America + Germany
pos=['Putin','America']
neg=['Russia']
leader = model.analogy(pos,neg)

print()
print("{0} is to {1} as {2} is to ...".format(neg[0], pos[0], pos[1])) 
print(model.generate_response(*leader))


while True:
    print("\n")
    word = input()
    try:
        print(model.cosine(word))
        indexes, metrics = model.cosine(word)
        #model.vocab[indexes]
        print(model.generate_response(indexes, metrics).tolist())
        for word,dist,size in model.generate_response(indexes, metrics).tolist():
            print(word,dist,size)

    except KeyError:
        pass
