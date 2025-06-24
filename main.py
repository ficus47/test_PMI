import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

df = pd.read_excel("excel.xlsx", skiprows=3)

os.makedirs("output/", exist_ok=True)

column = [i.strip().replace("/", "") for i in df.columns]#["Type d'acteur",
         #"COMMUNE D'HABITATION",
         #"Age",
         #"Thème"] #[i.strip().replace("/", "") for i in df.columns]#

def unique(labels):
    final_dict = {}
    for i in labels:
        try:
            final_dict[i] += 1
        except Exception as e:
            final_dict[i] = 1
    return final_dict

#print(df.columns)

df = df.dropna(how='all')

#selected = df[column]
#
#print(selected, type(selected))

dict_for_classifying = {}

for i in column:
    dict_for_classifying[i] = []

    try:
        selected = df[i]
    except Exception:
        print(f"erreur sur {i}")
        if i == "DATE":
            selected = df[i+":"]
        continue

    for j in selected:
        if not (isinstance(j, float) and np.isnan(j)):
            dict_for_classifying[i].append(j)

value_dict = {
    "Age": {
        "65 ans et plus": 1,
        "58 ans": 2,
        "18-29 ans": 3
    },

    "Type d'acteur": {
        "Habitant": 1,
    },
}

real_temp_dict = {}

for j, y in dict_for_classifying.items():
    temp_dict = {}
    for i, k in zip(y, range(len(y))):
        if i == "DATE:":
            i = datetime.strptime(i, "%d/%m/%Y")
        temp_dict.update({i: k})

    real_temp_dict.update({j:temp_dict})


value_dict.update(real_temp_dict)
selected_dict = value_dict
#for i in column:
#    Not_value = False
#    selected_dict[i] = []
#
#    try:
#        selected_values_dict = value_dict[i]
#    except KeyError as e:
#        Not_value = True
#
#    for j in selected[i]:
#        if not (isinstance(j, float) and np.isnan(j)):
#            if not Not_value:
#                selected_dict[i].append(selected_values_dict[j])
#            else:
#                selected_dict[i].append(j)

for selected_class in value_dict.keys():
    labels = list(value_dict[selected_class].keys())

    percent = unique(selected_dict[selected_class])

    percent2 = list(percent.values())
    #for i, j in percent.items():
    #    percent2.update({i-min(list(percent.keys())): j})
    percent = percent2
    del percent2

    #print("percent ? : ", percent)
    first_labels = labels
    for i in range(len(labels)):
        labels[i] = str(labels[i])

    for i in range(len(labels)):
        labels[i] += " " + str(round(percent[i] / sum(percent) * 100, 3)) + "%"

    #print("truc random : ", unique(selected_dict[selected_class]).values(), selected_dict[selected_class])
    #print("labels : ", labels)
    
    plt.close()
    if selected_class.lower() != "date:":
        plt.figure(figsize=(7, 4))

        plt.title(selected_class, fontsize=14, color='red')
        x = unique(selected_dict[selected_class]).values()
        if len(x) == 0:
            continue
        plt.pie(x=x, labels=labels)#, explode=list(value_dict['Age'].values()))

    else:
        plt.title(selected_class, fontsize=14, color='red')
        x = unique(selected_dict[selected_class]).values()
        plt.plot(x, first_labels)
    #plt.legend(loc='best')
    plt.savefig("output/pie_"+str(selected_class)+".png")
