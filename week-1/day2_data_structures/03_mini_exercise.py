# 03_mini_exercise.py

def count_word_frequencies(text):
    """
    This function takes a string and returns a dictionary 
    with the frequency of each word.
    """
    # Convert text to lowercase and split into words (List)
    words = text.lower().split()
    
    # Empty dictionary to store counts
    word_count = {}
    
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
            
    return word_count

# Testing the exercise
sample_text = "Python is great and Python is easy to learn"
result = count_word_frequencies(sample_text)

print(f"Text: '{sample_text}'")
print("Word Frequencies:")
for key, value in result.items():
    print(f"- '{key}': {value}")