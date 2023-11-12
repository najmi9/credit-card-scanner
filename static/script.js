document.addEventListener('DOMContentLoaded', () => {
    const videoElement = document.getElementById('camera-preview');
    const captureButton = document.getElementById('capture-btn');
    const capturedImageCanvas = document.getElementById('captured-image');
    const resultDiv = document.getElementById('result');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            videoElement.srcObject = stream;
        })
        .catch((error) => {
            console.error('Error accessing camera:', error);
        });

    captureButton.addEventListener('click', async () => {
        const context = capturedImageCanvas.getContext('2d');
        capturedImageCanvas.width = videoElement.videoWidth;
        capturedImageCanvas.height = videoElement.videoHeight;
        context.drawImage(videoElement, 0, 0, videoElement.videoWidth, videoElement.videoHeight);

        const extractedInfo = await extractInfoFromImage(capturedImageCanvas.toDataURL('image/jpeg'));

        displayInformation(extractedInfo);
    });

    async function extractInfoFromImage(imageData) {
        const blob = dataURItoBlob(imageData);
        const formData = new FormData();
        formData.append('file', blob);

        const res = await fetch('http://localhost:7000/api/upload', {
            method: 'POST',
            body: formData,
        });
        const { image_content } = await res.json();

        return { image_content };
    }

    function displayInformation(info) {
        console.log(info);
        resultDiv.innerHTML = `
           <p>
            ${info.image_content}
           </p>
        `;
    }
});


function dataURItoBlob(dataURI) {
    const splitDataURI = dataURI.split(',');
    const contentType = splitDataURI[0].match(/:(.*?);/)[1];
    const byteString = atob(splitDataURI[1]);
    const buffer = new ArrayBuffer(byteString.length);
    const uint8Array = new Uint8Array(buffer);
    for (let i = 0; i < byteString.length; i++) {
        uint8Array[i] = byteString.charCodeAt(i);
    }

    return new Blob([buffer], { type: contentType, name: 'image.jpeg' });
}
