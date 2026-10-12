"use strict";
// R50b / R53a: on narrow screens the orientation list starts collapsed. This runs where it is placed in the
// document, before anything below it is laid out, so nothing visible moves (CSP forbids inline scripts).
if (matchMedia("(max-width: 700px)").matches) {
 const details = document.currentScript && document.currentScript.previousElementSibling;
 if (details && details.tagName === "DETAILS") details.open = false;
}
