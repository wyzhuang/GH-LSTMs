import keras
from keras.layers import Input, Embedding, LSTM, Dense, Activation, Multiply, Masking
from keras.models import Model
from keras.callbacks import EarlyStopping, ModelCheckpoint
import pandas as pd
import numpy as np
from keras import backend as K
from keras.backend import clear_session
from sklearn.utils import compute_class_weight
from sklearn.metrics import f1_score,recall_score,precision_score,classification_report
import os

def pre_process_data(path):
    data = pd.read_csv(path)
    data = data[['mfa', 'ic', 'cbm', 'rfc', 'dam', 'ce', 'cbo', 'moa', 'wmc', 'ca', 'dit', 'noc', 'lcom3', 'lcom', 'cam', 'amc', 'npm', 'loc', 'bugs']]
    labels = np.array(data.iloc[:, [-1]])
    features = np.array(data.iloc[:, :-1])
    labels = np.where(labels>0, 1, labels)
    return features.reshape((-1,18,1)), labels

def my_loss(y_true, y_pred):
    theta = lambda t: (K.sign(t) + 1.) / 2.
    margin = 0.6
    return - (1 - theta(y_true - margin) * theta(y_pred - margin)
                - theta(1 - margin - y_true) * theta(1 - margin - y_pred)
             ) * (y_true * K.log(y_pred + 1e-8) + (1 - y_true) * K.log(1 - y_pred + 1e-8))

def my_f1(y_true, y_pred):
    y_pred = K.round(y_pred)
    tp = K.sum(K.cast(y_true * y_pred, 'float'), axis=0)
    tn = K.sum(K.cast((1 - y_true) * (1 - y_pred), 'float'), axis=0)
    fp = K.sum(K.cast((1 - y_true) * y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true * (1 - y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())

    f1 = 2 * p * r / (p + r + K.epsilon())
    f1 = tf.where(tf.is_nan(f1), tf.zeros_like(f1), f1)
    return K.mean(f1)

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# set GPU memory
if('tensorflow' == K.backend()):
    import tensorflow as tf
    from keras.backend.tensorflow_backend import set_session
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)


projects = [
    'ant',
    'camel',
    'ivy',
    'jedit',
    'log4j',
    'lucene',
    'poi',
    'synapse',
    'xalan',
    'xerces'
]

versions = {
    'ant':['1.5', '1.6', '1.7'],
    'camel':['1.2', '1.4', '1.6'],
    'jedit':['3.2', '4.0', '4.1'],
    'log4j':['1.0', '1.1'],
    'lucene':['2.0','2.2', '2.4'],
    'xalan':['2.4', '2.5'],
    'xerces':['1.2', '1.3'],
    'ivy':['1.4', '2.0'],
    'synapse':['1.0', '1.1', '1.2'],
    'poi':['1.5', '2.5', '3.0']
}

max_lengths = {
    'ant': 500,
    'camel':900,
    'ivy':1500,
    'jedit':2500,
    'log4j':1200,
    'lucene':1500,
    'poi':1800,
    'synapse':1200,
    'xalan':2000,
    'xerces':2000
}

dimensions = ['40d']

for i in range(10):
    for project in projects:
        version_pairs = [versions[project][i:i+2] for i in range(0, len(versions[project]) - 1, 1)]
        for pair in version_pairs:
            for dim in dimensions:
                file_name = '{}_{}_{}_{}'.format(project, pair[0], pair[1], dim)
                task_name = '{}_{}_{}_{}_{}'.format(project, pair[0], pair[1], dim, str(i))
                train_X_sce = np.load('./data/sce_data/{}_train_X.npy'.format(file_name))
                train_Y_sce = np.load('./data/sce_data/{}_train_Y.npy'.format(file_name))
                test_X_sce = np.load('./data/sce_data/{}_test_X.npy'.format(file_name))
                test_Y_sce = np.load('./data/sce_data/{}_test_Y.npy'.format(file_name))
                train_X_promise, train_Y_promise = pre_process_data('./data/promise_data/{}/{}.csv'.format(project, pair[0]))
                test_X_promise, test_Y_promise = pre_process_data('./data/promise_data/{}/{}.csv'.format(project, pair[1]))

                weight = dict(enumerate(compute_class_weight(class_weight='balanced', classes=[0, 1],
                                                             y=train_Y_promise.transpose().tolist()[0])))
                clear_session()

                print('{} started:'.format(task_name))
                sce_input = Input(shape=(max_lengths[project], int(dim[:2])), name='sce_input')
                sce_mask = Masking()(sce_input)
                sce_lstm_out = LSTM(128, dropout=0.2, recurrent_dropout=0.2, name='sce_lstm')(sce_mask)
                print(sce_lstm_out)
                sce_gate = Dense(128, activation='sigmoid', name='sce_gate')(sce_lstm_out)
                sce_gated_res = Multiply(name='sce_gated_res')([sce_gate, sce_lstm_out])
                promise_input = Input(shape=(18, 1), name='promise_input')
                promise_lstm_out = LSTM(128, name='promise_lstm')(promise_input)
                promise_gate = Dense(128, activation='sigmoid', name='promise_gate')(promise_lstm_out)
                promise_gated_res = Multiply(name='promise_gated_res')([promise_gate, promise_lstm_out])
                merge = keras.layers.concatenate([sce_gated_res, promise_gated_res])
                main_output = Dense(1, activation='sigmoid', name='main_output')(merge)
                model = Model(inputs=[sce_input, promise_input], outputs=[main_output])

                model.compile(loss=my_loss, optimizer='adam', metrics=['accuracy', my_f1])

                val_data = ({'sce_input': test_X_sce,
                             'promise_input': test_X_promise},
                            {'main_output': test_Y_promise})

                model.fit(x={'sce_input': train_X_sce, 'promise_input': train_X_promise},
                          y={'main_output': train_Y_promise},
                          batch_size=2048,
                          epochs=200,
                          class_weight=weight,
                          validation_data=val_data)

                predict_y = model.predict(x={'sce_input': test_X_sce, 'promise_input': test_X_promise})
                np.save("./res/{}.npy".format(task_name),predict_y)
                predict_y=np.round(predict_y)

                with open('./res/res.txt', 'a+', encoding='utf-8') as f:
                    f.write('{}\n'.format(task_name))
                    f.writelines(classification_report(y_true=test_Y_promise, y_pred=predict_y))
                    f.write('P: {}\n'.format(precision_score(y_true=test_Y_promise, y_pred=predict_y)))
                    f.write('R: {}\n'.format(recall_score(y_true=test_Y_promise, y_pred=predict_y)))
                    f.write('F: {}\n'.format(f1_score(y_true=test_Y_promise, y_pred=predict_y)))
                    f.flush()





#               precision    recall  f1-score   support
#
#            0       0.88      0.77      0.82       747
#            1       0.38      0.57      0.46       188
#
#     accuracy                           0.73       935
#    macro avg       0.63      0.67      0.64       935
# weighted avg       0.78      0.73      0.75       935
#
# 0.38162544169611307
# 0.574468085106383
# 0.45859872611464964


