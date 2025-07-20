// Navigation functionality
function showPage(pageId, event = null) {
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
    if (event) {
        event.target.closest('.nav-item').classList.add('active');
    }

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
        showSuccessMessage(); // Fallback for demo
        document.getElementById('smsContent').value = '';
        document.getElementById('description').value = '';
    }
}

// Photo upload handling
function handlePhotoUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
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
    formData.append('image', file);
    formData.append('timestamp', new Date().toISOString());

    try {
        const response = await fetch('/api/photo/', {
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
    console.log(response)
    } catch (error) {
        console.error('Error:', error);
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
        const response = await fetch('/api/history');

        if (response.ok) {
            const transactions = await response.json();
            displayHistory(transactions);
        } else {
            throw new Error('Failed to load history');
        }
    } catch (error) {
        console.error('Error loading history:', error);
        displayHistory([]);
    }
}

// Display history
function displayHistory(transactions) {
    const historyContent = document.getElementById('historyContent');

    if (!transactions || transactions.length === 0) {
        historyContent.innerHTML = '<p style="text-align: center; color: #666;">هیچ تراکنشی یافت نشد</p>';
        return;
    }

    historyContent.innerHTML = transactions.map(transaction => {
        let typeLabel = '';
        let typeColor = '';

        if (transaction.type === -1) {
            typeLabel = 'برداشت';
            typeColor = '#d9534f';
        } else if (transaction.type === 1) {
            typeLabel = 'واریز';
            typeColor = '#5cb85c';
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

async function loadAnalytics(month = 4) {
    const analyticsContent = document.getElementById('analyticsContent');

    try {
        const summaryRes = await fetch(`/api/summary/?month=${month}`);
        const summary = await summaryRes.json();

        displayAnalytics({
            income: summary.income,
            expense: summary.expense,
            balance: summary.balance,
            suggestions: [
                {
                    title: 'تحلیل مالی ماه جاری ',
                    message: 'گزارشی برای نمایش وجود ندارد.'
                }
            ]
        });

        const result = await Swal.fire({
            title: 'پیشنهاد هوشمند💡',
            text: 'مایل هستید بر اساس الگوی تراکنش ها، وضعیت ماه جاری تحلیل و بررسی بشه ؟',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'بله، نمایش بده',
            cancelButtonText: 'خیر'
        });

        if (!result.isConfirmed) return;

        Swal.fire({
            title: 'در حال بررسی و پردازش تراکنش ها ...',
            text: 'لطفاً منتظر بمانید',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
        
        const suggestionsRes = await fetch(`/api/analytics/?income=${summary.income}&expense=${summary.expense}&balance=${summary.balance}`);
        const suggestionsData = await suggestionsRes.json();
        // console.log(suggestionsData)
        Swal.close();
        displayAnalytics({
                income: summary.income,
                expense: summary.expense,
                balance: summary.balance,
                suggestions: suggestionsData.suggestions ?? []
            });

    } catch (error) {
        console.error('Error loading analytics or suggestions:', error);

        displayAnalytics({
            income: summary.income,
            expense: summary.expense,
            balance: summary.balance,
            suggestions: [
                {
                    title: 'کاهش هزینه خرید',
                    message: 'هزینه خرید شما این ماه 20% افزایش یافته. سعی کنید از لیست خرید استفاده کنید.'
                },
                {
                    title: 'پس انداز',
                    message: 'با توجه به الگوی خرج شما، می‌توانید ماهانه 200,000 ریال پس‌انداز کنید.'
                }
            ]
        });
    }
}

function displayAnalytics(analytics) {
    const analyticsContent = document.getElementById('analyticsContent');

    const income = analytics?.income ?? 0;
    const expense = analytics?.expense ?? 0;
    const balance = analytics?.balance ?? 0;
    const suggestions = Array.isArray(analytics?.suggestions) ? analytics.suggestions : [];

    analyticsContent.innerHTML = `
        <div class="analytics-card">
            <h3>هزینه این ماه</h3>
            <div class="amount">${expense.toLocaleString()} ریال</div>
            <p>مجموع تراکنش‌های این ماه</p>
            <div style="display: flex;
                    justify-content: space-evenly;
                    margin-top: 15px;
                    background-color: white;
                    border-radius: 10px;
                    padding: 10px;">
                <div style="text-align: center;">
                    <div style="font-size: 10px; color: #28a745;">${income.toLocaleString()}+</div>
                    <div style="font-size: 10px; color: #373737;">درآمد</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 10px; color: #dc3545;">${expense.toLocaleString()}-</div>
                    <div style="font-size: 10px; color: #373737;">هزینه</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 10px; color: #17a2b8;">${balance.toLocaleString()}</div>
                    <div style="font-size: 10px; color: #373737;">باقی‌مانده</div>
                </div>
            </div>
        </div>

        <div class="card" id="suggestionsArea">     
            <h3 style="margin-bottom: 20px;">پیشنهادات هوشمند</h3>
        </div>
    `;

    const container = document.getElementById('suggestionsArea');

    let index = 0;
    function typeNextSuggestion() {
        if (index >= suggestions.length) return;

        const suggestion = suggestions[index];
        const card = document.createElement('div');
        card.className = 'suggestion-card';
        const title = document.createElement('h4');
        const message = document.createElement('p');

        title.textContent = suggestion.title;
        message.textContent = ''; 

        card.appendChild(title);
        card.appendChild(message);
        container.appendChild(card);

        typewriterEffect(message, suggestion.message, 0, () => {
            index++;
            setTimeout(typeNextSuggestion, 500);
        });
    }

    typeNextSuggestion(); 
}

function typewriterEffect(element, text, i = 0, callback) {
    if (i < text.length) {
        element.innerHTML += text.charAt(i);
        setTimeout(() => {
            typewriterEffect(element, text, i + 1, callback);
        }, 30);
    } else if (callback) {
        callback();
    }
}