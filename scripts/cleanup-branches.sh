#!/bin/bash

# Cleanup Merged Branches Script
# Usage: ./cleanup-branches.sh

set -e

echo "🧹 Cleaning up merged branches..."

# Switch to develop
git checkout develop
git pull origin develop

# Switch to main
git checkout main  
git pull origin main

# Back to develop
git checkout develop

echo "🔍 Finding merged branches..."

# List branches that have been merged
MERGED_BRANCHES=$(git branch --merged | grep -v "\*\|main\|develop" | tr -d ' ')

if [ -z "$MERGED_BRANCHES" ]; then
    echo "✅ No merged branches to clean up"
    exit 0
fi

echo "📋 Found merged branches:"
echo "$MERGED_BRANCHES"

read -p "🗑️  Delete these branches? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Delete local merged branches
    echo "$MERGED_BRANCHES" | xargs -n 1 git branch -d
    
    # Prune remote tracking branches
    git remote prune origin
    
    echo "✅ Cleanup completed!"
else
    echo "❌ Cleanup cancelled"
fi
