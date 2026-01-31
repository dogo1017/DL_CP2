#DL 1st, morse code 
import os
# Define tuples for English letters and corresponding Morse Code symbols
ENGLISH = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
           '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ')

MORSE = ('.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---',
         '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-',
         '..-', '...-', '.--', '-..-', '-.--', '--..', '.----', '..---', '...--',
         '....-', '.....', '-....', '--...', '---..', '----.', '-----', '/')

# function to Convert an English message to Morse Code, Parameters are message in English text to translate, Returns morse_message or the translated Morse Code
def english_to_morse(message):
    # Initialize empty string to store morse code translation
    morse_message = ""
    
    # Convert message to uppercase for matching with tuple
    message = message.upper()
    
    # Loop through each character in the message
    for char in message:
        try:
            # Find the index of the character in the ENGLISH tuple
            index = ENGLISH.index(char)
            # Use that index to get corresponding morse code symbol
            morse_message += MORSE[index] + " "
        except ValueError:
            # Handle error if character is not in ENGLISH tuple
            print(f"Warning: Character '{char}' cannot be translated to Morse Code. Skipping.")
    
    return morse_message.strip()

# function to Convert an Morse code message to english, Parameters are message in Morse Code to translate, Returns translated English message
def morse_to_english(morse_message):

    # Initialize empty string to store english translation
    english_message = ""
    
    # Split the morse code by spaces to get individual symbols
    morse_symbols = morse_message.split(" ")
    
    # Loop through each morse code symbol
    for symbol in morse_symbols:
        try:
            # Find the index of the symbol in the MORSE tuple
            index = MORSE.index(symbol)
            # Use that index to get corresponding english character
            english_message += ENGLISH[index]
        except ValueError:
            # Handle error if symbol is not in MORSE tuple
            print(f"Warning: Morse symbol '{symbol}' is not recognized. Skipping.")
    
    return english_message.lower()

# Display the main menu options to the user
def display_menu():
    print("MORSE CODE TRANSLATOR")
    print("1. Translate from Morse Code to English")
    print("2. Translate from English to Morse Code")
    print("3. Exit")

# Main program loop, displays menu and handles user choices
def main():
    # Clear screen and display welcome message
    os.system('cls')
    print("\nWelcome to the Morse Code Translator!")
    print("This program can translate between English and Morse Code.")
    print("For Morse Code input, separate each symbol with a space.")
    print("Use '/' to represent a space between words.")
    input("\nPress Enter to continue...")
    
    # Main program loop - continues until user chooses to exit
    while True:
        # Clear screen and display menu options
        os.system('cls')
        display_menu()
        
        # Get user's menu choice
        choice = input("\nEnter your choice (1-3): ").strip()
        
        # Process user's choice
        if choice == "1":
            # Clear screen for translation
            os.system('cls')
            # Translate Morse Code to English
            print("\nMORSE CODE TO ENGLISH")
            morse_input = input("What is the code you need translated?\n").strip()
            
            # Call translation function
            english_output = morse_to_english(morse_input)
            
            # Display result
            print("\nYour message says:")
            print(english_output)
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            # Clear screen for translation
            os.system('cls')
            # Translate English to Morse Code
            print("\nENGLISH TO MORSE CODE")
            english_input = input("What is the message you need translated?\n").strip()
            
            # Call translation function
            morse_output = english_to_morse(english_input)
            
            # Display result
            print("\nYour message says:")
            print(morse_output)
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            # Clear screen and exit the program
            os.system('cls')
            print("\nThank you for using the Morse Code Translator!")
            print("Goodbye!")
            break
            
        else:
            # Clear screen and handle invalid menu choice
            os.system('cls')
            print("\nInvalid choice. Please enter 1, 2, or 3.")
            input("Press Enter to continue...")
            
main()