
var observer = new MutationObserver(function(mutationsList, observer) {
    var xpath = "/html/body/div/div/main/div[2]/section[1]/div[4]/div";
    var container = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

    if (container) {
        observer.disconnect();
        var existingImg = container.querySelector("img");
        if (existingImg) {
            container.removeChild(existingImg);
        }
        var imgElement = document.createElement("img");
        imgElement.src = "https://img.028029.xyz/1734498853435.png";
        imgElement.style.position = "absolute";
        imgElement.style.right = "8px";
        imgElement.style.top = "-80px";
        imgElement.style.zIndex = "10";
        imgElement.style.width = "90px";
        container.appendChild(imgElement);
    }
});
var config = { childList: true, subtree: true };
observer.observe(document.body, config);
