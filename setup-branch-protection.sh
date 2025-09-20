#!/bin/bash

# Branch Protection Setup Script for Group Assignment
# This script helps set up branch protection rules for your GitHub repository

echo "🔒 Setting up Branch Protection Rules for Group Assignment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo ""
echo "📋 Branch Protection Rules Setup Guide"
echo "======================================"
echo ""
echo "You need to set up branch protection rules in your GitHub repository:"
echo ""
echo "1. Go to your GitHub repository"
echo "2. Click on 'Settings' tab"
echo "3. Click on 'Branches' in the left sidebar"
echo "4. Click 'Add rule' for each branch"
echo ""
echo "🔒 Required Branch Protection Rules:"
echo ""
echo "📌 DEV BRANCH:"
echo "   - Branch name pattern: dev"
echo "   - ❌ NO pull request required (direct push allowed)"
echo "   - ✅ Restrict pushes that create files larger than 100MB"
echo "   - ✅ Require status checks to pass before merging (for PRs to test)"
echo ""
echo "📌 TEST BRANCH:"
echo "   - Branch name pattern: test"
echo "   - ✅ Require a pull request before merging"
echo "   - ✅ Require approvals (1 reviewer)"
echo "   - ✅ Dismiss stale PR approvals when new commits are pushed"
echo "   - ✅ Require status checks to pass before merging"
echo "   - ✅ Require branches to be up to date before merging"
echo "   - ✅ Restrict pushes that create files larger than 100MB"
echo ""
echo "📌 MASTER BRANCH:"
echo "   - Branch name pattern: master"
echo "   - ✅ Require a pull request before merging"
echo "   - ✅ Require approvals (1 reviewer)"
echo "   - ✅ Dismiss stale PR approvals when new commits are pushed"
echo "   - ✅ Require status checks to pass before merging"
echo "   - ✅ Require branches to be up to date before merging"
echo "   - ✅ Restrict pushes that create files larger than 100MB"
echo "   - ✅ Include administrators"
echo ""
echo "🔧 Required Status Checks:"
echo "   - dev branch: 'Code Quality Check' (on push)"
echo "   - test branch: 'Unit Tests' (on PR)"
echo "   - master branch: 'Jenkins Build' (on PR)"
echo ""
echo "👥 Admin Permissions:"
echo "   - Only the admin can merge PRs"
echo "   - Admin receives email notifications"
echo "   - Admin can bypass branch protection if needed"
echo ""
echo "📧 Email Notifications:"
echo "   - Update ADMIN_EMAIL in Jenkinsfile"
echo "   - Configure SMTP settings in Jenkins"
echo "   - Test email notifications"
echo ""
print_success "Branch protection setup guide completed!"
echo ""
echo "🚀 Next Steps:"
echo "1. Set up branch protection rules in GitHub"
echo "2. Configure Jenkins email notifications"
echo "3. Test the complete pipeline"
echo "4. Verify admin approval workflow"
echo ""
echo "📚 For detailed setup instructions, see GROUP-ASSIGNMENT-SETUP.md"
