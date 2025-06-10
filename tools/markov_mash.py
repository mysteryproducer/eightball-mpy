import pickle

markov_table=dict()
files=["test/verne/verne en.txt","test/verne/verne fr.txt"]
order=3
for filename in files:
    all_data=""
    with open(filename,"r") as in_stream:
        all_data=in_stream.read()
        all_data=all_data.replace("\r\n","\n").replace("\n\n","\r")\
                        .replace("\n","").replace("\r","\n")
    for i in range(order,len(all_data)):
        key=all_data[i-3:i]
        value=all_data[i]
        if key in markov_table:
            subtable=markov_table[key]
        else:
            subtable=dict()
            markov_table[key]=subtable
        counter=(subtable[value] if value in subtable else 0) + 1
        subtable[value]=counter
for prefix in markov_table.keys():
    subtable=markov_table[prefix]
    total=sum(subtable.values())
    tx=list()
    ix=0
    for subkey in subtable.keys():
        ix += subtable[subkey] / total
        tx.append((ix,subkey))
    markov_table[prefix]=tx
#print(markov_table)
with open(f"test/verne/verne{order}.bin","wb") as out_file:
    pickle.dump(markov_table,out_file)
