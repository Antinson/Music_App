document.addEventListener("DOMContentLoaded", function () {

    const search = document.getElementById("search_text_area");
    search.addEventListener("input", searchTracks);

    function searchTracks() {
        const text = document.getElementById("search_text_area").value;
        const data = { text: text };

        fetch('http://127.0.0.1:5000/searchjs',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
    }
});