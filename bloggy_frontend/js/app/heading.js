$(document).ready(function () {
    let answerContent = document.getElementById("article-content")
    if (answerContent) {
        let headings = answerContent.querySelectorAll('h1, h2, h3, h4');

        for (let i = 0; i < headings.length; i++) {
            let headingText = headings[i].textContent;
            const slugifyHeader = headingText
                .toLowerCase()
                .trim()
                .replace(/[^\w\s-]/g, '')
                .replace(/[\s_-]+/g, '-')
                .replace(/^-+|-+$/g, '');

            var a = document.createElement("a");
            a.href = '#' + slugifyHeader
            a.className = "hash-anchor"
            a.type = "button"
            a.setAttribute("aria-hidden", true)

            headings[i].id = slugifyHeader;
            insertAfter(headings[i].firstChild, a);
        }
    }

});

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}