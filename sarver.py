import os
from flask import Flask, request, send_from_directory, render_template_string, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# إعدادات التصميم
PRIMARY_COLOR = "#4361ee"
SECONDARY_COLOR = "#3f37c9"
BACKGROUND_COLOR = "#f8f9fa"
TEXT_COLOR = "#212529"
ACCENT_COLOR = "#4cc9f0"

# إعدادات الموقع
BASE_DIR = "my_website"
ALLOWED_EXTENSIONS = {'html', 'css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'ico'}
os.makedirs(BASE_DIR, exist_ok=True)
for folder in ['css', 'js', 'images', 'fonts']:
    os.makedirs(f"{BASE_DIR}/{folder}", exist_ok=True)

# دالة لحساب مساحة التخزين
def get_storage_info():
    total_size = 0
    file_count = 0
    
    for dirpath, dirnames, filenames in os.walk(BASE_DIR):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
            file_count += 1
    
    # تحويل البايت إلى ميغابايت
    total_size_mb = total_size / (1024 * 1024)
    
    return {
        'total_size': total_size,
        'total_size_mb': round(total_size_mb, 2),
        'file_count': file_count
    }

# واجهة التحكم الجميلة مع قسم التخزين
CONTROL_PANEL = f'''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام الاستضافة المتكامل</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: {PRIMARY_COLOR};
            --secondary: {SECONDARY_COLOR};
            --background: {BACKGROUND_COLOR};
            --text: {TEXT_COLOR};
            --accent: {ACCENT_COLOR};
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Tajawal', sans-serif;
        }}
        
        body {{
            background-color: var(--background);
            color: var(--text);
            line-height: 1.6;
            padding: 0;
        }}
        
        .container {{
            max-width: 100%;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 30px 20px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-radius: 0 0 20px 20px;
        }}
        
        h1 {{
            font-size: 2.2rem;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        
        .card-title {{
            color: var(--primary);
            margin-bottom: 20px;
            font-size: 1.4rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .card-title i {{
            font-size: 1.6rem;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--text);
        }}
        
        select, input, textarea {{
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s;
        }}
        
        select:focus, input:focus, textarea:focus {{
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
        }}
        
        textarea {{
            min-height: 200px;
            resize: vertical;
        }}
        
        .btn {{
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            width: 100%;
        }}
        
        .btn:hover {{
            background-color: var(--secondary);
            transform: translateY(-2px);
        }}
        
        .btn i {{
            font-size: 1.2rem;
        }}
        
        .file-list {{
            list-style: none;
        }}
        
        .file-item {{
            padding: 15px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.2s;
        }}
        
        .file-item:hover {{
            background-color: #f8f9fa;
        }}
        
        .file-link {{
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .file-actions {{
            display: flex;
            gap: 10px;
        }}
        
        .action-btn {{
            padding: 5px 10px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
        }}
        
        .view-btn {{
            background-color: var(--accent);
            color: white;
            border: none;
        }}
        
        .delete-btn {{
            background-color: #ff6b6b;
            color: white;
            border: none;
        }}
        
        .progress-container {{
            display: none;
            margin-top: 20px;
            background: #f1f3f5;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }}
        
        .progress-bar {{
            height: 6px;
            background: #e9ecef;
            border-radius: 3px;
            margin-top: 10px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: var(--primary);
            width: 0%;
            transition: width 0.3s;
        }}
        
        .result-message {{
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }}
        
        .success {{
            background-color: #ebfbee;
            color: #2b8a3e;
            border: 1px solid #40c057;
        }}
        
        .error {{
            background-color: #fff5f5;
            color: #c92a2a;
            border: 1px solid #ff6b6b;
        }}
        
        /* أنماط قسم التخزين */
        .storage-info {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .storage-item {{
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }}
        
        .storage-item .icon {{
            font-size: 2rem;
            color: var(--primary);
        }}
        
        .storage-label {{
            font-size: 0.9rem;
            color: #6c757d;
        }}
        
        .storage-value {{
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text);
        }}
        
        .progress-info {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-size: 0.9rem;
            color: #6c757d;
        }}
        
        .storage-progress-container {{
            grid-column: span 2;
            margin-top: 10px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            header {{
                padding: 20px 15px;
            }}
            
            h1 {{
                font-size: 1.8rem;
            }}
            
            .storage-info {{
                grid-template-columns: 1fr;
            }}
            
            .storage-progress-container {{
                grid-column: span 1;
            }}
        }}
        
        /* أيقونات */
        .icon {{
            font-family: 'Material Icons';
            font-weight: normal;
            font-style: normal;
            font-size: 24px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            -webkit-font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
        }}
    </style>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
</head>
<body>
    <header>
        <div class="container">
            <h1>نظام الاستضافة المتكامل</h1>
            <p class="subtitle">رفع وإدارة ملفات موقعك بكل سهولة</p>
        </div>
    </header>
    
    <div class="container">
        <div class="card">
            <h2 class="card-title">
                <span class="icon">cloud_upload</span>
                رفع ملفات جديدة
            </h2>
            
            <form id="uploadForm">
                <div class="form-group">
                    <label for="file_type">
                        <span class="icon">category</span>
                        نوع الملف
                    </label>
                    <select name="file_type" id="file_type" required>
                        <option value="">-- اختر نوع الملف --</option>
                        <option value="html">صفحة ويب (HTML)</option>
                        <option value="css">تنسيقات (CSS)</option>
                        <option value="js">أكواد جافاسكريبت (JS)</option>
                        <option value="images">صور (PNG, JPG, GIF)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="fileInput">
                        <span class="icon">attach_file</span>
                        اختر الملف
                    </label>
                    <input type="file" name="file" id="fileInput" required>
                </div>
                
                <button type="button" class="btn" onclick="uploadFile()">
                    <span class="icon">file_upload</span>
                    رفع الملف
                </button>
            </form>
            
            <div id="progressContainer" class="progress-container">
                <div id="progressText">جاري رفع الملف...</div>
                <div class="progress-bar">
                    <div id="progressFill" class="progress-fill"></div>
                </div>
            </div>
            
            <div id="resultMessage" class="result-message"></div>
        </div>
        
        <div class="card">
            <h2 class="card-title">
                <span class="icon">storage</span>
                معلومات التخزين
            </h2>
            
            <div class="storage-info">
                <div class="storage-item">
                    <span class="icon">folder</span>
                    <div>
                        <div class="storage-label">إجمالي الملفات</div>
                        <div class="storage-value" id="totalFiles">0</div>
                    </div>
                </div>
                
                <div class="storage-item">
                    <span class="icon">data_usage</span>
                    <div>
                        <div class="storage-label">المساحة المستخدمة</div>
                        <div class="storage-value" id="usedSpace">0 MB</div>
                    </div>
                </div>
                
                <div class="storage-progress-container">
                    <div class="progress-info">
                        <span>0% مستخدم</span>
                        <span>100% متبقي</span>
                    </div>
                    <div class="progress-bar">
                        <div id="storageProgress" class="progress-fill"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2 class="card-title">
                <span class="icon">folder</span>
                الملفات الموجودة
            </h2>
            
            <ul class="file-list" id="fileList">
                <!-- سيتم ملؤها بالجافاسكريبت -->
                <li class="file-item">
                    <span>جاري تحميل قائمة الملفات...</span>
                </li>
            </ul>
        </div>
    </div>
    
    <script>
        // رفع الملفات
        function uploadFile() {{
            const fileInput = document.getElementById('fileInput');
            const fileType = document.getElementById('file_type');
            const progressContainer = document.getElementById('progressContainer');
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            const resultMessage = document.getElementById('resultMessage');
            
            if (fileInput.files.length === 0) {{
                showResult('الرجاء اختيار ملف أولاً', 'error');
                return;
            }}
            
            if (!fileType.value) {{
                showResult('الرجاء اختيار نوع الملف', 'error');
                return;
            }}
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('file_type', fileType.value);
            
            // إظهار شريط التقدم
            progressContainer.style.display = 'block';
            progressFill.style.width = '0%';
            progressText.textContent = 'جاري رفع الملف...';
            resultMessage.style.display = 'none';
            
            // محاكاة تقدم الرفع (في الواقع الفعلي سيتم استخدام الأحداث الحقيقية)
            const progressInterval = setInterval(() => {{
                const currentWidth = parseInt(progressFill.style.width) || 0;
                if (currentWidth < 90) {{
                    progressFill.style.width = (currentWidth + 10) + '%';
                }}
            }}, 300);
            
            fetch('/upload', {{
                method: 'POST',
                body: formData
            }})
            .then(response => response.json())
            .then(data => {{
                clearInterval(progressInterval);
                progressFill.style.width = '100%';
                progressText.textContent = 'اكتمل الرفع!';
                
                if (data.status === 'success') {{
                    showResult(`تم رفع الملف بنجاح: ${{data.filename}}`, 'success');
                    loadFiles(); // تحديث قائمة الملفات ومعلومات التخزين
                }} else {{
                    showResult(data.message || 'حدث خطأ أثناء الرفع', 'error');
                }}
                
                // إخفاء شريط التقدم بعد 3 ثواني
                setTimeout(() => {{
                    progressContainer.style.display = 'none';
                }}, 3000);
            }})
            .catch(error => {{
                clearInterval(progressInterval);
                showResult('حدث خطأ في الاتصال بالخادم', 'error');
                progressContainer.style.display = 'none';
                console.error('Error:', error);
            }});
        }}
        
        // عرض رسائل النتيجة
        function showResult(message, type) {{
            const resultMessage = document.getElementById('resultMessage');
            resultMessage.textContent = message;
            resultMessage.className = 'result-message ' + type;
            resultMessage.style.display = 'block';
        }}
        
        // جلب قائمة الملفات
        function loadFiles() {{
            fetch('/api/files')
            .then(response => response.json())
            .then(data => {{
                const fileList = document.getElementById('fileList');
                fileList.innerHTML = '';
                
                if (data.files.length === 0) {{
                    fileList.innerHTML = '<li class="file-item">لا توجد ملفات بعد</li>';
                }} else {{
                    data.files.forEach(file => {{
                        const li = document.createElement('li');
                        li.className = 'file-item';
                        
                        const link = document.createElement('a');
                        link.href = `/${{file}}`;
                        link.className = 'file-link';
                        link.target = '_blank';
                        link.innerHTML = `
                            <span class="icon">${{getFileIcon(file)}}</span>
                            ${{file}}
                        `;
                        
                        const actions = document.createElement('div');
                        actions.className = 'file-actions';
                        
                        const viewBtn = document.createElement('button');
                        viewBtn.className = 'action-btn view-btn';
                        viewBtn.innerHTML = '<span class="icon">visibility</span> عرض';
                        viewBtn.onclick = () => window.open(`/${{file}}`, '_blank');
                        
                        const deleteBtn = document.createElement('button');
                        deleteBtn.className = 'action-btn delete-btn';
                        deleteBtn.innerHTML = '<span class="icon">delete</span> حذف';
                        deleteBtn.onclick = () => deleteFile(file);
                        
                        actions.appendChild(viewBtn);
                        actions.appendChild(deleteBtn);
                        li.appendChild(link);
                        li.appendChild(actions);
                        fileList.appendChild(li);
                    }});
                }}
                
                // تحديث معلومات التخزين
                updateStorageInfo(data.storage_info);
            }})
            .catch(error => {{
                console.error('Error loading files:', error);
            }});
        }}
        
        // تحديث معلومات التخزين
        function updateStorageInfo(storageInfo) {{
            document.getElementById('totalFiles').textContent = storageInfo.file_count;
            document.getElementById('usedSpace').textContent = `${{storageInfo.total_size_mb}} MB`;
            
            // حساب النسبة المئوية (افترضنا أن الحد الأقصى هو 100MB للتخزين)
            const maxStorageMB = 100;
            const percentage = Math.min((storageInfo.total_size_mb / maxStorageMB) * 100, 100);
            
            document.getElementById('storageProgress').style.width = `${{percentage}}%`;
            
            // تحديث النصوص
            const progressInfo = document.querySelector('.progress-info');
            if (progressInfo) {{
                progressInfo.innerHTML = `
                    <span>${{percentage.toFixed(1)}}% مستخدم</span>
                    <span>${{(100 - percentage).toFixed(1)}}% متبقي</span>
                `;
            }}
        }}
        
        // حذف الملف
        function deleteFile(filename) {{
            if (confirm(`هل أنت متأكد من حذف الملف ${{filename}}؟`)) {{
                fetch(`/api/delete/${{encodeURIComponent(filename)}}`, {{
                    method: 'DELETE'
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.status === 'success') {{
                        showResult(`تم حذف الملف ${{filename}}`, 'success');
                        loadFiles(); // تحديث قائمة الملفات ومعلومات التخزين
                    }} else {{
                        showResult(data.message || 'حدث خطأ أثناء الحذف', 'error');
                    }}
                }})
                .catch(error => {{
                    showResult('حدث خطأ في الاتصال بالخادم', 'error');
                    console.error('Error:', error);
                }});
            }}
        }}
        
        // تحديد أيقونة الملف حسب نوعه
        function getFileIcon(filename) {{
            if (filename.endsWith('.html')) return 'html';
            if (filename.endsWith('.css')) return 'css';
            if (filename.endsWith('.js')) return 'javascript';
            if (filename.endsWith('.png') || filename.endsWith('.jpg') || filename.endsWith('.jpeg') || filename.endsWith('.gif')) return 'image';
            return 'insert_drive_file';
        }}
        
        // تحميل الملفات عند فتح الصفحة
        document.addEventListener('DOMContentLoaded', loadFiles);
    </script>
</body>
</html>
'''

# الصفحة الرئيسية
@app.route('/')
def control_panel():
    return CONTROL_PANEL

# واجهة API لسرد الملفات
@app.route('/api/files')
def list_files_api():
    files = []
    for root, dirs, filenames in os.walk(BASE_DIR):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(root, filename), BASE_DIR)
            files.append(rel_path.replace('\\', '/'))
    
    storage_info = get_storage_info()
    
    return jsonify({
        'files': files,
        'storage_info': storage_info
    })

