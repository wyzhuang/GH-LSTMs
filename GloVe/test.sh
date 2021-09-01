
arr_dimension=(15 25 35 45 55 65)
arr_project=("ambari" "ant" "felix" "jackrabbit" "jenkins" "lucene-solr")
for VECTOR_SIZE in ${arr_dimension[@]};do
    for SAVE_FILE in ${arr_project[@]};do
        CORPUS=../corpus/$SAVE_FILE.txt
        echo $VECTOR_SIZE/$CORPUS
    done
done