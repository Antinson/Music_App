## Description

A modern Flask-based music discovery application featuring a comprehensive music database with user authentication, track reviews, and dynamic visual effects. The application provides an intuitive interface for browsing, searching, and reviewing music tracks with contemporary UI styling and engaging visual animations.

## Features

- **User Authentication**: Complete registration and login system with secure session management
- **Music Database**: Browse extensive collection of tracks with detailed metadata (artist, album, genre, duration, release year)
- **Search & Filter**: Advanced search functionality by track name, artist, album, or genre with pagination
- **User Reviews**: Rate and review tracks with a 5-star rating system
- **User Profiles**: View user activity including liked tracks and review history
- **Visual Enhancements**:
  - Site-wide floating musical notes animation
  - Organic gel visualizer on individual track pages
  - Modern responsive UI with hover effects and smooth transitions
- **Responsive Design**: Optimized for desktop and mobile viewing

## Installation

**Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)

**Setup Instructions**

1. Clone the repository:
   ```shell
   $ git clone <repository-url>
   $ cd Music_App
   ```

2. Create and activate virtual environment:
   ```shell
   # Windows
   $ py -3 -m venv venv
   $ venv\Scripts\activate

   # macOS/Linux
   $ python3 -m venv venv
   $ source venv/bin/activate
   ```

3. Install dependencies:
   ```shell
   $ pip install -r requirements.txt
   ```

## Execution

**Running the application**

From the project directory, within the activated virtual environment:

```shell
$ flask run
```

The application will be available at `http://localhost:5000`

## Usage

1. **Registration/Login**: Create an account or login with existing credentials
2. **Browse Music**: Navigate through the music collection using the browse page
3. **Search Tracks**: Use the search functionality to find specific tracks, artists, albums, or genres
4. **Rate & Review**: Click on individual tracks to view details and leave reviews
5. **User Profile**: Access your profile to view liked tracks and review history
6. **Visual Effects**: Hover over track details to see the organic gel visualizer animation

## Visual Enhancements

The application features modern visual enhancements for an engaging user experience:

- **Floating Musical Notes**: Site-wide animated musical notes that gently float upward across all pages
- **Organic Gel Visualizer**: Interactive fluid animation on track detail pages that activates on hover
- **Modern UI Design**: Contemporary styling with gradients, shadows, and smooth transitions
- **Responsive Tables**: Enhanced table designs with hover effects and consistent styling
- **Focus Effects**: Background blur effects that highlight active content areas

## Technical Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login with secure session management
- **Forms**: Flask-WTF for form handling and CSRF protection
- **Styling**: Custom CSS with modern design patterns and animations

## Data sources

The data files are modified excerpts downloaded from:
https://www.loc.gov/item/2018655052  or
https://github.com/mdeff/fma 

We would like to acknowledge the authors of these papers for introducing the Free Music Archive (FMA), an open and easily accessible dataset of music collections: 

Defferrard, M., Benzi, K., Vandergheynst, P., & Bresson, X. (2017). FMA: A Dataset for Music Analysis. In 18th International Society for Music Information Retrieval Conference (ISMIR).

Defferrard, M., Mohanty, S., Carroll, S., & Salathe, M. (2018). Learning to Recognize Musical Genre from Audio. In The 2018 Web Conference Companion. ACM Press.
