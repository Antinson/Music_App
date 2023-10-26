let page = 1;
let totalTracks = 0;
let debug = true;



document.addEventListener("DOMContentLoaded", function() {
    const trackCardTemplate = document.querySelector("[data-track-template]");
    const albumCardContainer = document.querySelector("[data-track-cards-container]");
    const pageNumberTotal = document.querySelector("[page-number-total]");

    const nextButton = document.querySelector("[data-next-button]");
    const previousButton = document.querySelector("[data-previous-button]");

    nextButton.addEventListener("click", () => {
        page++;
        previousButton.classList.remove("hide-keep-area");
        fetchTracks();
    });

    previousButton.addEventListener("click", () => {
        page--;
        nextButton.classList.remove("hide-keep-area");
        fetchTracks();
    });

    fetch("/totalTracks")
    .then(response => response.text())
    .then(data => {
        totalTracks = parseInt(data);
        fetchTracks();
    })


    function fetchTracks() {
        albumCardContainer.innerHTML = '';

        let tracks = [];
        let limit = 20;
        console.log("Total pages is: " + totalTracks / limit);
        pageNumberTotal.innerText = page + "/" + Math.ceil(totalTracks / limit);
        let category = "track";
        if(page < 1) {
            page = 1;
        }
        if (page == 1) {
            previousButton.classList.toggle("hide-keep-area");
        }

        if ((page) * limit >= totalTracks) {
            nextButton.classList.toggle("hide-keep-area");
        }
        const url = `/browseRequest?page=${page}&limit=${limit}&category=${category}`;
    
        fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(totalTracks);
            console.log("run");
            tracks = data.map(track => {                
                const card = trackCardTemplate.content.cloneNode(true).children[0];
                const title = card.querySelector("[data-title]");
                const album = card.querySelector("[data-album]");
                const artist = card.querySelector("[data-artist]");
                const trackUrl = card.querySelector("[data-track-url]");
                const trackDuration = card.querySelector("[data-track-duration]");
                const genres = card.querySelector("[data-genres]");

                if (debug == true) {
                    console.log(track);
                    debug = false;
                }
    
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
                card.addEventListener("click", () => { 
                    localStorage.setItem("selectedTrackId", track.track_id);
                    window.location.href = `/track/${track.track_id}`;
                });

                card.classList.add('hidden');
                albumCardContainer.appendChild(card);
                return {title: track.title, album: track.album.name, artist: track.artist.full_name, duration: track.track_duration
                ,genres: track.track_genres.name, track_url: track.track_url, element: card};
            })

            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('show');
                    } else {
                        entry.target.classList.remove('show');
                    }
                });
            });
            
            const hiddenElements = document.querySelectorAll('.hidden');
            hiddenElements.forEach((el) => observer.observe(el));
        })
    }
});




