import os

for dir in os.listdir("./"):
    if os.path.isdir(dir):
        for children in os.listdir("./"+dir):
            if ".txt" in children:
                read_file=open("./{}/{}".format(dir,children),"r+").readlines()
                for i in range(0,len(read_file)):
                    if len(read_file[i].split(" ")) != 2:
                        read_file=read_file[i:]
                        break
                write_file=open("./{}/{}".format(dir,children),"w+")
                write_file.write("{} {}\n".format(len(read_file),dir))
                for line in read_file:
                    write_file.write(line)