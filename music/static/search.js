

document.addEventListener("DOMContentLoaded", function() {
    const trackCardTemplate = document.querySelector("[data-track-template]");
    const albumCardContainer = document.querySelector("[album-cards-container]");

    let tracks = [];

    const searchInput = document.querySelector("[data-search]");

    searchInput.addEventListener("input", e => { 
        const value = e.target.value;
        tracks.forEach(track => {
            const isVisible = track.title.includes(value) || track.album.includes(value) || track.artist.includes(value);
            track.element.classList.toggle("hide", !isVisible);
        })
    });



    fetch("/getCards")
        .then(response => response.json())
        .then(data => {
        tracks = data.map(track => {
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
            albumCardContainer.appendChild(card);
            return {title: track.title, album: track.album.name, artist: track.artist.full_name, duration: track.track_duration
            ,genres: track.track_genres.name, track_url: track.track_url, element: card};
        })
    })
});




