import streamlit as st

# Utility Functions
def clean_word_list(input_text):
    """Cleans input text by removing non-alphabetic characters."""
    return "\n".join(
        [line.strip() for line in input_text.split("\n") if line.strip()]
    )

def remove_letters(word_list, letters):
    """Removes specified letters from words in the list while considering counts."""
    letters_count = {letter: letters.count(letter) for letter in set(letters)}
    result = []

    for word in word_list.split("\n"):
        word_lower = word.lower()
        word_letters = list(word_lower)

        # Check if the word contains the necessary letters the required number of times
        for letter, count in letters_count.items():
            if word_letters.count(letter) < count:
                break
        else:
            # If the word has enough letters, proceed with removal
            for letter, count in letters_count.items():
                for _ in range(count):
                    if letter in word_letters:
                        word_letters.remove(letter)

            result.append(f"{word} ==> {''.join(word_letters)}")

    return "\n".join(result)

def is_sequential_in_word(word, sequence):
    """Checks if a sequence appears in the word in order (not necessarily adjacent)."""
    index = 0
    for char in sequence:
        index = word.find(char, index)
        if index == -1:
            return False
        index += 1
    return True

def is_consecutive_in_word(word, sequence):
    """Checks if a sequence appears in the word in order and adjacent."""
    return sequence in word

def is_reverse_sequential_in_word(word, sequence):
    """Checks if the reversed sequence appears in the word in order (not necessarily adjacent)."""
    reversed_sequence = sequence[::-1]
    return is_sequential_in_word(word, reversed_sequence)

def is_reverse_consecutive_in_word(word, sequence):
    """Checks if the reversed sequence appears in the word in order and adjacent."""
    reversed_sequence = sequence[::-1]
    return is_consecutive_in_word(word, reversed_sequence)

def sequence_checker(word_list, condition, match_type):
    """Filters words based on sequence match type."""
    results = []
    for word in word_list.split("\n"):
        word_lower = word.lower()
        if match_type == "sequential" and is_sequential_in_word(word_lower, condition.lower()):
            results.append(word)
        elif match_type == "consecutive" and is_consecutive_in_word(word_lower, condition.lower()):
            results.append(word)
        elif match_type == "reverse_sequential" and is_reverse_sequential_in_word(word_lower, condition.lower()):
            results.append(word)
        elif match_type == "reverse_consecutive" and is_reverse_consecutive_in_word(word_lower, condition.lower()):
            results.append(word)
    return "\n".join(results)

# Streamlit App
st.title("Word Puzzle Analyzer")

# Upload or Paste Words
uploaded_file = st.file_uploader("Upload a file (TXT):", type=["txt"])
input_text = st.text_area("Or paste your words here:", height=200)

# If a file is uploaded, display its content in the text area
if uploaded_file:
    input_text = uploaded_file.read().decode("utf-8")
    st.text_area("Uploaded Words:", value=input_text, height=200, disabled=True)

# Functionality Selection
st.header("Select Functionality")
functionality = st.radio(
    "Choose a functionality:", 
    ["Letter Removal", "Sequence Checker"]
)

# Letter Removal
if functionality == "Letter Removal":
    letters_to_remove = st.text_input("Enter letters to remove (e.g., 'aeiou'):")
    if st.button("Remove Letters"):
        if input_text:
            result = remove_letters(input_text, letters_to_remove)
            st.text_area("Results:", value=result, height=200, disabled=True)
        else:
            st.warning("Please upload a file or paste text.")

# Sequence Checker
elif functionality == "Sequence Checker":
    condition = st.text_input("Enter the sequence to check:")
    match_type = st.selectbox("Match Type:", ["sequential", "consecutive", "reverse_sequential", "reverse_consecutive"])
    if st.button("Check Sequences"):
        if input_text:
            result = sequence_checker(input_text, condition, match_type)
            st.text_area("Results:", value=result, height=200, disabled=True)
        else:
            st.warning("Please upload a file or paste text.")

# Download Results
if st.button("Download Results"):
    if input_text:
        st.download_button(
            label="Download Results",
            data=input_text,
            file_name="results.txt",
            mime="text/plain",
        )
    else:
        st.warning("No results to download.")
