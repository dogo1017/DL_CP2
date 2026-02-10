from menu import menu
import csv


# Load movie data from CSV file and return as dictionary
def load_movies(filepath):
    movies = {}  # Dictionary to store all movie data
    
    try:
        # Open CSV file with UTF-8 encoding
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)  # Create CSV reader
            headers = next(reader)  # Get column names from first row
            
            # Create empty list for each column
            for header in headers:
                movies[header] = []
            
            # Read each row and add values to dictionary
            for row in reader:
                # Skip empty rows
                if not row or all(cell.strip() == '' for cell in row):
                    continue
                
                # Pad rows that are too short with empty strings
                while len(row) < len(headers):
                    row.append('')
                
                # Add each cell value to its corresponding column list
                for i, value in enumerate(row):
                    if i < len(headers):
                        movies[headers[i]].append(value)
                    
    except FileNotFoundError:
        print("The file 'movies.csv' containing the movie data could not be found")
        exit()  # Stop program if file not found
    
    return movies


# Extract and return sorted lists of unique genres, directors, and actors
def extract_unique_values(movies):
    # Get unique genres
    all_genres = set()  # Use set to avoid duplicates
    for genre_str in movies['Genre']:  # Loop through all genre strings
        genres = genre_str.split('/')  # Split multi-genre strings on '/'
        for g in genres:  # Add each individual genre
            all_genres.add(g.strip())  # Remove whitespace
    genre_list = sorted(list(all_genres))  # Convert to sorted list
    
    # Get unique directors
    director_list = sorted(list(set(movies['Director'])))  # Remove duplicates and sort
    
    # Get unique actors
    all_actors = set()  # Use set to avoid duplicates
    for actor_str in movies['Notable Actors']:  # Loop through all actor strings
        actors = actor_str.split(',')  # Split multi-actor strings on ','
        for a in actors:  # Add each individual actor
            all_actors.add(a.strip())  # Remove whitespace
    actor_list = sorted(list(all_actors))  # Convert to sorted list
    
    return genre_list, director_list, actor_list


# Display welcome screen with instructions
def show_intro():
    print("=" * 80)
    print("MOVIE RECOMMENDER SYSTEM".center(80))
    print("=" * 80)
    print("\nWelcome! This program helps you find movies based on your preferences.")
    print("\nFeatures:")
    print("  - Search by genre, director, actor, and/or length")
    print("  - View detailed information for any movie")
    print("  - Browse the complete movie list")
    print("\nNavigation:")
    print("  - Use UP/DOWN arrow keys to move through options")
    print("  - Use LEFT/RIGHT arrow keys to toggle filters or adjust numbers")
    print("  - Press ENTER to select an option")
    print("\n" + "=" * 80)
    input("\nPress ENTER to continue...")


# Show detailed information for a single movie
def display_movie_details(movies, movie_idx):
    # Build list of formatted movie details
    movie_details = [
        f"Title: {movies['Title'][movie_idx]}",
        f"Director: {movies['Director'][movie_idx]}",
        f"Genre: {movies['Genre'][movie_idx]}",
        f"Rating: {movies['Rating'][movie_idx]}",
        f"Length: {movies['Length (min)'][movie_idx]} min",
        f"Actors: {movies['Notable Actors'][movie_idx]}",
        'return'
    ]
    menu(movie_details)  # Display details in menu


# Show complete list of all movies
def display_full_movie_list(movies, movie_titles):
    # Create menu with all movie titles plus return option
    print_result = menu(movie_titles + ['return'])
    print_index = print_result['index']  # Get which option was selected
    
    # If user selected a movie (not return), show its details
    if print_index < len(movie_titles):
        display_movie_details(movies, print_index)


# Reapply all active filters to get current filtered movie list
def apply_all_filters(movies, genre_active, selected_genres, director_active, selected_directors, 
                      actor_active, selected_actors, length_active, min_length, max_length):
    # Start with all movies
    filtered_titles = list(range(len(movies['Title'])))
    
    # Apply genre filter if active
    if genre_active:
        new_filtered = []  # Build new filtered list
        for idx in filtered_titles:  # Check each movie
            movie_genres = movies['Genre'][idx]  # Get movie's genres
            # If any selected genre is in movie's genres, keep it
            if any(genre in movie_genres for genre in selected_genres):
                new_filtered.append(idx)
        filtered_titles = new_filtered  # Update filtered list
    
    # Apply director filter if active
    if director_active:
        new_filtered = []  # Build new filtered list
        for idx in filtered_titles:  # Check each remaining movie
            # If movie's director is in selected directors, keep it
            if movies['Director'][idx] in selected_directors:
                new_filtered.append(idx)
        filtered_titles = new_filtered  # Update filtered list
    
    # Apply actor filter if active
    if actor_active:
        new_filtered = []  # Build new filtered list
        for idx in filtered_titles:  # Check each remaining movie
            movie_actors = movies['Notable Actors'][idx]  # Get movie's actors
            # If any selected actor is in movie's actors, keep it
            if any(actor in movie_actors for actor in selected_actors):
                new_filtered.append(idx)
        filtered_titles = new_filtered  # Update filtered list
    
    # Apply length filter if active
    if length_active:
        new_filtered = []  # Build new filtered list
        for idx in filtered_titles:  # Check each remaining movie
            movie_length = int(movies['Length (min)'][idx])  # Get movie's length
            # If movie length is within range, keep it
            if min_length <= movie_length <= max_length:
                new_filtered.append(idx)
        filtered_titles = new_filtered  # Update filtered list
    
    return filtered_titles  # Return final filtered list


