// Navigation functionality
function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Remove active class from all nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Show selected page
    document.getElementById(pageId).classList.add('active');
    
    // Add active class to clicked nav item
    event.target.closest('.nav-item').classList.add('active');
    
    // Load content for specific pages
    if (pageId === 'history') {
        loadHistory();
    } else if (pageId === 'analytics') {
        loadAnalytics();
    }
}

// SMS submission
async function submitSMS() {
    const smsContent = document.getElementById('smsContent').value;
    const description = document.getElementById('description').value;
    
    if (!smsContent.trim()) {
        alert('لطفاً محتوای پیامک را وارد کنید');
        return;
    }
    
    try {
        // Replace with your actual API endpoint
        const response = await fetch('/api/sms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                smsContent: smsContent,
                description: description,
                timestamp: new Date().toISOString()
            })
        });
        
        if (response.ok) {
            showSuccessMessage();
            document.getElementById('smsContent').value = '';
            document.getElementById('description').value = '';
        } else {
            alert('خطا در ارسال اطلاعات');
        }
    } catch (error) {
        console.error('Error:', error);
        // For demo purposes, show success message
        showSuccessMessage();
        document.getElementById('smsContent').value = '';
        document.getElementById('description').value = '';
    }
}

// Photo upload handling
function handlePhotoUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('previewImage');
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

// Photo submission
async function submitPhoto() {
    const photoInput = document.getElementById('photoInput');
    const file = photoInput.files[0];
    
    if (!file) {
        alert('لطفاً ابتدا عکسی انتخاب کنید');
        return;
    }
    
    const formData = new FormData();
    formData.append('photo', file);
    formData.append('timestamp', new Date().toISOString());
    
    try {
        // Replace with your actual API endpoint
        const response = await fetch('/api/photo', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showSuccessMessage();
            photoInput.value = '';
            document.getElementById('previewImage').style.display = 'none';
        } else {
            alert('خطا در آپلود عکس');
        }
    } catch (error) {
        console.error('Error:', error);
        // For demo purposes, show success message
        showSuccessMessage();
        photoInput.value = '';
        document.getElementById('previewImage').style.display = 'none';
    }
}

// Show success message
function showSuccessMessage() {
    const successMessage = document.getElementById('successMessage');
    successMessage.style.display = 'block';
    setTimeout(() => {
        successMessage.style.display = 'none';
    }, 3000);
}

// Load transaction history
async function loadHistory() {
    const historyContent = document.getElementById('historyContent');
    
    try {
        // Replace with your actual API endpoint
        const response = await fetch('/api/history');
        
        if (response.ok) {
            const transactions = await response.json();
            displayHistory(transactions);
        } else {
            throw new Error('Failed to load history');
        }
    } catch (error) {
        console.error('Error loading history:', error);
        // For demo purposes, show sample data
        displayHistory([
            {
                id: 1,
                smsContent: 'واریز 500000 ریال به حساب شما',
                description: 'حقوق',
                date: '2024-01-15'
            },
            {
                id: 2,
                smsContent: 'برداشت 150000 ریال از حساب شما',
                description: 'خرید مواد غذایی',
                date: '2024-01-14'
            },
            {
                id: 3,
                smsContent: 'برداشت 300000 ریال از حساب شما',
                description: 'اجاره خانه',
                date: '2024-01-13'
            }
        ]);
    }
}

// Display history
function displayHistory(transactions) {
    const historyContent = document.getElementById('historyContent');

    if (transactions.length === 0) {
        historyContent.innerHTML = '<p style="text-align: center; color: #666;">هیچ تراکنشی یافت نشد</p>';
        return;
    }

    historyContent.innerHTML = transactions.map(transaction => {
        let typeLabel = '';
        let typeColor = '';

        if (transaction.type === -1) {
            typeLabel = 'برداشت';
            typeColor = '#d9534f'; // قرمز
        } else if (transaction.type === 1) {
            typeLabel = 'واریز';
            typeColor = '#5cb85c'; // سبز
        }

        return `
            <div class="history-item" style="position: relative; border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 8px;">
                ${typeLabel ? `<div style="position: absolute; top: 10px; left: 10px; background: ${typeColor}; color: white; padding: 2px 8px; font-size: 12px; border-radius: 4px;">
                    ${typeLabel}
                </div>` : ''}
                <h3 style="margin-top: 10px;">${transaction.description || 'بدون توضیح'}</h3>
                <p>${transaction.smsContent}</p>
                <div class="date" style="color: #888; font-size: 13px;">${transaction.date}</div>
            </div>
        `;
    }).join('');
}


// Load analytics
async function loadAnalytics() {
    const analyticsContent = document.getElementById('analyticsContent');
    
    try {
        // Replace with your actual API endpoint
        const response = await fetch('/api/analytics');
        
        if (response.ok) {
            const analytics = await response.json();
            displayAnalytics(analytics);
        } else {
            throw new Error('Failed to load analytics');
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
        // For demo purposes, show sample data
        displayAnalytics({
            monthlySpending: 2500000,
            suggestions: [
                {
                    title: 'کاهش هزینه خرید',
                    message: 'هزینه خرید شما این ماه 20% افزایش یافته. سعی کنید از لیست خرید استفاده کنید.'
                },
                {
                    title: 'پس انداز',
                    message: 'با توجه به الگوی خرج شما، می توانید ماهانه 200000 ریال پس انداز کنید.'
                }
            ]
        });
    }
}

// Display analytics
function displayAnalytics(analytics) {
    const analyticsContent = document.getElementById('analyticsContent');
    
    analyticsContent.innerHTML = `
        <div class="analytics-card">
            <h3>هزینه این ماه</h3>
            <div class="amount">${analytics.monthlySpending.toLocaleString()} ریال</div>
            <p>مجموع تراکنش های این ماه</p>
            <div style="display: flex;
                    justify-content: space-evenly;
                    margin-top: 15px;
                    background-color: white;
                    border-radius: 10px;
                    padding: 10px;">
                <div style="text-align: center;">
                    <div style="font-size: 10px; color: #28a745;">30,467,423+</div>
                    <div style="font-size: 10px; color: #373737;">درآمد</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 10px; color: #dc3545;">2,450,000-</div>
                    <div style="font-size: 10px; color: #373737;">هزینه</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 10px; color: #17a2b8;">2,550,000+</div>
                    <div style="font-size: 10px; color: #373737;">باقی‌مانده</div>
                </div>
                </div>
            </div>
        <div class="card">
            <h3 style="margin-bottom: 20px;">پیشنهادات هوشمند</h3>
            ${analytics.suggestions.map(suggestion => `
                <div class="suggestion-card">
                    <h4>${suggestion.title}</h4>
                    <p>${suggestion.message}</p>
                </div>
            `).join('')}
        </div>
    `;
}