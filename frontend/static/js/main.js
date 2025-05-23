const notyf = new Notyf({duration: 1500,
    position: {x: 'right',y: 'top'},
    ripple: true,
});

const downloadForm = document.querySelector('#download-form');
const title = document.querySelector('#image-name');
const type = document.querySelector('#file-extension');
const amount = document.querySelector('#download-count');
const btnSubmit = document.querySelector('#btn-submit');

downloadForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    // ปุ่ม disabled ขณะกำลังประมวลผล
    btnSubmit.disabled = true;
    btnSubmit.innerHTML = `
        <span class="loading loading-spinner loading-sm"></span>
        กำลังประมวลผล...
    `;

    const data = {
        title: title.value,
        type: type.value,
        amount: amount.value
    };

    if (data.title.replace(" ", "").split(",").length * data.amount <= 100
  ) {
    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // ตรวจสอบ HTTP Status
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || `ดาวน์โหลดล้มเหลว (Status: ${response.status})`);
        }

        // ตรวจสอบ Content-Type
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/zip')) {
            throw new Error("รูปแบบไฟล์ไม่ถูกต้อง");
        }

        const blob = await response.blob();
        
        // ตรวจสอบขนาดไฟล์
        if (blob.size === 0) {
            throw new Error("ไฟล์ที่ดาวน์โหลดมาว่างเปล่า");
        }

        // สร้าง URL สำหรับดาวน์โหลด
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `${data.title || 'download'}.zip`;
        document.body.appendChild(a);
        a.click();

        // ทำความสะอาด
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        // แสดงสถานะสำเร็จ
        notyf.success({message: 'ดาวน์โหลดเสร็จสิ้น',
            position: {x: 'left',y:'bottom'},
            duration: 5000
        });
    }
    catch (error) {
        // notyf.error({message: error || "เกิดข้อผิดพลาดในการดาวน์โหลด"}
        console.log(error);
    }
    finally {
        // คืนสถานะปุ่มเป็นปกติ
        btnSubmit.disabled = false;
        btnSubmit.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            ดาวน์โหลดเลย
        `;
    return false;
    }
}
    else {
        notyf.error({
            message: "จำนวนรูปห้ามต้องไม่เกิน 100 รูป",
    });
        btnSubmit.disabled = false;
        btnSubmit.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            ดาวน์โหลดเลย
        `;
    };
});