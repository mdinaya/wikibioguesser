# WikiBio Guesser 🕵️‍♀️

A fun, minimalistic web game built with Streamlit that challenges you to guess famous personalities based solely on the section titles from their Wikipedia pages. Put your knowledge and deduction skills to the test!

## Table of Contents

- [Features](#features)
- [How to Play](#how-to-play)
- [Setup and Run Locally](#setup-and-run-locally)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Features

✅ Guess famous individuals from their Wikipedia section titles.

✅ Keep track of your score.

✅ Option to reveal the correct answer if you're stuck.

✅ "New Person" button for continuous play.

✅ Dynamic fetching of Wikipedia data using the MediaWiki API.

✅ Clean and minimalistic user interface with custom CSS.

✅ Input field has a subtle black outline on focus for better usability.

✅ Autocomplete disabled on the guess input for a fresh challenge each time.

✅ Responsive design elements for a good experience across devices (basic).

✅ Sticky footer for consistent layout.


## How to Play

1.  Read the list of section titles presented on the screen.
2.  Enter your guess for the person's name in the input box.
3.  Click "Submit" to check your answer.
4.  If you're correct, your score increases!
5.  If you're stuck, click "Reveal Person" to see the answer.
6.  Click "New Person" to get a fresh set of sections and try another guess.

## Setup and Run Locally

Follow these steps to get your own WikiBio Guesser running on your local machine.

### Prerequisites

* Python 3.8+
* `pip` 

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mdinaya/wikibioguesser.git
    cd wikibioguesser
    
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

1.  **Prepare the `names.json` file:**
    This project relies on a `names.json` file containing a list of Wikipedia article titles (e.g., famous people, places, concepts) that the game will use.
    * Create a file named `names.json` in the root directory of your project.
    * Populate it with a JSON array of strings. Each string should be an exact Wikipedia article title.
    * **Example `names.json` content:**
        ```json
        [
            "Albert Einstein",
            "Marie Curie",
            "Leonardo da Vinci",
            "Queen Elizabeth II",
            "Nelson Mandela"
        ]
        ```

2.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    Your browser should automatically open to the app (usually `http://localhost:8501`).

## Project Structure
```
├── app.py           # The main Streamlit application script
├── names.json       # (You need to create this) A list of Wikipedia titles for the game
├── data.py          # The script to get the names from the HF database
├── README.md        # This README file
└── requirements.txt # (You'll generate this) Python dependencies
```

## Future Enhancements

Here's a list of features we'd love to implement to make WikiBio Guesser even better! Contributions are highly encouraged!

- [ ] **Prevent Repetitive Guesses:** Ensure the same person isn't picked too frequently (or add a "skip" option).
- [ ] **Difficulty Levels:**
    - [ ] Option to choose fewer sections for harder guesses.
- [ ] **Timed Guesses:** Add a timer for each guess to challenge players' speed.
- [ ] **Hints System:**
    - [ ] Reveal the first letter of the person's name.
    - [ ] Provide a category hint (e.g., "Scientist", "Artist").
- [ ] **Improved Error Handling:** More user-friendly messages for API failures or missing `names.json`.
- [ ] **Enhanced Mobile Responsiveness:** Further optimize layout and touch interactions for mobile devices.
- [ ] **"How to Play" / "About" Section:** Dedicated in-app pages explaining the game and project.
- [ ] **Visual Feedback:**
    - [ ] Green border/background for correct guesses.
    - [ ] Red border/background for incorrect guesses.
- [ ] **Category/Theme Selection:** Allow users to choose specific categories of people (e.g., "Historical Figures", "Musicians").

## Contributing

I welcome contributions! If you have ideas for features, bug fixes, or improvements, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'feat: Add new feature X'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to good practices, includes appropriate tests where applicable, and follows the existing code style.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Additional Info
- This [HuggingFace dataset](https://huggingface.co/datasets/rcds/wikipedia-persons-masked) is used to get data from Wikipedia biographies.
- The styles were written with the help of Gemini (2.5).
