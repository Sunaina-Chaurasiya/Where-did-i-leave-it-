const startBtn = document.getElementById("start-detection");
const stopBtn = document.getElementById("stop-detection");
const cameraFeed = document.getElementById("camera-feed");
const findBtn = document.getElementById("find-item");
const voiceResult = document.getElementById("voice-result");

// Start detection
startBtn.addEventListener("click", () => {
    fetch("/start-detection")
        .then(res => res.json())
        .then(() => {
            startBtn.style.display = "none";
            stopBtn.style.display = "inline";
            cameraFeed.src = "/video_feed";
        });
});

// Stop detection
stopBtn.addEventListener("click", () => {
    fetch("/stop-detection")
        .then(res => res.json())
        .then(() => {
            stopBtn.style.display = "none";
            startBtn.style.display = "inline";
            cameraFeed.src = ""; // Stop feed
        });
});

// Voice query
findBtn.addEventListener("click", () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = function(event) {
        const query = event.results[0][0].transcript;
        fetch("/voice-query", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        })
        .then(res => res.json())
        .then(data => {
            voiceResult.textContent = `Response: ${data.message}`;  // ⬅️ Display first
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(data.message);
            synth.speak(utter);  // ⬅️ Then speak
        });
    };

    recognition.onerror = function(event) {
        voiceResult.textContent = `Voice recognition error: ${event.error}`;
    };
});
