# DockerHub Credentials Setup Guide

## 🔧 **Configure DockerHub Credentials in Jenkins**

To enable Docker image pushing to DockerHub, you need to configure credentials in Jenkins.

### **Step 1: Create DockerHub Access Token**

1. **Go to DockerHub**: https://hub.docker.com/
2. **Login** with your account (`masteroz`)
3. **Click on your profile** (top right)
4. **Go to "Account Settings"**
5. **Click "Security"** (left sidebar)
6. **Click "New Access Token"**
7. **Fill in the form**:
   - **Access Token Description**: `Jenkins CI/CD Pipeline`
   - **Access permissions**: `Read, Write, Delete`
8. **Click "Generate"**
9. **Copy the token** (you won't see it again!)

### **Step 2: Configure Jenkins Credentials**

1. **Go to Jenkins**: http://5.161.59.136:8080
2. **Click "Manage Jenkins"** (left sidebar)
3. **Click "Manage Credentials"**
4. **Click on "Global"** (or your domain)
5. **Click "Add Credentials"**
6. **Fill in the form**:
   ```
   Kind: Username with password
   Scope: Global
   Username: masteroz
   Password: [Your DockerHub Access Token]
   ID: dockerhub-credentials
   Description: DockerHub credentials for CI/CD pipeline
   ```
7. **Click "OK"**

### **Step 3: Test DockerHub Connection**

1. **Go to your Jenkins job**: MLOps
2. **Click "Configure"**
3. **Scroll to "Build Environment"**
4. **Add "Use secret text(s) or file(s)"**
5. **Select "dockerhub-credentials"**
6. **Click "Save"**

### **Step 4: Run Pipeline Test**

1. **Click "Build Now"**
2. **Check the build logs**
3. **Look for "Push to DockerHub" stage**
4. **Verify successful push**

## 🐳 **DockerHub Repository Setup**

### **Create Repository on DockerHub**

1. **Go to DockerHub**: https://hub.docker.com/
2. **Click "Create Repository"**
3. **Fill in the form**:
   ```
   Repository Name: zomato-flask-app
   Visibility: Public (or Private)
   Description: Flask Zomato Restaurant Price Prediction App
   ```
4. **Click "Create"**

### **Repository URL**
Your Docker image will be available at:
```
https://hub.docker.com/r/masteroz/zomato-flask-app
```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **"Authentication failed"**
   - Check DockerHub username and access token
   - Ensure access token has correct permissions
   - Verify credentials ID in Jenkins

2. **"Repository not found"**
   - Create the repository on DockerHub first
   - Check repository name matches Jenkinsfile
   - Ensure repository is public or you have access

3. **"Push failed"**
   - Check Docker image was built successfully
   - Verify DockerHub credentials are correct
   - Check network connectivity

### **Useful Commands**

```bash
# Test Docker login locally
docker login -u masteroz
# Enter your access token when prompted

# Test push locally
docker tag masteroz/zomato-flask-app:latest masteroz/zomato-flask-app:test
docker push masteroz/zomato-flask-app:test

# Check Jenkins logs
docker logs jenkins-server
```

## 📋 **Expected Pipeline Flow**

After setup, your pipeline should:

1. **✅ Checkout**: Pull code from repository
2. **✅ Code Quality**: Run flake8 checks
3. **✅ Unit Tests**: Run pytest tests
4. **✅ Build Docker**: Build Docker image
5. **✅ Push to DockerHub**: Push image to DockerHub
6. **✅ Security Scan**: Scan image for vulnerabilities
7. **✅ Email Notification**: Send success/failure email

## 🎯 **Success Indicators**

### **Build Logs Should Show:**
```
[Pipeline] stage
[Pipeline] { (Push to DockerHub)
[Pipeline] echo
Pushing Docker image to DockerHub...
[Pipeline] script
[Pipeline] {
[Pipeline] withCredentials
[Pipeline] {
[Pipeline] sh
+ echo Logging into DockerHub...
Logging into DockerHub...
+ echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
Login Succeeded
+ echo Pushing image to DockerHub...
Pushing image to DockerHub...
+ docker push masteroz/zomato-flask-app:10
The push refers to repository [docker.io/masteroz/zomato-flask-app]
...
+ docker push masteroz/zomato-flask-app:latest
The push refers to repository [docker.io/masteroz/zomato-flask-app]
...
+ echo Docker image pushed successfully to DockerHub!
Docker image pushed successfully to DockerHub!
+ echo Image URL: https://hub.docker.com/r/masteroz/zomato-flask-app
Image URL: https://hub.docker.com/r/masteroz/zomato-flask-app
```

### **DockerHub Should Show:**
- **New image tags**: `10`, `latest`
- **Updated timestamp**: Recent push time
- **Image size**: Appropriate size for Flask app

## 🚀 **Next Steps**

1. **Set up DockerHub credentials** in Jenkins
2. **Create DockerHub repository** if not exists
3. **Run the pipeline** to test Docker push
4. **Verify image** appears on DockerHub
5. **Test email notifications** are working

The Docker image will be pushed to DockerHub once the credentials are configured!