# Handle genre filter selection and application
def handle_genre_filter(movies, genre_list, genre_active, selected_genres, 
                        director_active, selected_directors, actor_active, selected_actors, 
                        length_active, min_length, max_length):
    # Create list of False values for all genres
    default_genre_vals = [False] * len(genre_list)
    
    # If filter already active, pre-check currently selected genres
    if genre_active:
        for i, genre in enumerate(genre_list):
            if genre in selected_genres:
                default_genre_vals[i] = True  # Set to True if previously selected
    
    # Show genre selection menu with toggles
    genre_result = menu(
        genre_list + ['Apply Filter', 'Cancel'],  # Options list
        toggle=list(range(len(genre_list))),  # Make all genres toggleable
        default_vals=default_genre_vals  # Set initial toggle states
    )
    
    # Get list of selected genres (ones that are toggled True)
    new_selected_genres = [genre_list[i] for i in range(len(genre_list)) if genre_result['toggles'].get(i, False)]
    
    # Check if user clicked Apply Filter and selected at least one genre
    if genre_result['index'] == len(genre_list) and new_selected_genres:
        # Reapply all filters with new genre selection
        filtered_titles = apply_all_filters(movies, True, new_selected_genres, director_active, selected_directors, actor_active, selected_actors, length_active, min_length, max_length)
        return True, new_selected_genres, filtered_titles  # Return updated state
    
    # If user clicked Cancel, return unchanged
    return genre_active, selected_genres, None


# Handle director filter selection and application
def handle_director_filter(movies, director_list, director_active, selected_directors,
                          genre_active, selected_genres, actor_active, selected_actors,
                          length_active, min_length, max_length):
    # Create list of False values for all directors
    default_director_vals = [False] * len(director_list)
    
    # If filter already active, pre-check currently selected directors
    if director_active:
        for i, director in enumerate(director_list):
            if director in selected_directors:
                default_director_vals[i] = True  # Set to True if previously selected
    
    # Show director selection menu with toggles
    director_result = menu(
        director_list + ['Apply Filter', 'Cancel'],  # Options list
        toggle=list(range(len(director_list))),  # Make all directors toggleable
        default_vals=default_director_vals  # Set initial toggle states
    )
    
    # Get list of selected directors (ones that are toggled True)
    new_selected_directors = [director_list[i] for i in range(len(director_list)) if director_result['toggles'].get(i, False)]
    
    # Check if user clicked Apply Filter and selected at least one director
    if director_result['index'] == len(director_list) and new_selected_directors:
        # Reapply all filters with new director selection
        filtered_titles = apply_all_filters(movies, genre_active, selected_genres, True, new_selected_directors, actor_active, selected_actors, length_active, min_length, max_length)
        return True, new_selected_directors, filtered_titles  # Return updated state
    
    # If user clicked Cancel, return unchanged
    return director_active, selected_directors, None


# Handle actor filter selection and application
def handle_actor_filter(movies, actor_list, actor_active, selected_actors,
                       genre_active, selected_genres, director_active, selected_directors,
                       length_active, min_length, max_length):
    # Create list of False values for all actors
    default_actor_vals = [False] * len(actor_list)
    
    # If filter already active, pre-check currently selected actors
    if actor_active:
        for i, actor in enumerate(actor_list):
            if actor in selected_actors:
                default_actor_vals[i] = True  # Set to True if previously selected
    
    # Show actor selection menu with toggles
    actor_result = menu(
        actor_list + ['Apply Filter', 'Cancel'],  # Options list
        toggle=list(range(len(actor_list))),  # Make all actors toggleable
        default_vals=default_actor_vals  # Set initial toggle states
    )
    
    # Get list of selected actors (ones that are toggled True)
    new_selected_actors = [actor_list[i] for i in range(len(actor_list)) if actor_result['toggles'].get(i, False)]
    
    # Check if user clicked Apply Filter and selected at least one actor
    if actor_result['index'] == len(actor_list) and new_selected_actors:
        # Reapply all filters with new actor selection
        filtered_titles = apply_all_filters(movies, genre_active, selected_genres, director_active, selected_directors, True, new_selected_actors, length_active, min_length, max_length)
        return True, new_selected_actors, filtered_titles  # Return updated state
    
    # If user clicked Cancel, return unchanged
    return actor_active, selected_actors, None


