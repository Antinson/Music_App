document.addEventListener("DOMContentLoaded", function() {
    const trackCardTemplate = document.querySelector("[data-track-template]");
    const albumCardContainer = document.querySelector("[album-cards-container]");

    let tracks = [];

    const searchInput = document.querySelector("[data-search]");

    // Define the number of records to display initially
    const initialRecordCount = 10;

    fetch("/getCards")
        .then(response => response.json())
        .then(data => {
            tracks = data.map(track => {
                if (track === null) {
                    return null;
                }
                try {
                    const card = trackCardTemplate.content.cloneNode(true).children[0];
                    const title = card.querySelector("[data-title]");
                    const album = card.querySelector("[data-album]");
                    const artist = card.querySelector("[data-artist]");
                    const trackUrl = card.querySelector("[data-track-url]");
                    const trackDuration = card.querySelector("[data-track-duration]");
                    const genres = card.querySelector("[data-genres]");
                    title.innerText = track.title;
                    album.innerText = track.album.name;
                    artist.innerText = track.artist.full_name;
                    trackUrl.innerText = track.track_url;
                    trackDuration.innerText = track.track_duration;
                    genres.innerText = track.track_genres[0].name;

                    card.addEventListener("click", () => { 
                        localStorage.setItem("selectedTrackId", track.track_id);
                        window.location.href = `/track/${track.track_id}`;
                    });

                    albumCardContainer.appendChild(card);
                    return {
                        title: track.title,
                        album: track.album.name,
                        artist: track.artist.full_name,
                        duration: track.track_duration,
                        genres: track.track_genres.name,
                        track_url: track.track_url,
                        element: card,
                    };
                } catch (error) {
                    return null;
                }
            })
            .filter(track => track !== null);

            // Hide records beyond the initial limit
            tracks.slice(initialRecordCount).forEach(track => {
                track.element.classList.add("hide");
            });
        });

    searchInput.addEventListener("input", e => {
        const value = e.target.value.toLowerCase();
        tracks.forEach(track => {
            const isVisible =
                value === "" || // Display all records if the search input is empty
                track.title.toLowerCase().includes(value) ||
                track.album.toLowerCase().includes(value) ||
                track.artist.toLowerCase().includes(value);
            track.element.classList.toggle("hide", !isVisible);
        });
    });
});
