#!/bin/bash

echo "🚀 Home Vision AI Mobile App Setup"
echo "=================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are installed"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if Android Studio is installed (for Android development)
if command -v adb &> /dev/null; then
    echo "✅ Android SDK is available"
    echo "📱 To run on Android: npm run android"
else
    echo "⚠️  Android SDK not found. Install Android Studio for Android development."
fi

# Check if Xcode is installed (for iOS development, macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v xcodebuild &> /dev/null; then
        echo "✅ Xcode is available"
        echo "🍎 To run on iOS: npm run ios"
    else
        echo "⚠️  Xcode not found. Install Xcode for iOS development."
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start Metro bundler: npm start"
echo "2. Run on Android: npm run android"
echo "3. Run on iOS: npm run ios (macOS only)"
echo ""
echo "Demo credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "Note: Make sure your backend server is running at http://localhost:8000"
