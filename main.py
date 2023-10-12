# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# import torch
# import pandas as pd



# tokenizer = AutoTokenizer.from_pretrained("microsoft/tapex-large-finetuned-wtq")
# model = AutoModelForSeq2SeqLM.from_pretrained("microsoft/tapex-large-finetuned-wtq")

# # prepare table + question
# data = {"Actors": ["Brad Pitt", "Leonardo Di Caprio", "George Clooney"], "Number of movies": ["87", "53", "69"]}
# table = pd.DataFrame.from_dict(data)
# question = "how many movies does Leonardo Di Caprio have?"

# # encode question + table
# encoding=tokenizer(table, question, return_tensors="pt")
# # let the model generate an answer autoregressively
# outputs = model.generate(**encoding)

# # decode back to text
# predicted_answer = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
# print(predicted_answer)





# def translate(text):
#     inputs = tokenizer.encode(text, return_tensors="pt")
#     outputs = model.generate(inputs, max_length=40, num_beams=4, early_stopping=True)
#     return tokenizer.decode(outputs[0])

# def translate_file(file_name):
#     df = pd.read_csv(file_name)
#     df['translation'] = df['text'].apply(translate)
#     df.to_csv(file_name, index=False)

# translate_file('data.csv')  



from website import create_app


app= create_app()

if __name__=="__main__":

    app.run(debug=True)
    