# حذف الملفات
@app.route('/api/delete/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        file_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'status': 'success', 'message': f'تم حذف الملف {filename}'})
        return jsonify({'status': 'error', 'message': 'الملف غير موجود'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# رفع الملفات
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'لم يتم اختيار ملف'
        }), 400
    
    file = request.files['file']
    file_type = request.form.get('file_type', '')
    
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'لم يتم اختيار ملف'
        }), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # تحديد مسار الحفظ بناءً على نوع الملف
        if file_type in ['css', 'js', 'images', 'fonts']:
            save_path = os.path.join(BASE_DIR, file_type, filename)
            filepath = f"{file_type}/{filename}"
        else:
            save_path = os.path.join(BASE_DIR, filename)
            filepath = filename
        
        file.save(save_path)
        
        return jsonify({
            'status': 'success',
            'filename': filename,
            'filepath': filepath
        })
    
    return jsonify({
        'status': 'error',
        'message': 'نوع الملف غير مسموح به'
    }), 400

# عرض الملفات
@app.route('/<path:filename>')
def serve_file(filename):
    # تحديد مجلد الملف بناءً على الامتداد
    if filename.endswith('.css'):
        return send_from_directory(f"{BASE_DIR}/css", filename)
    elif filename.endswith('.js'):
        return send_from_directory(f"{BASE_DIR}/js", filename)
    elif any(filename.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
        return send_from_directory(f"{BASE_DIR}/images", filename)
    else:
        return send_from_directory(BASE_DIR, filename)

# التحقق من نوع الملف المسموح به
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)