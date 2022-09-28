# GH-LSTMs
Software defect prediction based on gated hierarchical LSTMs

简单讲一下各个代码文件作用和运行步骤（以下仅以"ant"项目为例，其他项目的promise数据集也已经打包上传）

1.首先通过“parse_ast.py”提取对应项目版本的AST序列，生成两部分，一部分是"corpus"文件夹下的语料库，另一部分是“sequence_and_label”文件夹下的AST序列-标签对，以方便后续进一步处理。

2.通过“GloVe”下的"demo.sh"生成基于GloVe方法的词向量模型，由于测试集的词向量是由训练集的词向量模型生成的，所以“ant”项目的1.7版本词向量模型无需生成。这里最好放在linux服务器上进行，在本地可能会出现bug，词向量模型存放在“GloVe/models”下。

3.运行“GloVe/models”下“glove_title.py“文件。这里解释一下，我们后续是通过“gensim.models.KeyedVectors.load_word2vec_format”方法加载词向量模型，这个word2vec的方法与GloVe生成的词向量模型不太兼容，解决方法很多，我们这里就是简单的在文件开头写上词向量模型的词数和维度，让这个方法可以正确识别词向量模型。

4.运行"train_test_sets_generation.py"文件生成训练集和测试集，生成结果我打包上传了，下载解压既可。

5.执行“GH-LSTM.py”程序进行训练。这里还有一个很大的坑，就是我们之前做实验是直接保存模型的，但是TensorFlow有bug，某些你自定义的层会无法保存，导致加载模型时会丢失参数，所以我们现在是直接保存训练结束后的预测结果。这个bug已经有不少人报告过，不知道现在有没有被解决。
