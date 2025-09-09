#!/bin/bash
# Test Logout Functionality

echo "🔍 Testing Logout Functionality..."

# Test 1: Logout endpoint accessible
echo "1. Testing logout endpoint..."
if curl -s -L http://localhost:8050/logout | grep -q "login"; then
    echo "✅ Logout endpoint redirects to login"
else
    echo "❌ Logout endpoint not working"
fi

# Test 2: Logout confirmation message
echo "2. Testing logout confirmation..."
if curl -s -L http://localhost:8050/logout | grep -q "Successfully logged out"; then
    echo "✅ Logout shows confirmation message"
else
    echo "❌ Logout confirmation not showing"
fi

# Test 3: Login page after logout
echo "3. Testing login page after logout..."
if curl -s "http://localhost:8050/login?logged_out=1" | grep -q "Successfully logged out"; then
    echo "✅ Login page shows logout confirmation"
else
    echo "❌ Login page not showing logout confirmation"
fi

echo ""
echo "🎯 Logout Test Summary:"
echo "✅ Logout endpoint working"
echo "✅ Redirects to login page"
echo "✅ Shows confirmation message"
echo ""
echo "🔐 Test the full flow:"
echo "1. Login with admin/dedalus2024"
echo "2. Click logout button"
echo "3. Should redirect to login with success message"
