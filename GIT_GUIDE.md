# Git Repository Guide

## 🚀 Files to COMMIT (Track in Git)

### ✅ Source Code
- `backend/` - All Python backend code
- `frontend/src/` - All React frontend code
- `tests/` - All test files
- `*.py` - Python files
- `*.js` / `*.jsx` - JavaScript/React files
- `*.css` - Stylesheets
- `*.html` - HTML files

### ✅ Configuration Files
- `package.json` - Node.js dependencies
- `package-lock.json` - Exact dependency versions
- `tailwind.config.js` - Tailwind CSS config
- `postcss.config.js` - PostCSS config
- `tsconfig.json` - TypeScript config
- `docker-compose.yml` - Docker configuration
- `.vscode/` - VS Code settings (except sensitive ones)

### ✅ Documentation
- `README.md` - Project documentation
- `SETUP.md` - Setup instructions
- `project-structure.md` - Project structure
- `LICENSE` - License file
- `*.md` - All markdown files

### ✅ Important JSON Files
- `tests/camera_config.json` - Camera configuration (without sensitive data)
- `backend/app/config/` - Configuration files (without secrets)

### ✅ Test Files
- `tests/camera_integration_test.py`
- `tests/capture_single_frame.py`
- `tests/frontend_api_test.js`
- `tests/rtsp_test.py`
- `tests/firebase_test.py`

## 🚫 Files to IGNORE (Don't Track)

### ❌ Dependencies & Build Artifacts
- `node_modules/` - Node.js dependencies
- `__pycache__/` - Python cache
- `*.pyc` - Python compiled files
- `build/` - Build outputs
- `dist/` - Distribution files

### ❌ Environment & Secrets
- `.env` - Environment variables
- `*.json` - JSON files (except important ones)
- `backend/app/config/home-vision-ai-firebase-adminsdk-*.json` - Firebase credentials
- `catcam/` - Virtual environment

### ❌ Temporary Files
- `*.jpg` / `*.jpeg` / `*.png` - Camera frames
- `*.mp4` / `*.avi` / `*.mov` - Video files
- `test_*.jpg` - Test frame outputs
- `direct_frame.jpg` - Test frames
- `api_frame.jpg` - Test frames
- `frames/` - Temporary frame directory

### ❌ IDE & OS Files
- `.vscode/settings.json` - Personal VS Code settings
- `.vscode/launch.json` - Personal debug config
- `.vscode/tasks.json` - Personal tasks
- `.DS_Store` - macOS system files
- `Thumbs.db` - Windows system files

### ❌ Logs & Cache
- `*.log` - Log files
- `.cache/` - Cache directories
- `coverage/` - Test coverage reports

## 📋 Recommended Git Commands

### Add Important Files
```bash
# Add source code
git add backend/
git add frontend/src/
git add tests/

# Add configuration files
git add package.json
git add package-lock.json
git add tailwind.config.js
git add postcss.config.js
git add docker-compose.yml

# Add documentation
git add *.md
git add LICENSE

# Add important config files
git add tests/camera_config.json
git add .gitignore
```

### Ignore Temporary Files
```bash
# These files are automatically ignored by .gitignore
# No need to manually ignore them
```

### Check What Will Be Committed
```bash
git status
git diff --cached
```

### Commit Changes
```bash
git add .
git commit -m "Add camera integration and frontend components"
git push origin main
```

## 🔒 Security Notes

### Never Commit:
- API keys
- Database passwords
- Firebase credentials
- Personal environment variables
- Camera passwords in plain text

### Safe to Commit:
- Configuration templates
- Example environment files
- Non-sensitive camera configs
- Public API endpoints

## 📁 Project Structure After Cleanup

```
Home-Vision-AI/
├── backend/                 # ✅ Commit
├── frontend/               # ✅ Commit (except node_modules)
├── tests/                  # ✅ Commit
├── .vscode/               # ✅ Commit (except personal settings)
├── .gitignore             # ✅ Commit
├── README.md              # ✅ Commit
├── LICENSE                # ✅ Commit
├── docker-compose.yml     # ✅ Commit
├── package.json           # ✅ Commit
└── [temporary files]      # ❌ Ignore
``` 