# Group Assignment CI/CD Pipeline Setup

## 👥 **Group Structure (2 Members)**

### **Admin Role**
- **Responsibility**: Approve pull requests and receive notifications
- **Email**: hassanejaz400@gmail.com
- **Permissions**: Can merge PRs to test and master branches

### **Developer Role**
- **Responsibility**: Develop features and push to dev branch
- **Permissions**: Can push to feature branches and dev branch, create PRs to test/master

## 🌿 **Branch Structure & Workflow**

```
Feature Branch → Push → dev branch → GitHub Actions (flake8)
                ↓
dev branch → PR → test branch → GitHub Actions (unit tests)
                ↓
test branch → PR → master branch → Jenkins (Docker build + push)
                ↓
master branch → Email notification to admin
```

## 🔄 **Complete Workflow Steps**

### **Step 1: Feature Development**
```bash
# Developer creates feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

### **Step 2: Dev Branch Integration (Code Quality)**
```bash
# Push directly to dev branch
git checkout dev
git merge feature/new-feature
git push origin dev

# GitHub Actions will run automatically:
# - flake8 code quality check
# - Syntax error detection
# - Code style validation
```

### **Step 3: Test Branch Integration (Unit Tests)**
```bash
# Create PR: dev → test
# GitHub Actions will run:
# - Unit tests (pytest)
# - Coverage reports
# - Test result validation
```

### **Step 4: Master Branch Integration (Docker Build)**
```bash
# Create PR: test → master
# After admin approval and merge:
# - Jenkins CI/CD pipeline triggers
# - Builds Docker image
# - Pushes to DockerHub (masteroz/zomato-flask-app)
# - Sends email notification to admin
```

## 🚀 **Jenkins Setup Instructions**

### **1. Run Jenkins Setup on VPS**
```bash
# On your VPS (5.161.59.136)
./jenkins-setup.sh
```

### **2. Access Jenkins**
- **URL**: http://5.161.59.136:8080
- **Get initial password**: `docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword`

### **3. Install Required Plugins**
Go to **Manage Jenkins → Manage Plugins** and install:
- ✅ **Git** - Source code management
- ✅ **Docker Pipeline** - Docker integration
- ✅ **Email Extension** - Email notifications
- ✅ **HTML Publisher** - Coverage reports
- ✅ **Build Timeout** - Build management
- ✅ **Timestamper** - Build timestamps
- ✅ **Workspace Cleanup** - Cleanup after builds

### **4. Configure Credentials**

#### **GitHub Credentials**
- **Type**: Username with password
- **ID**: `github-credentials`
- **Username**: Your GitHub username
- **Password**: GitHub personal access token

#### **DockerHub Credentials**
- **Type**: Username with password
- **ID**: `dockerhub-credentials`
- **Username**: `masteroz`
- **Password**: DockerHub access token

### **5. Configure Email Notifications**

#### **SMTP Settings (Gmail Example)**
```
SMTP Server: smtp.gmail.com
SMTP Port: 587
Use SSL: Yes
Use TLS: Yes
Username: your-email@gmail.com
Password: your-app-password
```

#### **Email Configuration**
- Go to **Manage Jenkins → Configure System**
- Scroll to **Extended E-mail Notification**
- Configure SMTP settings
- Set default recipient list to admin email
- Test configuration

### **6. Create Jenkins Pipeline Job**

1. **New Item → Pipeline**
2. **Pipeline Name**: `zomato-flask-cicd`
3. **Pipeline Script**: Select "Pipeline script from SCM"
4. **SCM**: Git
5. **Repository URL**: Your GitHub repository URL
6. **Credentials**: Select `github-credentials`
7. **Script Path**: `Jenkinsfile`
8. **Branch**: `*/master`

### **7. Configure GitHub Webhooks**

1. Go to your GitHub repository
2. **Settings → Webhooks → Add webhook**
3. **Payload URL**: `http://5.161.59.136:8080/github-webhook/`
4. **Content type**: `application/json`
5. **Events**: Select "Just the push event"
6. **Active**: ✅

## 🧪 **Testing the Pipeline**

### **Test 1: Code Quality Check (dev branch)**
```bash
# Push directly to dev branch
git checkout dev
echo "# Test change" >> README.md
git add README.md
git commit -m "test: trigger flake8 check"
git push origin dev
```
**Expected**: GitHub Actions runs flake8 check automatically on push

### **Test 2: Unit Tests (test branch)**
```bash
# Create PR: dev → test
# After PR approval and merge:
# - GitHub Actions runs unit tests
# - Generates coverage reports
```

### **Test 3: Docker Build (master branch)**
```bash
# Create PR: test → master
# After admin approval and merge:
# - Jenkins pipeline triggers
# - Builds Docker image
# - Pushes to DockerHub
# - Sends email notification to admin
```

## 📧 **Email Notifications**

### **Success Email to Admin**
```
Subject: ✅ Jenkins Build Success: zomato-flask-cicd #123

🎉 Build Successful!

Project: zomato-flask-cicd
Build Number: 123
Branch: master
Commit: abc123def456
Docker Image: masteroz/zomato-flask-app:123
DockerHub URL: https://hub.docker.com/r/masteroz/zomato-flask-app
Build URL: http://5.161.59.136:8080/job/zomato-flask-cicd/123/

✅ All tests passed and Docker image has been successfully pushed to DockerHub.
🚀 The application is now ready for deployment!
```

