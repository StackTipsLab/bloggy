/*jslint
    white: true,
    browser: true,
    vars: true

    https://github.com/matthewkastor/html-table-of-contents/blob/master/src/html-table-of-contents.js
*/

/**
 * Generates a table of contents for your document based on the headings
 *  present. Anchors are injected into the document and the
 *  entries in the table of contents are linked to them. The table of
 *  contents will be generated inside the first element with the id `toc`.
 * @param {HTMLDOMDocument} documentRef Optional A reference to the document
 *  object. Defaults to `document`.
 * @author Matthew Christopher Kastor-Inare III
 * @version 20130726
 * @example
 * // call this after the page has loaded
 * htmlTableOfContents();
 */






function htmlTableOfContents () {
    const toc = document.getElementById('toc');
    const headings = [].slice.call(document.getElementById('article-content')
        .querySelectorAll('h1, h2, h3, h4')
    );
    headings.forEach(function (heading, index) {
        const anchor = document.createElement('a');
        anchor.setAttribute('name', 'toc' + index);
        anchor.setAttribute('id', 'toc' + index);

        const link = document.createElement('a');
        link.setAttribute('href', '#toc' + index);
        link.textContent = heading.textContent;

        const div = document.createElement('div');
        div.setAttribute('class', heading.tagName.toLowerCase());

        div.appendChild(link);
        toc.appendChild(div);
        heading.parentNode.insertBefore(anchor, heading);
    });
}
