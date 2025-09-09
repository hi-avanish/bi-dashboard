#!/bin/bash

# Create Feature Branch Script
# Usage: ./create-feature.sh feature-name

set -e

if [ -z "$1" ]; then
    echo "❌ Error: Please provide a feature name"
    echo "Usage: ./create-feature.sh feature-name"
    exit 1
fi

FEATURE_NAME=$1
BRANCH_NAME="feature/$FEATURE_NAME"

echo "🚀 Creating feature branch: $BRANCH_NAME"

# Switch to develop and pull latest
echo "📥 Switching to develop branch..."
git checkout develop
git pull origin develop

# Create and switch to feature branch
echo "🌿 Creating feature branch..."
git checkout -b $BRANCH_NAME

# Push to remote
echo "📤 Pushing to remote..."
git push -u origin $BRANCH_NAME

echo "✅ Feature branch '$BRANCH_NAME' created successfully!"
echo "🔗 You can now start working on your feature"
echo "📝 Don't forget to make meaningful commits!"
