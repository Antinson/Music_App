const id = localStorage.getItem("selectedTrackId");
let url = `/getTrack/${id}`;
let comments = [];
let isLiked = false;

let commentSection = document.querySelector("[comment-section]");
let commentTemplate = document.querySelector("[comment-template]");
const commentBox = document.getElementById("comment-box");

const trackCardTemplate = document.querySelector("[data-track-template]");
const albumCardContainer = document.querySelector("[data-track-cards-container]");
const commentButton = document.querySelector("[data-comment-button]");

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
                const likeButton = card.querySelector("[data-like]");

                
                likeButton.addEventListener("click", () => {
                    if (isLiked) {
                        console.log("Unliked track: " + track.track_id);
                        likeButton.innerText = "Like";
                        isLiked = false;
                    } else {
                        console.log("Liked track: " + track.track_id);
                        likeButton.innerText = "Unlike";
                        isLiked = true;
                    }
                });

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


const postComment = () => {
    const comment = document.querySelector("[data-comment]").value;
    document.querySelector("[data-comment]").value = "";
    const track_id = localStorage.getItem("selectedTrackId");
    const url = "/postComment";
    const data = {comment: comment, track_id: track_id};
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        getComments();
    })
}

const getComments = () => {
    // Fetching comments from the API passing the current tracks ID
    const track_id = id;
    const url = `/getComments/${track_id}`;
    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => response.json())
    .then(data => {
        const commentSection = document.querySelector("[comment-section]");

        data.forEach(comment => {
            const commentCard = commentTemplate.content.cloneNode(true).children[0];
            const username = commentCard.querySelector("[user-name]");
            const commentText = commentCard.querySelector("[comment-content]");

            username.innerText = comment.user;
            commentText.innerText = comment.review_text;

            commentSection.insertBefore(commentCard, commentSection.firstChild);
            
            comments.push({
                username: comment.user,
                comment: comment.review_text,
                element: commentCard,
            });
        });
    })
}

getComments();
commentButton.addEventListener("click", postComment);
commentBox.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent the default Enter key behavior (e.g., line break)
        postComment(); // Call your postComment function when Enter is pressed
    }
});

commentBox.addEventListener("click", (event) => {
    event.stopPropagation(); // Prevent the click event from propagating to the document body
    commentButton.classList.remove("hide");
})

document.body.addEventListener("click", (event) => {
    if (event.target !== commentBox && !commentButton.contains(event.target)) {
        commentButton.classList.add("hide");
    }
});