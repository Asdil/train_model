# import fasttext
#
#
#
# def train_w2c(raw_df, item):
#
# # model=fasttext.skipgram(input_train_file,'wordvec_model',word_ngrams=2,ws=7,epoch=200,dim=200,lr=0.05)


from shallowlearn.models import FastText
clf = FastText(dim=100, min_count=0, loss='hs', epoch=3, bucket=5, word_ngrams=2)
clf.fit([[u'i', u'am', u'tall', u'fds', u'haha'], [u'you', u'are']], [u'yes', u'no'])
a = clf._classifier.predict_proba(u'tall am i', clf._label_count)
stop = 0

documents = u'tall am i'

a = iter(' '.join(d) for d in documents)
for each in a:
    print(str(a))