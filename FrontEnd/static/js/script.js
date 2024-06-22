document.addEventListener('DOMContentLoaded', function() {
    const inpaintingForm = document.getElementById('inpainting-form');
    const uploadedImage = document.getElementById('uploaded-image');
    const imageContainer = document.getElementById('image-container');
    const generateButton = document.getElementById('generate-button');
    const loadingSpinner = document.getElementById('loading-spinner');
    const resultContainer = document.getElementById('result-container');

    imageContainer.style.display = 'block';
    uploadedImage.src = "https://ibb.co/X2Qv6xd"
    
    // Display default images
    const defaultImages = [
        "https://ibb.co/LZQnWjF",
        "https://ibb.co/LnjDV7p",
        "https://ibb.co/fpXDDVz",
        "https://ibb.co/Zg4Cmmh"
    ];

    

    defaultImages.forEach(imgBase64 => {
        const imgElement = document.createElement('img');
        imgElement.src = imgBase64;
        imgElement.style.width = '300px';  // Adjust size as needed
        imgElement.style.margin = '10px';
        resultContainer.appendChild(imgElement);
    });

    inpaintingForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(this);

        loadingSpinner.style.display = 'block';
        generateButton.disabled = true;

        const response = await fetch('/process', {
            method: 'POST',
            body: formData,
        });

        loadingSpinner.style.display = 'none';
        generateButton.disabled = false;

        if (response.ok) {
            const resultImages = await response.json();
            resultContainer.innerHTML = '';  // Clear previous result images

            resultImages.forEach(imgBase64 => {
                const imgElement = document.createElement('img');
                imgElement.src = imgBase64;
                imgElement.style.width = '300px';  // Adjust size as needed
                imgElement.style.margin = '10px';
                resultContainer.appendChild(imgElement);
            });
        } else {
            alert('Error generating images');
        }
    });

    // Display uploaded image
    document.getElementById('file-upload').addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                uploadedImage.src = e.target.result;
                imageContainer.style.display = 'block';
                resultContainer.innerHTML = '';  // Clear previous result images
            };
            reader.readAsDataURL(file);
        }
    });
});
