function toggleFileField() {
    const selected = document.querySelector('input[name="media"]:checked').value;
    const fileField = document.getElementById("file-field");
    const youtubeField = document.getElementById("youtube-field")

    if (selected === "upload") {
        fileField.style.display = "block";
    } else {
        fileField.style.display = "none";
    }
    if (selected === "youtube") {
        youtubeField.style.display = "block";
    } else {
        youtubeField.style.display = "none";
    }
}

const radios = document.querySelectorAll('input[name="media"]');
radios.forEach(radio => {
    radio.addEventListener("change", toggleFileField);
});

window.onload = toggleFileField;