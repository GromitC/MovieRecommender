import pip

def install(package):
    pip.main(['install', package])


if __name__ == '__main__':
    install('pymongo')
    install('joblib')
    install('HTMLParser')
    install('stop_words')
    install('gensim')
