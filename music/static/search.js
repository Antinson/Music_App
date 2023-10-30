const trackCardTemplate = document.querySelector("[data-track-template]");
const albumCardContainer = document.querySelector("[album-cards-container]");
const searchInput = document.querySelector("[data-search]");
const initialRecordCount = 5;
let tracks = [];
let trackElements = [];
let filteredTracks = [];


document.addEventListener("DOMContentLoaded", function() {

    // Define the number of records to display initially

    fetch("/getCards")
        .then(response => response.json())
        .then(data => {
            let count = -1;
            tracks = data.map(track => {
                if (track === null) {
                    return null;
                }
                try {              
                    count++;
                    return {
                        title: track.title,
                        album: track.album.name,
                        artist: track.artist.full_name,
                        duration: track.track_duration,
                        genres: track.track_genres.name,
                        track_url: track.track_url,
                        track_array_index: count,
                        track_id: track.track_id
                    };
                } catch (error) {
                    return null;
                }
            })
            .filter(track => track !== null);

            tracks.forEach(track => {
                createTrackElements(track);
            });

            // Display the initial number of records
            displayTrackElements(tracks.slice(0, initialRecordCount));
        });

    searchInput.addEventListener("input", e => {

        const value = e.target.value.toLowerCase();
        albumCardContainer.innerHTML = '';

        filteredTracks = [];

        filteredTracks = tracks.filter(track => {
            return(
            track.title.toLowerCase().includes(value) ||
            track.album.toLowerCase().includes(value) ||
            track.artist.toLowerCase().includes(value)
            );
        })
        
        displayTrackElements(filteredTracks.slice(0, initialRecordCount));
    });
});


async function createTrackElements(track) {
    
    // Create the elements
    const card = trackCardTemplate.content.cloneNode(true).children[0];
    const title = card.querySelector("[data-title]");
    const album = card.querySelector("[data-album]");
    const artist = card.querySelector("[data-artist]");
    const trackUrl = card.querySelector("[data-track-url]");
    const trackDuration = card.querySelector("[data-track-duration]");
    //const genres = card.querySelector("[data-genres]");

    // Assign the elements
    title.innerText = track.title;
    album.innerText = track.album;
    artist.innerText = track.artist;
    trackUrl.innerText = track.track_url;
    trackDuration.innerText = track.duration;
    //genres.innerText = track.genres[0];

    // Event listener that goes to the individual track page
    card.addEventListener("click", () => { 
        localStorage.setItem("selectedTrackId", track.track_id);
        window.location.href = `/track/${track.track_id}`;
    });

    // Push the element to the array
    trackElements.push(card);
}


async function displayTrackElements(trackArray) {
    trackArray.forEach(track => {
        // Appends the element object to the container
        albumCardContainer.appendChild(trackElements[track.track_array_index]);
    });
}

function loadMore() {
    const currentRecordCount = albumCardContainer.childElementCount;
    const newRecordCount = currentRecordCount + initialRecordCount;
    const trackArray = filteredTracks.length ? filteredTracks : tracks;
    displayTrackElements(trackArray.slice(currentRecordCount, newRecordCount));
}