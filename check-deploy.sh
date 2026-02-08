#!/bin/bash
echo "=== Vercel Deployment Checker ==="
echo "Waiting for new deployment..."
echo ""

OLD_BUILD="index-BVZ62spy.js"
MAX_ATTEMPTS=30
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  ATTEMPT=$((ATTEMPT + 1))
  echo "Attempt $ATTEMPT/$MAX_ATTEMPTS..."

  CURRENT=$(curl -s "https://drag-n-scroll.vercel.app" | grep -o "index-[^\"]*\.js" | head -1)

  if [ ! -z "$CURRENT" ] && [ "$CURRENT" != "$OLD_BUILD" ]; then
    echo ""
    echo "✓ NEW BUILD DETECTED: $CURRENT"
    echo "Deployment is complete!"
    echo ""
    echo "=== READY TO TEST ==="
    echo "1. Open browser in INCOGNITO mode"
    echo "2. Go to: https://drag-n-scroll.vercel.app"
    echo "3. Test registration and login"
    echo ""
    exit 0
  else
    echo "  Still old build: ${CURRENT:-not found}"
  fi

  sleep 10
done

echo ""
echo "✗ Timeout: Deployment not complete"
echo "Check Vercel dashboard: https://vercel.com/dashboard"
exit 1
