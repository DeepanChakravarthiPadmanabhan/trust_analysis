import pickle
with open('questions.pkl', 'rb') as f:
    a = pickle.load(f)
print(a)
