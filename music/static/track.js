let id = 5;
let url = `/getTrack/${id}`;

const trackCardTemplate = document.querySelector("[data-track-template]");
const albumCardContainer = document.querySelector("[data-track-cards-container]");



fetch(url, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
    },
})
.then(response => response.json())
.then(track => {
    const card = trackCardTemplate.content.cloneNode(true).children[0];
                const title = card.querySelector("[data-title]");
                const album = card.querySelector("[data-album]");
                const artist = card.querySelector("[data-artist]");
                const trackUrl = card.querySelector("[data-track-url]");
                const trackDuration = card.querySelector("[data-track-duration]");
                const genres = card.querySelector("[data-genres]");
    
                try {
                    title.innerText = track.title;
                    album.innerText = track.album.name;
                    artist.innerText = track.artist.full_name;
                    trackDuration.innerText = track.track_duration;
                    genres.innerText = track.track_genres[0].name;
                } catch (error) {
                    console.error("Error processing track data:", error);
                    // Set the fields to a blank or default value
                    title.innerText = "N/A";
                    album.innerText = "N/A";
                    artist.innerText = "N/A";
                    trackUrl.innerText = "N/A";
                    trackDuration.innerText = "N/A";
                    genres.innerText = "N/A";
                }
                albumCardContainer.appendChild(card);
})