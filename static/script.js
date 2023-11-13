const takePicture = async (videoElement) => {
    const audio = new Audio('/static/Barcode-scanner-beep-sound.mp3');
    audio.play();
    showLoader();

    const capturedImageCanvas = document.getElementById('captured-image');
    const context = capturedImageCanvas.getContext('2d');
    capturedImageCanvas.width = videoElement.videoWidth;
    capturedImageCanvas.height = videoElement.videoHeight;

    context.drawImage(
        videoElement,
        0,
        0,
        videoElement.videoWidth,
        videoElement.videoHeight
    );

    const imageData = capturedImageCanvas.toDataURL('image/jpeg');
    const blob = dataURItoBlob(imageData);

    hideScanArea(imageData);

    const extractedInfo = await extractInfoFromImage(blob);

    displayInformation(extractedInfo);

    hideLoader();
};

async function extractInfoFromImage(imageData) {
    const formData = new FormData();
    formData.append('file', imageData);

    const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
    });
    const { credit_card, output_file } = await res.json();

    return { credit_card, output_file };
}

function displayInformation({ credit_card, output_file }) {
    const resultDiv = document.getElementById('result');
    document.getElementById('cardNumber').value = credit_card.number;
    document.getElementById('name').value = credit_card.holder_name;
    document.getElementById('cvv').value = credit_card.cvv;
    document.getElementById('expirationDate').value = credit_card.expiry_date;

    resultDiv.style.display = 'block';
    const resultDataDiv = document.getElementById('result-data');

    const src = output_file;
    const img = document.createElement('img');
    img.src = src;
    img.width = 300;
    img.height = 300;

    const restartBtn = document.createElement('button')
    restartBtn.className = 'restart-btn';
    restartBtn.innerHTML = 'Restart';
    resultDiv.appendChild(restartBtn);

    restartBtn.addEventListener('click', () => {
        showScanArea();
        resultDiv.innerHTML = '';
        resultDiv.style.display = 'none';
    });

    resultDataDiv.appendChild(img);
    const capturedImage = document.getElementById('captured-image');
    capturedImage.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    const videoElement = document.getElementById('camera-preview');
    const captureButton = document.getElementById('capture-btn');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            videoElement.srcObject = stream;
        })
        .catch((error) => {
            console.error('Error accessing camera:', error);
        });

    captureButton.addEventListener('click', () => takePicture(videoElement));

    const starBtn = document.getElementById('start-btn');

    starBtn.addEventListener('click', () => {
        const timerContainer = document.getElementById('timer');
        timerContainer.style.display = 'block';
        let count = 10;

        const timer = setInterval(() => {
            timerContainer.innerHTML = count;
            count -= 1;
            if (count === -1) {
                clearInterval(timer);
                timerContainer.style.display = 'none';
                takePicture(videoElement);
            }
        }, 1000);
    });

    document.addEventListener('keydown', (event) => {
        takePicture(videoElement);
    });
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

function hideScanArea(imageData) {
    const scanArea = document.getElementById('scan-area');
    scanArea.style.display = 'none';

    const capturedImage = document.getElementById('captured-image');
    capturedImage.src = imageData;
    capturedImage.style.display = 'block';
}

function showScanArea() {
    const scanArea = document.getElementById('scan-area');
    scanArea.style.display = 'block';
}

function showLoader() {
    const loader = document.getElementById('loader');
    loader.style.display = 'block';
}

function hideLoader() {
    const loader = document.getElementById('loader');
    loader.style.display = 'none';
}
