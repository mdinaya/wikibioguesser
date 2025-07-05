import streamlit as st
import requests, random, json

# --- Page Configuration (Must be the very first Streamlit command) ---
st.set_page_config(layout="centered", page_title="WikiBio Guesser", page_icon="🕵️‍♀️")

# --- Custom CSS for Minimalistic Design ---
st.markdown(
    """
    <style>
    html {
        height: 100%;
    }

    /* General body styling for font and background */
    body {
        margin: 0;
        padding: 0;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        background-color: #f0f2f6; /* Light gray background */
    }

    /* Center align main title and subtitle */
    .stApp > header {
        display: none; /* Hide Streamlit's default header */
    }

    h1 {
        text-align: center;
        color: #262730; /* Darker text for main title */
        font-size: 3.5em; /* Larger font size for main title */
        margin-bottom: 0.2em;
    }

    h2 {
        text-align: center;
        color: #4f535a; /* Slightly lighter text for subtitle */
        font-size: 1.8em;
        margin-bottom: 2em; /* Space below subtitle */
    }

        /* Ensure the main app container takes full viewport height and is a flex column */
    .stApp {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    /* Hide Streamlit's default header and remove its top padding */
    header {
        display: none !important;
    }
    .stApp > div:first-child {
        padding-top: 0px !important;
    }

    /* Make the main content area grow to push the footer down */
    div[data-testid="stAppViewContainer"] {
        flex-grow: 1;
        padding-bottom: 100px; /* Space before footer */
    }

    /* Score in top-left - Keeping it fixed for immediate visibility */
    .score-container {
        position: absolute;
        top: 20px;
        left: 20px;
        font-size: 1.5em;
        font-weight: bold;
        color: #262730;
        z-index: 10;
    }

    /* Card styling for sections */
    .stMarkdown p {
        padding: 10px 15px;
        margin: 5px 0;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #333333;
    }

    /* Text input styling - get its effective height */
    .stTextInput > div > div > input {
        border-radius: 8px;
        padding: 10px 15px; /* This gives it 10px top/bottom padding */
        border: 1px solid #ced4da;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.075);
        height: 38px; /* Explicitly set height for consistency */
        box-sizing: border-box; /* Include padding and border in height */
    }
    .stTextInput > label {
        font-weight: bold;
        color: #262730;
        margin-bottom: 4px; /* Standard label margin */
    }

    // Find the specific text input by looking for the input tag within its data-testid parent
    var inputElement = document.querySelector('d[data-testid="stTextInput"] input');
    if (inputElement) {
        inputElement.setAttribute('autocomplete', 'off');
    }
    
    #* Text input focus styling */
    div[data-testid="stTextInput"] input:focus {
        border-color: #000000 !important; /* Black border on focus, with high priority */
        box-shadow: 0 0 0 0.2rem rgba(0, 0, 0, 0.25) !important; /* Black shadow for outline effect, with high priority */
        outline: 0 !important; /* Absolutely remove any default outline */
        /* Ensure no specific border-width is overriding it, if a red border persists */
        border-width: 1px !important;
    }

    /* Streamlit button general styling - ALL buttons will follow this base */
    .stButton > button {
        border-radius: 8px;
        font-weight: bold;
        height: 38px; /* Consistent height for ALL buttons, matching input */
        padding: 0 15px; /* Consistent horizontal padding for ALL buttons */
        display: flex; /* Use flexbox to center content vertically */
        align-items: center; /* Center text vertically */
        justify-content: center; /* Center text horizontally */
        transition: all 0.2s ease-in-out;
        white-space: nowrap; /* Prevent button text from wrapping */
    }

    /* Specific color overrides for buttons */

    /* Submit button (success green) */
    .stButton button[kind="primary"] { /* Targets buttons with type="primary" */
        background-color: #28a745;
        color: white;
        border: 1px solid #28a745;
    }
    .stButton button[kind="primary"]:hover {
        background-color: #218838;
        border-color: #1e7e34;
    }

    /* Reveal button (danger red) */
    .stButton button[kind="secondary"] { /* Targets buttons with type="secondary" */
        background-color: #dc3545;
        color: white;
        border: 1px solid #dc3545;
    }
    .stButton button[kind="secondary"]:hover {
        background-color: #c82333;
        border-color: #bd2130;
    }

    /* New Person button (primary blue) - targeted by its specific data-testid as it's not type="primary" or "secondary" */
    .stButton button[data-testid="stButton-new_person_button"] {
        background-color: #007bff;
        color: white;
        border: 1px solid #007bff;
    }
    .stButton button[data-testid="stButton-new_person_button"]:hover {
        background-color: #0056b3;
        border-color: #004085;
    }

    /* Alignment of the columns: Align their bottoms */
    div[data-testid="stHorizontalBlock"] {
        display: flex; /* Ensure it's a flex container */
        align-items: flex-end; /* Vertically aligns children (the columns) to their bottom */
    }

    /* THIS IS THE KEY TO LIFT THE SUBMIT BUTTON UP TO ALIGN WITH THE INPUT BOX */
    /* Target the div wrapper of the submit button specifically within its column */
    /* This negative margin compensates for the height of the label above the text input.
       You might need to fine-tune the `-25px` value slightly (e.g., -24px, -26px, -28px)
       by inspecting the page in your browser's developer tools (F12)
       and checking the `margin-bottom` of the label and `margin-top` of the input field. */
    div[data-testid="stColumn"] > div > .stButton:has(button[kind="primary"]) {
        margin-top: -25px; /* Adjust this value to perfectly align */
    }

    /* Footer styling */
    .footer {
        margin-top: auto;
        padding: 20px;
        font-size: 0.9em;
        color: #6c757d;
        text-align: center;
        width: 100%;
        flex-shrink: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Data Loading (from your original code) ---
@st.cache_data
def load_titles():
    # Ensure 'names.json' is in the same directory as your script
    try:
        with open("names.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("`names.json` not found. Please ensure it's in the same directory.")
        return []

titles = load_titles()

def get_sections(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": title,
        "prop": "sections",
        "format": "json",
    }
    try:
        res = requests.get(url, params=params)
        data = res.json()
        if 'parse' in data:
            # Filters to exclude common non-biographical sections
            skip = {"References", "External links", "Further reading", "See also", "Notes", "Bibliography", "Contents"}
            sections = [
                section['line']
                for section in data['parse']['sections']
                if section['line'] not in skip
                and section['line'].strip()
                and section.get("toclevel") == 1 # only top-level sections
            ]
            return sections if len(sections) > 2 else None # ensure enough sections
        else:
            # handle cases where 'parse' key might be missing (e.g. page not found)
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Network error fetching sections for {title}: {e}")
        return []
    except Exception as e:
        st.error(f"Error processing sections for {title}: {e}")
        return []

def pick_new_person(titles_list): # renamed to avoid shadowing global 'titles'
    if not titles_list:
        return "No person available", ["No sections loaded. Check names.json."]

    attempts = 0
    while attempts < 15: # limit attempts to prevent infinite loop
        person = random.choice(titles_list)
        sections = get_sections(person)
        if sections and len(sections) > 2: # ensure enough sections for a good hint
            return person, sections
        attempts += 1
    st.warning("Could not find a person with enough sections after several attempts.")
    return "Unknown Person", ["Could not retrieve meaningful sections."]


# initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "person" not in st.session_state:
    st.session_state.person, st.session_state.sections = pick_new_person(titles)
    # ensure person and sections are initialized even if pick_new_person fails initially
    if not st.session_state.person:
        st.session_state.person = "Failed to load person"
        st.session_state.sections = ["Please check your internet connection or 'names.json' file."]

if "revealed" not in st.session_state:
    st.session_state.revealed = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "guess_result" not in st.session_state:
    st.session_state.guess_result = None
if "input_key_counter" not in st.session_state: # for resetting text input
    st.session_state.input_key_counter = 0


# ui

# centered title and subtitle
st.markdown("<h1>wikibio guesser. challenge yourself.</h1>", unsafe_allow_html=True)
st.markdown("<h2>guess a person based on their wikipedia sections.</h2>", unsafe_allow_html=True)

# score in top-left (using custom CSS positioning)
st.markdown(f'<div class="score-container">Score: {st.session_state.score}</div>', unsafe_allow_html=True)

st.write("---") # simple separator

# sections display
# use columns to somewhat center the sections, but still keep left alignment within the column
sections_col1, sections_col2, sections_col3 = st.columns([1, 4, 1])
with sections_col2: # Content in the middle column
    for section in st.session_state.sections:
        # wrap each section in a markdown block which will be styled as a card
        st.markdown(f"<p>{section}</p>", unsafe_allow_html=True)

# input and submit buttons
st.write("---") # separator before input
guess_disabled = st.session_state.get("revealed", False)
guess_col, submit_col = st.columns([0.7, 0.3]) # adjust column width for better alignment

with guess_col:
    # key changes to force reset
    guess = st.text_input(
        "Who do you think it is?",
        key=f"guess_input_{st.session_state.input_key_counter}",
        disabled=guess_disabled,
        placeholder="Enter your guess here..."
    )
with submit_col:
    # add a small vertical space to align with text input
    st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True) # adjust height as needed
    if st.button("Submit", disabled=guess_disabled, type="primary"):
        st.session_state.submitted = True
        # set a temporary state to indicate processing guess, if needed for more complex UI

# handle the guess result display
if st.session_state.get("submitted"):
    if guess.strip().lower() == st.session_state.person.strip().lower():
        st.success("✅ Correct! You got it!")
        if st.session_state.guess_result != "correct": # prevent score increment on rerun if already correct
            st.session_state.score += 1
            st.session_state.guess_result = "correct"
            st.session_state.revealed = True # auto-reveal on correct guess
    else:
        st.warning("🤔 Not quite. That's not the person. Want to reveal the answer?")
        st.session_state.guess_result = "wrong"
    st.session_state.submitted = False # reset submitted state after handling

# reveal and new person buttons
st.markdown("<div style='margin-top: 1em;'></div>", unsafe_allow_html=True)
reveal_col, next_col = st.columns([1, 1])

with reveal_col:
    # assign a custom key for styling the reveal button as red
    if st.button("Reveal Person", key="reveal_button", type="secondary"):
        st.session_state.revealed = True
        st.session_state.submitted = False
        st.info(f"🎭 It was **{st.session_state.person}**!")

with next_col:
    # assign a custom key for styling the new person button as blue
    if st.button("New Person", key="new_person_button", type="primary"):
        st.session_state.person, st.session_state.sections = pick_new_person(titles)
        st.session_state.revealed = False
        st.session_state.submitted = False
        st.session_state.guess_result = None
        st.session_state.input_key_counter += 1 # increment to reset text input
        st.rerun()

# footer
st.markdown(
    """
    <div class="footer">
        x: @tiamaddina 2025
    </div>
    """,
    unsafe_allow_html=True
)