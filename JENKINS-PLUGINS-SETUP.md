# Jenkins Plugins Setup Guide

## 🔧 **Required Jenkins Plugins**

To use advanced features like Docker agents, you need to install these plugins:

### **Essential Plugins for CI/CD Pipeline**

1. **Docker Pipeline Plugin**
   - **Purpose**: Enables Docker agents in Jenkinsfiles
   - **Install**: Manage Jenkins → Manage Plugins → Available → Search "Docker Pipeline"
   - **Required for**: Docker agent support

2. **Git Plugin**
   - **Purpose**: Git integration
   - **Install**: Usually pre-installed
   - **Required for**: Source code management

3. **Email Extension Plugin**
   - **Purpose**: Email notifications
   - **Install**: Manage Jenkins → Manage Plugins → Available → Search "Email Extension"
   - **Required for**: Email notifications

4. **HTML Publisher Plugin**
   - **Purpose**: Publish HTML reports
   - **Install**: Manage Jenkins → Manage Plugins → Available → Search "HTML Publisher"
   - **Required for**: Coverage reports

5. **Build Timeout Plugin**
   - **Purpose**: Build timeout management
   - **Install**: Manage Jenkins → Manage Plugins → Available → Search "Build Timeout"
   - **Required for**: Build management

6. **Timestamper Plugin**
   - **Purpose**: Add timestamps to build logs
   - **Install**: Manage Jenkins → Manage Plugins → Available → Search "Timestamper"
   - **Required for**: Better logging

7. **Workspace Cleanup Plugin**
   - **Purpose**: Clean workspace after builds
   - **Install**: Manage Jenkins → Manage Plugins → Available → Search "Workspace Cleanup"
   - **Required for**: Workspace management

## 🚀 **Installation Steps**

### **Step 1: Access Plugin Management**
1. **Go to Jenkins**: http://5.161.59.136:8080
2. **Click "Manage Jenkins"** (left sidebar)
3. **Click "Manage Plugins"**

### **Step 2: Install Plugins**
1. **Go to "Available" tab**
2. **Search for each plugin** listed above
3. **Check the box** next to each plugin
4. **Click "Install without restart"**
5. **Wait for installation** to complete

### **Step 3: Restart Jenkins**
1. **Go to "Manage Jenkins"**
2. **Click "Restart Jenkins when no jobs are running"**
3. **Wait for restart** to complete

## 🔧 **Alternative: Use Basic Jenkinsfile**

If you don't want to install plugins, use the basic Jenkinsfile:

### **Use Jenkinsfile.basic**
1. **Go to your Jenkins job**: MLOps
2. **Click "Configure"**
3. **Copy content from `Jenkinsfile.basic`**
4. **Paste into Pipeline script**
5. **Click "Save"**

### **Features of Basic Jenkinsfile**
- ✅ **No Docker agents required**
- ✅ **Works with basic Jenkins setup**
- ✅ **Detects available Python commands**
- ✅ **Graceful fallbacks for missing tools**
- ✅ **Email notifications**
- ✅ **All pipeline stages**

## 📋 **Plugin Installation Checklist**

- [ ] **Docker Pipeline Plugin** - For Docker agents
- [ ] **Git Plugin** - For source code management
- [ ] **Email Extension Plugin** - For email notifications
- [ ] **HTML Publisher Plugin** - For coverage reports
- [ ] **Build Timeout Plugin** - For build management
- [ ] **Timestamper Plugin** - For better logging
- [ ] **Workspace Cleanup Plugin** - For workspace management

## 🧪 **Test Plugin Installation**

### **Test Docker Pipeline Plugin**
1. **Create a test job**
2. **Use this simple pipeline**:
   ```groovy
   pipeline {
       agent {
           docker {
               image 'hello-world'
           }
       }
       stages {
           stage('Test') {
               steps {
                   echo 'Docker agent working!'
               }
           }
       }
   }
   ```
3. **Run the job**
4. **If successful**, Docker Pipeline plugin is working

### **Test Email Extension Plugin**
1. **Go to "Manage Jenkins" → "Configure System"**
2. **Scroll to "Extended E-mail Notification"**
3. **If section exists**, Email Extension plugin is installed

## 🔍 **Troubleshooting**

### **Common Issues**

1. **"Plugin not found"**
   - Check plugin name spelling
   - Ensure Jenkins has internet access
   - Try refreshing the plugin list

2. **"Installation failed"**
   - Check Jenkins logs
   - Ensure sufficient disk space
   - Try installing plugins one by one

3. **"Plugin not working"**
   - Restart Jenkins after installation
   - Check plugin compatibility
   - Verify plugin configuration

### **Useful Commands**

```bash
# Check Jenkins logs
docker logs jenkins-server

# Restart Jenkins
docker restart jenkins-server

# Check installed plugins
docker exec jenkins-server ls /var/jenkins_home/plugins/ | grep -E "(docker|git|email|html)"
```

## 🎯 **Recommended Approach**

### **Option 1: Install Plugins (Advanced)**
- **Pros**: Full Docker agent support, advanced features
- **Cons**: Requires plugin installation
- **Best for**: Production environments

### **Option 2: Use Basic Jenkinsfile (Simple)**
- **Pros**: Works immediately, no plugin installation
- **Cons**: Limited Docker agent support
- **Best for**: Quick setup, testing

## 🚀 **Next Steps**

1. **Choose your approach**:
   - Install plugins for advanced features
   - Use basic Jenkinsfile for simple setup

2. **Test the pipeline**:
   - Run a manual build
   - Check all stages work correctly
   - Verify email notifications

3. **Configure additional features**:
   - Set up GitHub webhooks
   - Configure DockerHub credentials
   - Test complete CI/CD flow

The basic Jenkinsfile should work immediately without any plugin installation!
