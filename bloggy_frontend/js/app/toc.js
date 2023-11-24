function htmlTableOfContents() {
    let tocContainer = document.getElementById("toc-content");
    let articleContent = document.getElementById("article-content");
    if (null === articleContent) {
        articleContent = document.getElementById("static-page");
    }

    if (null === articleContent)
        return

    let headings = [].slice.call(articleContent.querySelectorAll('h2, h3, h4,h5'));
    if (headings.length >= 3) {
        document.getElementById("toc").setAttribute("style", "display:block !important")
        let tableOfContentList = document.createElement('div',);
        tableOfContentList.setAttribute('class', "toc-list");
        headings.forEach(function (heading, index) {
            const slugifyHeader = heading.textContent
                .toLowerCase()
                .trim()
                .replace(/[^\w\s-]/g, '')
                .replace(/[\s_-]+/g, '-')
                .replace(/^-+|-+$/g, '');

            let link = document.createElement('a');
            link.setAttribute('href', '#' + slugifyHeader);
            link.setAttribute('class', 'd-block toc-content-link mb-2 ' + heading.localName);

            let headingCounter = heading.localName.substring(1)
            link.setAttribute('style', 'padding-left:' + (8 * (headingCounter - 2)) + "px;");

            link.textContent = heading.textContent //.replace(/[0-9].\s/g, '');
            tableOfContentList.appendChild(link);
        });
        tocContainer.appendChild(tableOfContentList);
    } else {
        tocContainer.remove();
    }
}

function registerCollapsibleEvents() {
    let coll = document.getElementsByClassName("collapsible");
    for (let i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function () {
            this.classList.toggle("active");
            let content = this.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    }
}

$(document).ready(function () {
    if (document.getElementById("toc")) {
        htmlTableOfContents();
        // registerCollapsibleEvents();
    }
});