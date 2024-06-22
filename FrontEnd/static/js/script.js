document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('inpainting-form').addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(this);

        const response = await fetch('/process', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const resultImages = await response.json();
            const resultContainer = document.getElementById('result-container');
            resultContainer.innerHTML = '';

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
});