# Handle length filter selection and application
def handle_length_filter(movies, length_active, min_length, max_length,
                        genre_active, selected_genres, director_active, selected_directors,
                        actor_active, selected_actors):
    # Show length selection menu with number inputs
    length_result = menu(
        ['Minimum Length', 'Maximum Length', 'Apply Filter', 'Cancel'],  # Options list
        number=[0, 1]  # Make first two options have number inputs
    )
    
    # Check if user clicked Apply Filter
    if length_result['index'] == 2:
        # Get min and max length from number inputs (default to 1 and 200)
        new_min_length = length_result['numbers'].get(0, 1)
        new_max_length = length_result['numbers'].get(1, 200)
        
        # Reapply all filters with new length range
        filtered_titles = apply_all_filters(movies, genre_active, selected_genres, director_active, selected_directors, actor_active, selected_actors, True, new_min_length, new_max_length)
        return True, new_min_length, new_max_length, filtered_titles  # Return updated state
    
    # If user clicked Cancel, return unchanged
    return length_active, min_length, max_length, None


# Main search interface with filter selection
def search_movies(movies, movie_titles, genre_list, director_list, actor_list):
    # Start with all movies visible
    filtered_titles = list(range(len(movie_titles)))
    
    # Initialize filter states (all inactive at start)
    selected_genres = []
    selected_directors = []
    selected_actors = []
    min_length = None
    max_length = None
    genre_active = False
    director_active = False
    actor_active = False
    length_active = False
    
    # Main filter loop
    while True:
        # Build display list with currently filtered movies
        display_titles = [movie_titles[i] for i in filtered_titles]
        
        # Create status indicators for each filter
        genre_status = '✓ Active' if genre_active else '✗'
        director_status = '✓ Active' if director_active else '✗'
        actor_status = '✓ Active' if actor_active else '✗'
        length_status = '✓ Active' if length_active else '✗'
        
        # Show menu with filtered movies and filter options
        selection_result = menu(
            display_titles +  # Current filtered movies
            ['--- FILTERS ---',  # Separator
             f'Genre Filter {genre_status}',  # Genre filter option
             f'Director Filter {director_status}',  # Director filter option
             f'Actor Filter {actor_status}',  # Actor filter option
             f'Length Filter {length_status}',  # Length filter option
             'return']  # Return to main menu option
        )
        selection = selection_result['index']  # Get selected option index
        
        # User selected a movie from the filtered list
        if selection < len(filtered_titles):
            movie_idx = filtered_titles[selection]  # Get actual movie index
            display_movie_details(movies, movie_idx)  # Show movie details
        
        # User selected the separator (do nothing)
        elif selection == len(filtered_titles):
            continue
        
        # User selected Genre Filter
        elif selection == len(filtered_titles) + 1:
            # Handle genre filter selection
            genre_active, selected_genres, new_filtered = handle_genre_filter(
                movies, genre_list, genre_active, selected_genres,
                director_active, selected_directors, actor_active, selected_actors,
                length_active, min_length, max_length
            )
            # Update filtered list if filter was applied
            if new_filtered is not None:
                filtered_titles = new_filtered
        
        # User selected Director Filter
        elif selection == len(filtered_titles) + 2:
            # Handle director filter selection
            director_active, selected_directors, new_filtered = handle_director_filter(
                movies, director_list, director_active, selected_directors,
                genre_active, selected_genres, actor_active, selected_actors,
                length_active, min_length, max_length
            )
            # Update filtered list if filter was applied
            if new_filtered is not None:
                filtered_titles = new_filtered
        
        # User selected Actor Filter
        elif selection == len(filtered_titles) + 3:
            # Handle actor filter selection
            actor_active, selected_actors, new_filtered = handle_actor_filter(
                movies, actor_list, actor_active, selected_actors,
                genre_active, selected_genres, director_active, selected_directors,
                length_active, min_length, max_length
            )
            # Update filtered list if filter was applied
            if new_filtered is not None:
                filtered_titles = new_filtered
        
        # User selected Length Filter
        elif selection == len(filtered_titles) + 4:
            # Handle length filter selection
            length_active, min_length, max_length, new_filtered = handle_length_filter(
                movies, length_active, min_length, max_length,
                genre_active, selected_genres, director_active, selected_directors,
                actor_active, selected_actors
            )
            # Update filtered list if filter was applied
            if new_filtered is not None:
                filtered_titles = new_filtered
        
        # User selected return
        else:
            break  # Exit to main menu


# Main program entry point
def main():
    # Load movie data from CSV file
    movies = load_movies('individual_projects/movie_recommender/movies.csv')
    
    # Extract unique values for filters
    genre_list, director_list, actor_list = extract_unique_values(movies)
    
    # Get list of all movie titles
    movie_titles = movies['Title']
    
    # Show welcome screen
    show_intro()
    
    # Main menu loop
    while True:
        # Show main menu options
        main_result = menu(["Search Movies", "Display full movie list", "Exit"])
        main_index = main_result['index']  # Get selected option
        
        # User selected Exit
        if main_index == 2:
            print("\nThank you for using Movie Recommender! Goodbye!")
            break  # Exit program
        
        # User selected Display full movie list
        elif main_index == 1:
            display_full_movie_list(movies, movie_titles)
        
        # User selected Search Movies
        elif main_index == 0:
            search_movies(movies, movie_titles, genre_list, director_list, actor_list)
main()