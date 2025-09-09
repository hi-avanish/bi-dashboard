# Quick Git Workflow Reference

## 🚀 Complete Feature Workflow

### Step 1: Create Feature Branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
git push -u origin feature/your-feature-name
```

### Step 2: Development & Commit
```bash
# Make your changes
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

### Step 3: Create Pull Request
```bash
gh pr create --base develop --head feature/your-feature-name \
  --title "Feature: Your Feature Name" \
  --body "Description of changes"
```

### Step 4: Review Process
```bash
# Request review (done via GitHub UI)
# Address feedback if needed
git add .
git commit -m "fix: address review feedback"
git push origin feature/your-feature-name
```

### Step 5: Merge to Develop
```bash
gh pr merge PR_NUMBER --merge
git checkout develop
git pull origin develop
```

### Step 6: Release to Main
```bash
gh pr create --base main --head develop \
  --title "Release: Version X.X.X" \
  --body "Release notes"
gh pr merge PR_NUMBER --merge
```

### Step 7: Cleanup
```bash
git checkout main
git pull origin main
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## 📋 Quick Commands

| Action | Command |
|--------|---------|
| Create branch | `git checkout -b feature/name` |
| Switch branch | `git checkout branch-name` |
| Stage changes | `git add .` |
| Commit | `git commit -m "message"` |
| Push | `git push origin branch-name` |
| Pull latest | `git pull origin branch-name` |
| Create PR | `gh pr create --base develop --head feature/name` |
| Merge PR | `gh pr merge PR_NUMBER --merge` |
| Delete branch | `git branch -d branch-name` |

## 🔄 Branch Flow

```
main (production)
  ↑
develop (integration)
  ↑
feature/your-feature (development)
```

## ✅ Checklist

- [ ] Created feature branch from develop
- [ ] Made changes and committed with clear messages
- [ ] Pushed branch to remote
- [ ] Created PR to develop
- [ ] Requested and received code review
- [ ] Merged to develop
- [ ] Created release PR to main
- [ ] Merged to main
- [ ] Deleted feature branch locally and remotely

## 🚨 Emergency Commands

### Undo Last Commit (not pushed)
```bash
git reset --soft HEAD~1
```

### Undo Last Commit (already pushed)
```bash
git revert HEAD
git push origin branch-name
```

### Fix Merge Conflicts
```bash
git status  # See conflicted files
# Edit files to resolve conflicts
git add .
git commit -m "resolve: merge conflicts"
```

### Sync with Latest Develop
```bash
git checkout develop
git pull origin develop
git checkout feature/your-branch
git rebase develop
```
