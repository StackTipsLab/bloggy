const copyButtonLabel = "Copy";

async function copyCode(event) {
    const button = event.target;
    const pre = button.parentElement;
    let text = pre.innerText.replace(copyButtonLabel, "").trim()
    await navigator.clipboard.writeText(text);

    button.innerText = "Copied!";
    setTimeout(() => {
        button.innerText = copyButtonLabel;
    }, 1000)

}

$(document).ready(function () {
    let preBlocks = document.getElementsByTagName("pre");

    for (let i = 0; i < preBlocks.length; i++) {
        if (navigator.clipboard) {
            new_html = "<div class='codeBox'>" + preBlocks[i].outerHTML + "<button class='btn__copyCode' type='button'>Copy</button></div>";
            preBlocks[i].outerHTML = new_html;
        }
    }


    document.querySelectorAll('pre').forEach((el) => {
        hljs.highlightElement(el);
    });

    document.addEventListener('click', function (e) {
        if (e.target && e.target.className === 'btn__copyCode') {
            copyCode(e);
        } else if (e.target && (e.target.className === 'collapsible' || e.target.className === 'collapsible active')) {
            const collapsible = e.target;
            collapsible.classList.toggle("active");

            let content = collapsible.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        }
    });

});


document.addEventListener("DOMContentLoaded", function () {

    let articleContent = document.getElementById("article-content");
    if (null === articleContent) {
        articleContent = document.getElementById("static-page");
    }

    if (null === articleContent)
        return


    var currentDomain = window.location.hostname;
    var links = articleContent.querySelectorAll('a');

    links.forEach(function (link) {
        if (link.href.startsWith('http') || link.href.startsWith('www')) {
            if (!link.href.startsWith('https://' + currentDomain)) {
                link.classList.add('external');
            }
        }
    });
});