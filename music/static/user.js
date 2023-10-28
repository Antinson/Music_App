const user_name = window.user_name.toUpperCase();

const userProfileArea = document.querySelector("[user-profile-area]");
const userNameArea = document.querySelector("[user-name-area]");
const likedTracksArea = document.querySelector("[liked-tracks-area]");

let commentSection = document.querySelector("[comment-section]");
let commentTemplate = document.querySelector("[comment-template]");

let comments = [];

userNameArea.innerText = user_name;
userProfileArea.appendChild(userNameArea);


const getLikedTracks = () => {
    let url = `/getUserLikedTracks/${user_name}`;
    fetch(url, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
    })
    .then(response => response.json())
    .then(data => {
        userProfileArea.appendChild(likedTracksArea);
        console.log(data);
    })
};

getLikedTracks();

const getReviews = () => {
    let url = `/getReviews/${user_name}`;
    fetch(url, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'}
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

        const trackId = comment.track_id;

        commentCard.classList.add("user-area-comment");
        commentCard.addEventListener("click", () => {
            window.location.href = `/track/${trackId}`;
        });

        commentSection.insertBefore(commentCard, commentSection.firstChild);
        
        comments.push({
            username: comment.user,
            comment: comment.review_text,
            element: commentCard,
            });
        });
    });
};

getLikedTracks();
getReviews();

