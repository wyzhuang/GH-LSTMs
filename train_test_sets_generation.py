import numpy as np
import pickle
from gensim.models import KeyedVectors
from tqdm import tqdm


def save_glove_transform(w2v_model, project, version, vector_length, max_length):
    train_sequence = []
    train_labels = []
    train_sequence_and_label = open("./sequence_and_label/{}_{}.txt".format(project, version), 'r+',
                                    encoding='utf-8').readlines()
    for line in train_sequence_and_label:
        line = eval(line)
        train_sequence.append(line["sequence"].split(" "))
        train_labels.append(line["bug"])
    place_holder = np.zeros([len(train_sequence), max_length, vector_length])
    for i in tqdm(range(len(train_sequence))):
        sentence = train_sequence[i]
        if sentence:
            for j in range(min(len(sentence), max_length)):
                word = sentence[j]
                if word in w2v_model:
                    place_holder[i][j] = w2v_model[word]
                else:
                    place_holder[i][j] = w2v_model['<unk>']
    return place_holder, np.array(train_labels)


if __name__ == '__main__':

    projects = ['ant', 'camel', 'ivy', 'jedit', 'log4j', 'lucene', 'poi', 'synapse', 'xalan', 'xerces']

    versions = {'ant': ['1.5', '1.6', '1.7'], 'camel': ['1.2', '1.4', '1.6'], 'jedit': ['3.2', '4.0', '4.1'],
                'log4j': ['1.0', '1.1'], 'lucene': ['2.0', '2.2', '2.4'], 'xalan': ['2.4', '2.5'],
                'xerces': ['1.2', '1.3'], 'ivy': ['1.4', '2.0'], 'synapse': ['1.0', '1.1', '1.2'],
                'poi': ['1.5', '2.5', '3.0']}

    max_lengths = {'ant': 500, 'camel': 900, 'ivy': 1500, 'jedit': 2500, 'log4j': 1200, 'lucene': 1500, 'poi': 1800,
                   'synapse': 1200, 'xalan': 2000, 'xerces': 2000}
    for project in projects:
        version_pairs = [versions[project][i:i + 2] for i in range(0, len(versions[project]) - 1, 1)]
        for pair in version_pairs:
            file_name = '{}_{}_{}_{}'.format(project, pair[0], pair[1], "40d")
            print('{} start!\n'.format(file_name))
            # generate label dict
            w2v_model = KeyedVectors.load_word2vec_format('./GloVe/models/{}/{}_{}.txt'.format(40, project, pair[0]))
            train_X, train_Y = save_glove_transform(w2v_model, project, pair[0], 40, max_lengths[project])
            test_X, test_Y = save_glove_transform(w2v_model, project, pair[1], 40, max_lengths[project])
            np.save("./data/sce_data/{}_train_X.npy".format(file_name), train_X)
            np.save("./data/sce_data/{}_train_Y.npy".format(file_name), train_Y)
            np.save("./data/sce_data/{}_test_X.npy".format(file_name), test_X)
            np.save("./data/sce_data/{}_test_Y.npy".format(file_name), test_Y)







