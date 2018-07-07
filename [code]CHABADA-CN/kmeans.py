import jieba
import pandas as pd
import re
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
import numpy
import re
#import pyldavis
# 创建停用词list

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
        with open("topic.txt","a") as f:
            f.write("\nTopic #%d:" % topic_idx)
            f.write(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords
def chinese_word_cut(mytext):
    filtrate = re.compile(u'[^\u4E00-\u9FA5，。]');
    mytext = filtrate.sub(r'',str(mytext))
    #print(mytext)
    sentence_seged = jieba.cut(str(mytext).strip())
    stopwords = stopwordslist('stop.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr
df = pd.read_csv("appdescNew.csv",header=None,iterator = True)
df = df.get_chunk(300000)#只取前100行
col_name =df.columns[1]
names = pd.DataFrame(df[0])
df=df.rename(columns = {col_name:'content'})
df["content_cutted"] = df.content.apply(chinese_word_cut)
print(type(df.content_cutted))
#numpy.savetxt('new1.csv',df.content_cutted, delimiter = ',')
n_features = 10000 #特征词数量
tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features=n_features,
                                stop_words='english',
                                max_df = 0.5,
                                min_df = 10)
tf = tf_vectorizer.fit_transform(df.content_cutted)

n_topics =30 #话题数量
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
cm = lda.fit_transform(tf)
n_top_words = 30 #打印的话题数量
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)

numpy.savetxt('new2.csv',cm, delimiter = ',')
#聚类20个
kmeans = KMeans(n_clusters=32, random_state=0).fit(cm)
kresults = pd.DataFrame(data=numpy.array(kmeans.labels_))
print(type(names),type(kresults))
newre = pd.concat([names,kresults], axis=1)
#newre = names.append(kresults)
newre.to_csv('new3.csv',encoding="utf-8",index=False)
