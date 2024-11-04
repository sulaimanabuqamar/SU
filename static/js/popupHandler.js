function openPopup(id) {
    document.getElementById(id).hidden = false;
    document.getElementById(id).style.animation = "openPopupBG 0.2s linear forwards";
    document.getElementById(id).children[0].style.animation = "openPopup 0.3s ease-out forwards";
}
function closePopup(id) {
    document.getElementById(id).style.animation = "closePopupBG 0.2s linear forwards";
    document.getElementById(id).children[0].style.animation = "closePopup 0.3s ease-out forwards";
    setTimeout(function() {
        document.getElementById(id).hidden = true;
    }, 300);
}
