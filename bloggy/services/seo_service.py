from bs4 import BeautifulSoup

stopwords_list = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
    "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
    'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
    'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were',
    'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
    'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
    'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
    'can',
    'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
    'ain',
    'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
    'hasn',
    "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
    "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',
    "won't", 'wouldn', "wouldn't"]


def remove_stopwords(input_string, stopwords):
    words = input_string.split()  # Split the input string into words
    filtered_words = [word for word in words if word.lower() not in stopwords]
    result = ' '.join(filtered_words)  # Join the filtered words back into a string
    return result


def get_keywords(content, *extras):
    Soup = BeautifulSoup(content, 'html5lib')
    heading_tags = ["h1", "h2", "h3"]

    keywords = []
    for tags in Soup.find_all(heading_tags):
        keywords.append(tags.text.strip())
    if extras:
        keywords_str = (','.join(extras)) + "," + (','.join(keywords))
    else:
        keywords_str = ','.join(keywords)
    print("Keywords:%s" % keywords_str)

    filtered_keywords_str = remove_stopwords(keywords_str, stopwords_list)
    print("Keywords:%s" % filtered_keywords_str)
    return keywords_str.lower()
