

$(document).ready(async function () {
    let isBookmarked = false;
    const article = document.getElementById('article-content');
    let post_id;
    let post_type;

    let bookmarkContainer = document.getElementById('bookmarkContainer')
    if (bookmarkContainer) {
        post_id = article.getAttribute('data-cid')
        post_type = article.getAttribute('data-type')

        let bookmarks_json;
        try {

            var metaElement = document.querySelector('meta[name="is_authenticated"]');
            var isAuthenticated = metaElement.getAttribute("content");

            if (isAuthenticated === true) {
                bookmarks_json = await getBookmarks(post_id, post_type);
                console.log("onReady()::", JSON.stringify(bookmarks_json));
                isBookmarked = bookmarks_json.userBookmarkCount > 0;
            }
            isBookmarked = false
        } catch (error) {
            console.error("An error occurred:", error);
        }

        addBookmarkButton(bookmarkContainer)
    }

    async function getBookmarks(post_id, post_type) {
        const url = '/api/1.0/bookmark?post_id=' + post_id + "&post_type=" + post_type;
        const response = await fetch(url, {
            method: 'GET', headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch bookmarks: ${response.status} ${response.statusText}`);
        }

        return response.json();
    }

    async function addBookmark() {
        const requestData = {
            post_id: article.getAttribute('data-cid'), post_type: article.getAttribute('data-type')
        };
        const response = await fetch('/api/1.0/bookmark', {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }, body: JSON.stringify(requestData)
        });

        if (response.status === 401) {
            throw new Error("To start bookmarking posts, we invite you to create an account. By signing up, you'll unlock a range of personalized features that enhance your browsing experience. Join our community today!");
        } else if (response.ok) {
            return response.json();
        } else {
            throw new Error("An error occurred! Please try again!");
        }
    }

    function updateBookmarkStatus() {
        let bookmarkButton = document.getElementById('bookmarkButton');
        const iconClass = isBookmarked ? 'fa-bookmark' : 'fa-bookmark-o';
        bookmarkButton.innerHTML = `<i class="fa ${iconClass}"></i> ${isBookmarked ? 'Bookmarked' : 'Add bookmark'}`;
        bookmarkButton.classList.toggle('bookmarked', isBookmarked);
    }

    function addBookmarkButton(bookmarkContainer) {
        const button = document.createElement("button");
        if (isBookmarked) {
            button.setAttribute("id", "bookmarkButton");
            button.setAttribute("class", "bookmarked");
            button.innerHTML = `<i class="fa fa-bookmark" aria-hidden="true"></i> Bookmarked`;
        } else {
            button.setAttribute("id", "bookmarkButton");
            button.innerHTML = `<i class="fa fa-bookmark-o" aria-hidden="true"></i> Add bookmark`;
        }

        button.addEventListener('click', toggleBookmark);
        bookmarkContainer.appendChild(button);
    }

    async function toggleBookmark() {
        try {
            let bookmarks_json = await addBookmark(post_id, post_type);
            console.log("toggleBookmark()::", JSON.stringify(bookmarks_json));
            isBookmarked = bookmarks_json.userBookmarkCount > 0;
        } catch (error) {
            showToast(error.message, "error")
            console.error("An error occurred:", error);
        }
        updateBookmarkStatus()
    }
});



