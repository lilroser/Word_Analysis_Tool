import streamlit as st

# Utility Functions
def clean_word_list(input_text):
    """Cleans input text by removing non-alphabetic characters."""
    return "\n".join(
        [line.strip() for line in input_text.split("\n") if line.strip()]
    )

def remove_letters(word_list, letters):
    """Removes specified letters from each word in the list."""
    result = []
    for word in word_list.split("\n"):
        modified_word = "".join([char for char in word if char not in letters])
        result.append(f"{word} ==> {modified_word}")
    return "\n".join(result)

def is_sequence_in_word(word, sequence):
    """Checks if a sequence exists in the word."""
    index = 0
    for char in sequence:
        index = word.find(char, index)
        if index == -1:
            return False
        index += 1
    return True

def check_conditions(word, condition_a, type_a, condition_b, type_b, boolean_operator):
    """Checks conditions on a word with specified logic."""
    a_result = is_sequence_in_word(word, condition_a) if type_a == "sequential" else condition_a in word
    b_result = is_sequence_in_word(word, condition_b) if type_b == "sequential" else condition_b in word

    if boolean_operator == "AND":
        return a_result and b_result
    elif boolean_operator == "OR":
        return a_result or b_result
    elif boolean_operator == "NEITHER":
        return not (a_result or b_result)
    return False

# Streamlit App
st.title("Word Puzzle Analyzer")

# Upload or Paste Words
uploaded_file = st.file_uploader("Upload a file (TXT):", type=["txt"])
input_text = st.text_area("Or paste your words here:", height=200)

# If a file is uploaded, display its content in the text area
if uploaded_file:
    input_text = uploaded_file.read().decode("utf-8")
    st.text_area("Uploaded Words:", value=input_text, height=200, disabled=True)

# Display cleaned word list
if st.button("Clean Word List"):
    if input_text:
        cleaned_text = clean_word_list(input_text)
        st.text_area("Cleaned Word List:", value=cleaned_text, height=200, disabled=True)
    else:
        st.warning("Please upload a file or paste text.")

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
    condition_a = st.text_input("Condition A (sequence to find):")
    condition_b = st.text_input("Condition B (sequence to find):")
    type_a = st.selectbox("Type for Condition A:", ["sequential", "contains"])
    type_b = st.selectbox("Type for Condition B:", ["sequential", "contains"])
    boolean_operator = st.selectbox("Boolean Operator:", ["AND", "OR", "NEITHER"])
    if st.button("Check Sequences"):
        results = []
        if input_text:
            for word in input_text.split("\n"):
                if check_conditions(word, condition_a, type_a, condition_b, type_b, boolean_operator):
                    results.append(word)
            st.text_area("Results:", value="\n".join(results), height=200, disabled=True)
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
