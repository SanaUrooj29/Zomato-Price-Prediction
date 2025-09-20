# Jenkins Job Configuration Guide

## 🔧 **Fix Jenkins Pipeline Configuration**

The error you're seeing is because the Jenkins job isn't configured to use "Pipeline script from SCM". Here are two solutions:

## **Solution 1: Configure Job as "Pipeline script from SCM" (Recommended)**

### **Step 1: Update Jenkins Job Configuration**

1. **Go to your Jenkins job** (MLOps)
2. **Click "Configure"**
3. **In "Pipeline" section**:
   - **Definition**: Select "Pipeline script from SCM"
   - **SCM**: Select "Git"
   - **Repository URL**: `https://github.com/SanaUrooj29/Zomato-Price-Prediction.git`
   - **Credentials**: Select your GitHub credentials
   - **Branch**: `*/master`
   - **Script Path**: `Jenkinsfile.scm`

4. **Click "Save"**

### **Step 2: Use the SCM Jenkinsfile**

The `Jenkinsfile.scm` uses `checkout scm` which works with "Pipeline script from SCM" configuration.

## **Solution 2: Use Manual Git Checkout (Current Fix)**

### **Step 1: Keep Current Job Configuration**

1. **Go to your Jenkins job** (MLOps)
2. **Click "Configure"**
3. **In "Pipeline" section**:
   - **Definition**: Keep as "Pipeline script"
   - **Script**: Use the updated `Jenkinsfile` (with manual git checkout)

4. **Click "Save"**

### **Step 2: The Updated Jenkinsfile**

The current `Jenkinsfile` now uses:
```groovy
git branch: 'master', url: 'https://github.com/SanaUrooj29/Zomato-Price-Prediction.git'
```

## **Recommended Approach: Use Solution 1**

I recommend using **Solution 1** because:
- ✅ **Better integration** with GitHub
- ✅ **Automatic webhook triggers**
- ✅ **Branch-specific builds**
- ✅ **Cleaner configuration**

## **Step-by-Step Setup (Solution 1)**

### **1. Configure Jenkins Job**

1. **Go to Jenkins**: http://5.161.59.136:8080
2. **Click on your job**: MLOps
3. **Click "Configure"**
4. **Scroll to "Pipeline" section**
5. **Change settings**:
   ```
   Definition: Pipeline script from SCM
   SCM: Git
   Repository URL: https://github.com/SanaUrooj29/Zomato-Price-Prediction.git
   Credentials: github-credentials
   Branch: */master
   Script Path: Jenkinsfile.scm
   ```
6. **Click "Save"**

### **2. Test the Pipeline**

1. **Click "Build Now"**
2. **Check the build logs**
3. **Verify all stages run successfully**

### **3. Set up GitHub Webhook**

1. **Go to GitHub repository**
2. **Settings → Webhooks → Add webhook**
3. **Payload URL**: `http://5.161.59.136:8080/github-webhook/`
4. **Content type**: `application/json`
5. **Events**: Just the push event
6. **Active**: ✅

## **Troubleshooting**

### **Common Issues**

1. **"Repository not found"**
   - Check repository URL
   - Verify GitHub credentials
   - Ensure repository is public or credentials have access

2. **"Branch not found"**
   - Check branch name (master)
   - Ensure branch exists in repository

3. **"Script not found"**
   - Check script path (Jenkinsfile.scm)
   - Ensure file exists in repository

4. **"Credentials not found"**
   - Go to Manage Jenkins → Manage Credentials
   - Add GitHub credentials with ID: `github-credentials`

### **Useful Commands**

```bash
# Check Jenkins logs
docker logs jenkins-server

# Restart Jenkins
docker restart jenkins-server

# Check Jenkins plugins
docker exec jenkins-server ls /var/jenkins_home/plugins/ | grep git
```

## **Expected Workflow**

Once configured correctly:

1. **Push to master branch** → GitHub webhook triggers Jenkins
2. **Jenkins checks out code** using `checkout scm`
3. **Runs all pipeline stages**:
   - Code Quality Check (flake8)
   - Unit Tests (pytest)
   - Build Docker Image
   - Security Scan
   - Push to DockerHub
4. **Sends email notification** to hassanejaz400@gmail.com

## **Next Steps**

1. **Configure Jenkins job** using Solution 1
2. **Test the pipeline** with a manual build
3. **Set up GitHub webhook** for automatic triggers
4. **Test with a real push** to master branch
5. **Verify email notifications** are working

The pipeline should now work correctly without the `checkout scm` error!
