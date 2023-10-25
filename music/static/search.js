document.addEventListener("DOMContentLoaded", function () {
    const search = document.getElementById("search-box");
    search.addEventListener("input", searchTracks);
    const category = document.getElementById("inputGroupSelect01");
    category.addEventListener("input", searchTracks);

    // Keep a copy of all available results for re-display
    let allResultsData = [];

    // Fetch and display all available results when the page loads
    fetch('http://127.0.0.1:5000/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: '', category: '' }) // Empty data to get all results
    })
    .then(response => response.json())
    .then(data => {
        allResultsData = data; // Store all available results
        createLoad(data);
    });

    function searchTracks() {
        const text = document.getElementById("search-box").value;
        const category = document.getElementById("inputGroupSelect01").value;
        const filteredData = filterResults(text, category);
        createLoad(filteredData);
    }

    function filterResults(text, category) {
        // Use allResultsData to filter results based on user input
        return allResultsData.filter(element => {
            return element.title.toLowerCase().includes(text.toLowerCase()) &&
                   (category === '' || element.category === category);
        });
    }

    function createLoad(data) {
        const mainDiv = document.getElementById("display_area_search");
        mainDiv.innerHTML = ''; // Clear the existing results
    
        if (Array.isArray(data)) {
            data.forEach(element => {
                const container = document.createElement("div");
                container.setAttribute("class", "result-container");
                const title = document.createElement("h3");
                title.innerHTML = element.title;
                container.appendChild(title);
                mainDiv.appendChild(container);
            });
        }
    }
});    
