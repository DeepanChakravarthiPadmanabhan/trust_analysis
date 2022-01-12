import pickle
with open('questions.pkl', 'rb') as f:
    a = pickle.load(f)

for i in a:
    print(i)
    if i['unique_id'] == 77:
        print(i)