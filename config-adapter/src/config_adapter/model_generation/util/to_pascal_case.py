def to_pascal_case(input_string: str) -> str:
    """Converts string to PascalCase."""
    # Split the string by non-alphabetic characters (whitespace and underscores)
    words: list[str] = []
    current_word = ""
    for char in input_string.strip():
        if char.isalpha():
            current_word += char
        else:
            if current_word:
                words.append(current_word)
                current_word = ""
    if current_word:  # Append any remaining word
        words.append(current_word)

    # Capitalize the first letter of each word and join them together
    pascal_case_string = "".join(word[0].capitalize() + word[1:] for word in words)
    return pascal_case_string


print(to_pascal_case("helloWorld"))
