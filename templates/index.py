<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EyzCrypt Enterprise</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>EYZCRYPT <span class="badge">V1.0</span></h1>
            <p>Military-Grade Pure Python Encryption</p>
        </header>

        <div class="main-card">
            <form id="cryptoForm" enctype="multipart/form-data">
                <div class="form-group">
                    <label>Master Password (Leave empty for default)</label>
                    <input type="password" name="password" placeholder="eyzzey">
                </div>
                
                <div class="upload-area" id="uploadArea">
                    <p>Drag & Drop file here or Click to Browse</p>
                    <input type="file" name="file" id="fileInput" hidden>
                </div>

                <div class="actions">
                    <button type="button" class="btn encrypt" onclick="processFile('encrypt')">🔒 Encrypt</button>
                    <button type="button" class="btn decrypt" onclick="processFile('decrypt')">🔓 Decrypt</button>
                </div>
            </form>
        </div>
        <div id="status"></div>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        
        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', (e) => { e.preventDefault(); uploadArea.style.borderColor = "#00ffcc"; });
        uploadArea.addEventListener('dragleave', () => { uploadArea.style.borderColor = "#444"; });
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileInput.files = e.dataTransfer.files;
            uploadArea.querySelector('p').textContent = fileInput.files[0].name;
        });

        async function processFile(action) {
            if (!fileInput.files.length) return alert("Please select a file");
            
            const formData = new FormData(document.getElementById('cryptoForm'));
            formData.append('action', action);
            
            document.getElementById('status').innerHTML = "Processing... Please wait.";
            
            try {
                const response = await fetch('/process', { method: 'POST', body: formData });
                if (!response.ok) throw new Error("Processing failed");
                
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = action === 'encrypt' ? fileInput.files[0].name + '.eyz' : fileInput.files[0].name.replace('.eyz', '');
                document.body.appendChild(a);
                a.click();
                a.remove();
                document.getElementById('status').innerHTML = "✅ Done! File downloaded.";
            } catch (error) {
                document.getElementById('status').innerHTML = "❌ Error: " + error.message;
            }
        }
    </script>
</body>
</html>
