        // 初期化関数
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

        // ラジオボタン変更時に呼び出し
        const radios = document.querySelectorAll('input[name="media"]');
        radios.forEach(radio => {
            radio.addEventListener("change", toggleFileField);
        });

        // 初期表示時にも状態を反映
        window.onload = toggleFileField;