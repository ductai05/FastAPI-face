const API_URL = 'http://localhost:8000';

// Tab switching
document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        button.classList.add('active');
        document.getElementById(button.dataset.tab).classList.add('active');
    });
});

// Login form
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {
        username: formData.get('username'),
        password: formData.get('password')
    };

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        
        if (result.login === 'success') {
            alert('Đăng nhập thành công!');
        } else {
            alert('Đăng nhập thất bại!');
        }
    } catch (error) {
        alert('Có lỗi xảy ra!');
    }
});

// Register form
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {
        username: formData.get('username'),
        password: formData.get('password')
    };

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        
        if (result.register === 'success') {
            alert('Đăng ký thành công!');
            e.target.reset();
        } else {
            alert('Đăng ký thất bại - tên người dùng đã tồn tại!');
        }
    } catch (error) {
        alert('Có lỗi xảy ra!');
    }
});

// Face registration form
document.getElementById('faceForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const file = formData.get('face');  // Lấy file từ input có name="face"

    // Tạo FormData mới và thêm file vào với key là 'file'
    const sendData = new FormData();
    sendData.append('file', file);  // Key phải là 'file' để khớp với FastAPI

    try {
        const response = await fetch(`${API_URL}/save_encoding?username=${formData.get('username')}&password=${formData.get('password')}`, {
            method: 'POST',
            body: sendData  // Gửi FormData mới
        });
        const result = await response.json();
        
        if (response.ok) {
            alert('Lưu khuôn mặt thành công!');
            e.target.reset();
        } else {
            alert(result.detail || 'Lưu khuôn mặt thất bại!');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Có lỗi xảy ra!');
    }
});

// Face verification
async function verifyFace() {
    const username = document.getElementById('faceLoginUsername').value;
    const fileInput = document.getElementById('faceLoginInput');
    
    if (!username || !fileInput.files[0]) {
        alert('Vui lòng nhập tên đăng nhập và chọn ảnh!');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch(`${API_URL}/verify_existing_face?username=${username}`, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        if (result.match) {
            alert(`Xác thực thành công! Độ tin cậy: ${(result.confidence * 100).toFixed(2)}%`);
        } else {
            alert(`Xác thực thất bại! Độ tin cậy: ${(result.confidence * 100).toFixed(2)}%`);
        }
    } catch (error) {
        alert('Có lỗi xảy ra!');
    }
} 