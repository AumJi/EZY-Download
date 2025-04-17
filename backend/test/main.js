document.getElementById('downloadBtn').addEventListener('click', async () => {
    const statusElement = document.getElementById('status');
    statusElement.textContent = "Downloading secret image...";
    
    try {
        // เรียก API ของ FastAPI
        const response = await fetch('http://localhost:8000/api/download-secret-image');
        
        if (!response.ok) {
            throw new Error('Failed to download image');
        }
        
        // แปลง response เป็น blob
        const blob = await response.blob();
        console.log(blob);

        // สร้าง URL สำหรับดาวน์โหลด
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'secret_image.jpg';
        document.body.appendChild(a);
        a.click();
        
        // // ทำความสะอาด
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        statusElement.textContent = "Image downloaded successfully!";
    } catch (error) {
        console.error('Error:', error);
        statusElement.textContent = "Error downloading image: " + error.message;
    }
});