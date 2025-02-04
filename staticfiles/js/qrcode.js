document.addEventListener("DOMContentLoaded", function() {
    const videoElement = document.createElement('video');
    const scanner = new Instascan.Scanner({ video: videoElement });

    scanner.addListener('scan', function(content) {
        window.location.href = content; // Redirect to the scanned link
    });

    Instascan.Camera.getCameras().then(function(cameras) {
        if (cameras.length > 0) {
            scanner.start(cameras[0]);
        } else {
            console.error('No cameras found.');
        }
    }).catch(function(e) {
        console.error(e);
    });

    document.getElementById('preview').appendChild(videoElement);
});