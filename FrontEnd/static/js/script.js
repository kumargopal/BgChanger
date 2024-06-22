document.getElementById('inpainting-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    const response = await fetch('/process', {
        method: 'POST',
        body: formData,
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'result_images.zip';
        document.getElementById('download-link').innerHTML = "Download result: ";
        document.getElementById('download-link').appendChild(a);
        a.innerText = 'Download result_images.zip';
        a.click();
        window.URL.revokeObjectURL(url);
    } else {
        alert('Error generating images');
    }
});
