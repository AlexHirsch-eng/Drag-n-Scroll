#!/bin/bash
# Script to deploy frontend to Vercel with correct environment variables

echo "=== Deploying Drag'n'Scroll Frontend to Vercel ==="
echo ""

# Check if in frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the frontend directory"
    echo "   Run: cd frontend"
    exit 1
fi

echo "✓ Found package.json"
echo ""

# Check if Vercel CLI is installed
echo "Checking Vercel CLI..."
if command -v vercel &> /dev/null; then
    echo "✓ Vercel CLI $(vercel --version)"
else
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

echo ""
echo "=== IMPORTANT ==="
echo "You will need to login to Vercel if not already logged in"
echo ""

# Login to Vercel
echo "Checking Vercel login status..."
if ! npx vercel whoami &> /dev/null; then
    echo "⚠ Not logged in. Opening browser for login..."
    npx vercel login
else
    echo "✓ Already logged in to Vercel"
fi

echo ""
echo "=== Deploying to Production ==="
echo ""

# Deploy to production
echo "Running: npx vercel --prod --yes"
npx vercel --prod --yes

if [ $? -eq 0 ]; then
    echo ""
    echo "=== ✅ DEPLOYMENT SUCCESSFUL ==="
    echo ""
    echo "Your app is now live at: https://drag-n-scroll.vercel.app"
    echo ""
    echo "Next steps:"
    echo "1. Open browser in INCOGNITO mode"
    echo "2. Go to: https://drag-n-scroll.vercel.app"
    echo "3. Test registration and login"
    echo ""
else
    echo ""
    echo "=== ❌ DEPLOYMENT FAILED ==="
    echo "Please check the errors above and try again"
    echo ""
    exit 1
fi
