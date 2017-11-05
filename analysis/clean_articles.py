import os

def clean_str(s):
    punctuation = {'.',',',';','"',"'",':','!','?','\n','\t'}
    for punct in punctuation:
        s = s.replace(punct, '')
    return s.strip()

article_dir = '../articles/'

def clean():
    # Create set containing used articles (to avoid duplicates)
    used = set()
    with open('articles_used.txt', 'r') as history_file:
        for line in history_file.readlines():
            used.add(line.strip())


    used_update = set()
    with open('combined','a') as combined_file:
        for f in os.listdir(article_dir):
            if f[-4:] == '.txt' and f not in used:

                # Add article contents to 'combined'
                with open(article_dir + f, 'r') as art:
                    for line in art.readlines():
                        combined_file.write(clean_str(line))
                used_update.add(f)

    print("{0} new articles added to collection.".format(len(used_update)))
    with open('articles_used.txt', 'a') as history_file:
        for article in used_update:
            history_file.write(article + '\n')
