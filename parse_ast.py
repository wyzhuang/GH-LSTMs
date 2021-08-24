import javalang
import csv
import os
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

dict_dir = {"ant": ["src\main", "proposal\sandbox\junit\src\main"],
                "camel": ["camel-core\src\main\java", 'components\\camel-activemq\\src\\main\\java',
                          'components\\camel-bam\\src\\main\\java', 'components\\camel-cxf\\src\\main\\java',
                          'components\\camel-ftp\\src\\main\\java', 'components\\camel-http\\src\\main\\java',
                          'components\\camel-irc\\src\\main\\java', 'components\\camel-jaxb\\src\\main\\java',
                          'components\\camel-jbi\\src\\main\\java', 'components\\camel-jms\\src\\main\\java',
                          'components\\camel-josql\\src\\main\\java', 'components\\camel-jpa\\src\\main\\java',
                          'components\\camel-mail\\src\\main\\java', 'components\\camel-mina\\src\\main\\java',
                          'components\\camel-quartz\\src\\main\\java', 'components\\camel-rmi\\src\\main\\java',
                          'components\\camel-saxon\\src\\main\\java', 'components\\camel-script\\src\\main\\java',
                          'components\\camel-spring\\src\\main\\java', 'components\\camel-xmpp\\src\\main\\java',
                          'components\\pom.xml\\src\\main\\java', 'components\\camel-amqp\\src\\main\\java',
                          'components\\camel-atom\\src\\main\\java', 'components\\camel-groovy\\src\\main\\java',
                          'components\\camel-ibatis\\src\\main\\java', 'components\\camel-jdbc\\src\\main\\java',
                          'components\\camel-jetty\\src\\main\\java', 'components\\camel-jhc\\src\\main\\java',
                          'components\\camel-jing\\src\\main\\java', 'components\\camel-juel\\src\\main\\java',
                          'components\\camel-msv\\src\\main\\java', 'components\\camel-ognl\\src\\main\\java',
                          'components\\camel-osgi\\src\\main\\java', 'components\\camel-ruby\\src\\main\\java',
                          'components\\camel-stringtemplate\\src\\main\\java',
                          'components\\camel-velocity\\src\\main\\java', 'components\\camel-xmlbeans\\src\\main\\java',
                          'components\\camel-csv\\src\\main\\java', 'components\\camel-flatpack\\src\\main\\java',
                          'components\\camel-hamcrest\\src\\main\\java', 'components\\camel-jcr\\src\\main\\java',
                          'components\\camel-jxpath\\src\\main\\java', 'components\\camel-scala\\src\\main\\java',
                          'components\\camel-spring-integration\\src\\main\\java',
                          'components\\camel-sql\\src\\main\\java', 'components\\camel-stream\\src\\main\\java',
                          'components\\camel-supercsv\\src\\main\\java', 'components\\camel-swing\\src\\main\\java',
                          'components\\camel-testng\\src\\main\\java', 'components\\camel-uface\\src\\main\\java',
                          'components\\camel-xstream\\src\\main\\java', 'components\\camel-freemarker\\src\\main\\java',
                          'components\\camel-guice\\src\\main\\java', 'components\\camel-hl7\\src\\main\\java',
                          'components\\camel-jmxconnect\\src\\main\\java', 'components\\camel-jt400\\src\\main\\java',
                          'components\\camel-ldap\\src\\main\\java', 'components\\camel-rest\\src\\main\\java',
                          'components\\camel-restlet\\src\\main\\java', 'components\\camel-tagsoup\\src\\main\\java'],
                "jedit": [""], "log4j": ["src\java"], "lucene": ["src\java"], "poi": ["src\java"],
                "velocity": ["src\java"], "xalan": ["src", "compat_src"], "xerces": ["src"], "ivy": ["src\java"],
                "synapse": ["modules\core\src\main\java"]}

def parse_ast(path):
    data = open(path, encoding='utf-8').read()
    tree = javalang.parse.parse(data)
    res = []
    for path, node in tree:
        # res.append(node)
        pattern = javalang.tree.ReferenceType
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append('ReferenceType_' + node.name)
        pattern = javalang.tree.MethodInvocation
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append('MethodInvocation_' + node.member)
        pattern = javalang.tree.MethodDeclaration
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append('MethodDeclaration_' + node.name)
        pattern = javalang.tree.TypeDeclaration
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append('TypeDeclaration_' + node.name)
        pattern = javalang.tree.ClassDeclaration
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append('ClassDeclaration_' + node.name)
        pattern = javalang.tree.EnumDeclaration
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append('EnumDeclaration_' + node.name)
        pattern = javalang.tree.IfStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("ifstatement")
        pattern = javalang.tree.WhileStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("whilestatement")
        pattern = javalang.tree.DoStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("dostatement")
        pattern = javalang.tree.ForStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("forstatement")
        pattern = javalang.tree.AssertStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("assertstatement")
        pattern = javalang.tree.BreakStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("breakstatement")
        pattern = javalang.tree.ContinueStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("continuestatement")
        pattern = javalang.tree.ReturnStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("returnstatement")
        pattern = javalang.tree.ThrowStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("throwstatement")
        pattern = javalang.tree.SynchronizedStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("synchronizedstatement")
        pattern = javalang.tree.TryStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("trystatement")
        pattern = javalang.tree.SwitchStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("switchstatement")
        pattern = javalang.tree.BlockStatement
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("blockstatement")
        pattern = javalang.tree.StatementExpression
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("statementexpression")
        pattern = javalang.tree.TryResource
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("tryresource")
        pattern = javalang.tree.CatchClause
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("catchclause")
        pattern = javalang.tree.CatchClauseParameter
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("catchclauseparameter")
        pattern = javalang.tree.SwitchStatementCase
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("switchstatementcase")
        pattern = javalang.tree.ForControl
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("forcontrol")
        pattern = javalang.tree.EnhancedForControl
        if ((isinstance(pattern, type) and isinstance(node, pattern))):
            res.append("enhancedforcontrol")

    return ' '.join(res)


if __name__=="__main__":
    for project in projects:
        for version in versions[project]:
            promise_data = csv.reader(open( "./data/promise_data/{}/{}.csv".format(project,version), 'r'))
            next(promise_data)
            all_count=0
            exist_count=0
            sequence_and_label_file=open('./sequence_and_label/{}_{}.txt'.format(project,version), 'w+', encoding='utf-8')
            corpus_file=open('./corpus/{}_{}.txt'.format(project,version), 'w+', encoding='utf-8')
            for line in promise_data:
                file_name = line[0].replace(".", "\\").split("$")[0] + ".java"
                all_count+=1
                for pos_dir in dict_dir[project]:
                    path =  "./Code/{}/{}/{}".format(project,version,pos_dir)
                    file_path = path + "/" + file_name
                    if os.path.exists(file_path):
                        break
                else:
                    continue
                try:
                    file_sequence = parse_ast(file_path)
                    corpus_file.write(file_sequence+" ")
                    sequence_and_label_file.write(str({"sequence": file_sequence, "bug": line[-1]})+"\n")
                except Exception as e:
                    print("{}解析错误".format(file_path))



