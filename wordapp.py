import streamlit as st
import nltk
from pymed import PubMed
import pandas as pd
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


st.title('GolemPharm')
st.write('')

N_abstract = st.sidebar.slider(
    'Select a number of abstracts ',
    0.0, 10000.0, 2000.0)

#input box
myName  = st.text_input('Ask about your disease here:')
if myName:
    text = myName
    max1 =int(N_abstract)  # ilosc zapytan
    vv = list(myName.split())
    t = str('target')
    vv.append(t)

    pubmed = PubMed(tool="MyTool", email="p.karabowicz@gmail.com")
    results1 = pubmed.query(text, max_results=max1)

    #przeksztalcenie wynikow zapytania na data frame
    lista_abstract_3=[]
    for i in results1:
        lista_abstract_3.append(i.abstract)

    df_abstract = pd.DataFrame(lista_abstract_3, columns = ['abstracts'])
    df_abstract['abstracts_lower'] = df_abstract['abstracts'].str.lower()
    df_abstract_1 = df_abstract.dropna()

    Not_none_values = filter(None.__ne__, lista_abstract_3)
    list_of_values = list(Not_none_values)
    list_of_values = ' '.join(list_of_values)

    df_abstract_1['tokenized'] = df_abstract_1.apply(lambda row: nltk.word_tokenize(row['abstracts_lower']), axis=1)
    from gensim.models import Word2Vec
    EMB_DIM = 100
    model_ted = Word2Vec(sentences=df_abstract_1['tokenized'], vector_size=EMB_DIM, window=5, min_count=1, workers=4, sg=1)

    most_sim = model_ted.wv.most_similar(vv, topn=200)
    most_sim1 = dict(most_sim)
    db_protein = pd.read_csv('./bialka.csv')

    wt2 = db_protein['Gene names'].str.lower().tolist()
    gen = []
    val = []

    for k in most_sim1.keys() & set(wt2):
        gen.append(k)
        val.append(most_sim1[k])

    df = pd.DataFrame(list(zip(gen, val)), columns =['Name', 'val'])
    final_df = df.sort_values(by=['val'], ascending=False)
    ff = final_df.reset_index(drop=True)
    ff
