#DL 1st, password generator

import os
import msvcrt
import random

# Function to display interactive menu with arrow key navigation
def menu(options, **mod):
    # Get which options should be number inputs and which should be toggles
    number = mod.get('number', [])
    toggle = mod.get('toggle', [])
    index = 0
    
    # Initialize numeric values - create dictionary to store numbers for each number option
    num = {}
    for i in number:
        num[i] = 4  # Default starting value
    
    # Initialize toggle values - create dictionary to store True/False for each toggle option
    tog = {}
    for i in toggle:
        tog[i] = True # Default to True
    
    error_message = ""
    
    # Main menu loop - keeps running until user presses Enter
    while True:
        os.system('cls')
        
        # Calculate minimum required length based on how many toggles are True
        min_length = sum(1 for i in toggle if tog.get(i, False))
        
        # Auto-adjust length if it's less than minimum - prevents invalid passwords
        if 0 in num and num[0] < min_length:
            num[0] = min_length
        
        # Display all menu options with current selection marked with ">"
        for i, option in enumerate(options):
            prefix = "> " if i == index else "  "
            
            # Display toggle options with True/False status
            if i in toggle:
                status = "True" if tog[i] else "False"
                print(f"{prefix}{option}: {status}")
            # Display number options with current value in brackets
            elif i in number:
                print(f"{prefix}{option} <{num[i]}>")
            # Display regular options (like Generate Password, Return)
            else:
                print(f"{prefix}{option}")
        
        # Display navigation instructions at bottom of menu
        print("\nUse side arrow keys to change values, up/down to change option, and enter to select")
        
        # Get key press from user
        key = msvcrt.getch()
        
        # Check if it's a special key (arrow keys are two bytes)
        if key in (b'\x00', b'\xe0'):
            key = msvcrt.getch()
        
        # Handle up arrow - move selection up
        if key == b"H":
            index = (index - 1) % len(options)
        # Handle down arrow - move selection down
        elif key == b"P":
            index = (index + 1) % len(options)
        # Handle left arrow - decrease number or toggle False
        elif key == b"K":
            if index in number:
                # Decrease number but don't go below minimum length
                if num[index] > min_length if index == 0 else num[index] > 1:
                    num[index] -= 1
            elif index in toggle:
                # Toggle the True/False value
                tog[index] = not tog[index]
        # Handle right arrow - increase number or toggle True
        elif key == b"M":
            if index in number:
                # Increase the number value
                num[index] += 1
            elif index in toggle:
                # Toggle the True/False value
                tog[index] = not tog[index]
        # Handle Enter key - confirm selection and exit menu
        elif key == b"\r":
            # Return all the settings as a dictionary
            return {'index': index, 'numbers': num, 'toggles': tog}


# Function to generate a single password based on requirements
def generate_password(requirements):
    # Extract all requirements from the list
    password_len = requirements[0]
    lower_case = requirements[1] 
    upper_case = requirements[2] 
    numbers = requirements[3]
    special_chars = requirements[4]

    # Track how many random characters we still need to add
    remaining_chars = password_len
    # List to store which character types are allowed
    password_requirements = []

    # List to store the blueprint of the password (what type each character should be)
    password_outline = []
    # List to store the actual password characters
    password = []

    # If lowercase is required, add one lowercase character to outline and mark it as allowed
    if lower_case == True:
        password_outline.append([1])
        remaining_chars -= 1
        password_requirements.append(1)
    # If uppercase is required, add one uppercase character to outline and mark it as allowed
    if upper_case == True:
        password_outline.append([2])
        remaining_chars -= 1
        password_requirements.append(2)
    # If numbers are required, add one number character to outline and mark it as allowed
    if numbers == True:
        password_outline.append([3])
        remaining_chars -= 1
        password_requirements.append(3)
    # If special chars are required, add one special character to outline and mark it as allowed
    if special_chars == True:
        password_outline.append([4])
        remaining_chars -= 1
        password_requirements.append(4)

    # Error handling - make sure at least one character type is selected
    if not password_requirements:
        return "Error: Please select at least one character type"

    # Fill the rest of the password with random character types from allowed types
    for i in range(remaining_chars):
        password_outline.append([random.choice(password_requirements)])

    # Shuffle the outline so required characters aren't always at the start
    random.shuffle(password_outline)

    # Convert each character type number into an actual random character
    for x in password_outline:
        char_type = x[0]
        # Type 1 = lowercase letter (a-z using ASCII 97-122)
        if char_type == 1:
            password.append(chr(random.randint(97, 122)))
        # Type 2 = uppercase letter (A-Z using ASCII 65-90)
        elif char_type == 2:
            password.append(chr(random.randint(65, 90)))
        # Type 3 = number (0-9 using ASCII 48-57)
        elif char_type == 3:
            password.append(chr(random.randint(48, 57)))
        # Type 4 = special character (select from common special chars)
        elif char_type == 4:
            password.append(chr(random.choice([33, 35, 36, 37, 38, 42, 43, 45, 61, 63, 64])))
    
    # Join all characters into one string and return the password
    return ''.join(password)


# Main program loop - keeps running until user chooses to exit
while True:
    # Show main menu with Generate Password and Exit options
    main_choice = menu(
        ["Generate Password", "Exit Program"],
        number=[],
        toggle=[]
    )
    
    # If user selected "Generate Password"
    if main_choice['index'] == 0:
        # Show password settings menu where user configures password requirements
        output = menu(
            ["Password Length", "Lowercase", "Uppercase", "Numbers", "Special Characters", "Number of Passwords", "Generate Password", "Return"],
            number=[0, 5],  # Indices 0 and 5 are number inputs
            toggle=[1, 2, 3, 4]  # Indices 1-4 are toggle inputs
        )

        # If user selected "Return", go back to main menu
        if output['index'] == 7:
            continue
        
        # Extract all the settings user chose
        password_length = output['numbers'][0]
        lowercase = output['toggles'][1]
        uppercase = output['toggles'][2]
        numbers = output['toggles'][3]
        special_chars = output['toggles'][4]
        num_passwords = output['numbers'][5]
        selected_index = output['index']

        # Clear screen and display generated passwords
        os.system('cls')
        print("Generated Passwords:")
        # Generate the requested number of passwords
        for i in range(num_passwords):
            result = generate_password([password_length, lowercase, uppercase, numbers, special_chars])
            print(f"{i+1}. {result}")
        
        # Wait for user to press Enter before returning to main menu
        input("\nPress Enter to return to main menu...")
    
    # If user selected "Exit Program", break out of loop and end program
    elif main_choice['index'] == 1:
        break