### **Failure Email to Admin**
```
Subject: ❌ Jenkins Build Failed: zomato-flask-cicd #124

🚨 Build Failed!

Project: zomato-flask-cicd
Build Number: 124
Branch: master
Commit: def456ghi789
Build URL: http://5.161.59.136:8080/job/zomato-flask-cicd/124/

❌ Please check the build logs for more details and fix the issues.
🔧 Contact the development team for assistance.
```

## 🔧 **Required Files for Assignment**

### **1. Model & Dataset**
- ✅ **model.pkl** - Trained machine learning model
- ✅ **zomato_df.csv** - Unique dataset for your group
- ✅ **model.py** - Model training script

### **2. Flask Application**
- ✅ **app.py** - Flask web application
- ✅ **templates/index.html** - Web interface
- ✅ **static/css/style.css** - Styling
- ✅ **requirements.txt** - Dependencies

### **3. Testing**
- ✅ **tests/** - Unit test suite
- ✅ **pytest.ini** - Test configuration
- ✅ **conftest.py** - Test fixtures

### **4. CI/CD Pipeline**
- ✅ **Jenkinsfile** - Jenkins pipeline script
- ✅ **Dockerfile** - Docker container configuration
- ✅ **docker-compose.yml** - Local development setup
- ✅ **.github/workflows/** - GitHub Actions workflows

### **5. Documentation**
- ✅ **README.md** - Project documentation
- ✅ **CI-CD-SETUP.md** - Setup instructions
- ✅ **GROUP-ASSIGNMENT-SETUP.md** - This guide

## 🎯 **Assignment Checklist**

### **Tools Used** ✅
- [x] **Jenkins** - CI/CD pipeline orchestration
- [x] **GitHub** - Source code repository
- [x] **GitHub Actions** - Automated testing workflows
- [x] **Git** - Version control
- [x] **Docker** - Containerization
- [x] **Python** - Programming language
- [x] **Flask** - Web framework

### **Workflow Requirements** ✅
- [x] **Admin approval** for all merges
- [x] **dev branch** - Code quality checks (flake8)
- [x] **test branch** - Unit testing
- [x] **master branch** - Docker build and push
- [x] **Email notifications** to admin

### **Pipeline Stages** ✅
- [x] **Code Quality** - flake8 on dev branch
- [x] **Unit Testing** - pytest on test branch
- [x] **Docker Build** - Containerization on master
- [x] **DockerHub Push** - Image registry
- [x] **Email Notification** - Admin alerts

## 🚀 **Quick Start Commands**

### **Setup Jenkins**
```bash
# On your VPS
./jenkins-setup.sh
```

### **Test Pipeline**
```bash
# Test code quality
git checkout dev
echo "# Test" >> README.md
git add README.md
git commit -m "test: trigger workflow"
git push origin dev

# Test unit tests (after PR approval)
git checkout test
git merge dev
git push origin test

# Test Docker build (after PR approval)
git checkout master
git merge test
git push origin master
```

### **Monitor Results**
- **GitHub Actions**: https://github.com/your-username/your-repo/actions
- **Jenkins**: http://5.161.59.136:8080
- **DockerHub**: https://hub.docker.com/r/masteroz/zomato-flask-app

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Jenkins not accessible**
   - Check firewall: `sudo ufw allow 8080`
   - Verify container: `docker ps`
   - Check logs: `docker logs jenkins-server`

2. **GitHub webhook not triggering**
   - Verify webhook URL
   - Check Jenkins GitHub plugin
   - Ensure repository permissions

3. **Docker build fails**
   - Check Dockerfile syntax
   - Verify all files in context
   - Check .dockerignore

4. **Email not sending**
   - Verify SMTP settings
   - Check firewall restrictions
   - Use app password for Gmail

### **Useful Commands**
```bash
# View Jenkins logs
docker logs jenkins-server

# Restart Jenkins
docker restart jenkins-server

# Check Jenkins plugins
docker exec jenkins-server ls /var/jenkins_home/plugins/

# Test Docker build locally
docker build -t masteroz/zomato-flask-app .
docker run -p 5000:5000 masteroz/zomato-flask-app
```

## 📊 **Monitoring Dashboard**

### **Jenkins Dashboard**
- **URL**: http://5.161.59.136:8080
- **View**: Build history, trends, performance
- **Monitor**: Pipeline execution, success rates

### **GitHub Actions**
- **URL**: https://github.com/your-username/your-repo/actions
- **View**: Workflow runs, test results
- **Monitor**: Code quality, test coverage

### **DockerHub**
- **URL**: https://hub.docker.com/r/masteroz/zomato-flask-app
- **View**: Image versions, tags, security scans
- **Monitor**: Image pushes, vulnerabilities

## 🎉 **Assignment Completion**

Once all components are set up and tested:

1. ✅ **Jenkins** is running and accessible
2. ✅ **GitHub Actions** are working for dev and test branches
3. ✅ **Docker** images are being built and pushed
4. ✅ **Email notifications** are being sent to admin
5. ✅ **All workflows** are functioning correctly

Your group assignment CI/CD pipeline is now complete! 🚀
