import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("excel.xlsx", skiprows=3)

column = ["Type d'acteur",
          "COMMUNE D'HABITATION",
          "Age",]

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

selected = df[column]

#print(selected, type(selected))

dict_for_classifying = {}

for i in column:
    dict_for_classifying[i] = []

    for j in selected[i]:
        if not (isinstance(j, float) and np.isnan(j)):
            dict_for_classifying[i].append(j)

print(dict_for_classifying)

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
    for i, k in zip(y, range(len(j))):
        temp_dict.update({i: k})

    real_temp_dict.update({j:temp_dict})

print(real_temp_dict)

value_dict.update(dict_for_classifying)
selected_dict = {}

for i in column:
    Not_value = False
    selected_dict[i] = []

    try:
        selected_values_dict = value_dict[i]
    except KeyError as e:
        Not_value = True

    for j in selected[i]:
        if not (isinstance(j, float) and np.isnan(j)):
            if not Not_value:
                selected_dict[i].append(selected_values_dict[j])
            else:
                selected_dict[i].append(j)


print(selected_dict)

plt.pie(x=unique(selected_dict["Age"]).values(), labels=list(value_dict['Age'].keys()))#, explode=list(value_dict['Age'].values()))
plt.legend()
plt.savefig("first_plt.png")