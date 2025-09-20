# Jenkins Email Configuration

## SMTP Settings for Email Notifications

### Gmail Configuration
```
SMTP Server: smtp.gmail.com
SMTP Port: 587
Use SSL: Yes
Use TLS: Yes
Username: hassanejaz400@gmail.com
Password: your-google-app-password
```

### Outlook/Hotmail Configuration
```
SMTP Server: smtp-mail.outlook.com
SMTP Port: 587
Use SSL: No
Use TLS: Yes
Username: your-email@outlook.com
Password: your-password
```

### Custom SMTP Configuration
```
SMTP Server: your-smtp-server.com
SMTP Port: 587 (or 465 for SSL)
Use SSL: Yes/No (depending on your server)
Use TLS: Yes/No (depending on your server)
Username: your-username
Password: your-password
```

## Jenkins Configuration Steps

1. **Install Email Extension Plugin**
   - Go to Manage Jenkins → Manage Plugins
   - Search for "Email Extension"
   - Install and restart Jenkins

2. **Configure SMTP Settings**
   - Go to Manage Jenkins → Configure System
   - Scroll to "Extended E-mail Notification"
   - Configure SMTP settings as above
   - Test configuration

3. **Configure Default Email Settings**
   - Set default recipient list
   - Configure email templates
   - Set trigger conditions

## Email Templates

### Success Template
```
Subject: ✅ Build Success: ${PROJECT_NAME} #${BUILD_NUMBER}

Build Status: SUCCESS
Project: ${PROJECT_NAME}
Build Number: ${BUILD_NUMBER}
Branch: ${GIT_BRANCH}
Commit: ${GIT_COMMIT}
Build URL: ${BUILD_URL}

All tests passed and Docker image has been pushed successfully.
```

### Failure Template
```
Subject: ❌ Build Failed: ${PROJECT_NAME} #${BUILD_NUMBER}

Build Status: FAILURE
Project: ${PROJECT_NAME}
Build Number: ${BUILD_NUMBER}
Branch: ${GIT_BRANCH}
Commit: ${GIT_COMMIT}
Build URL: ${BUILD_URL}

Please check the build logs for more details.
```

## Post-Build Actions

Add these post-build actions to your Jenkins job:

1. **Editable Email Notification**
   - Project Recipient List: your-email@example.com
   - Trigger: Always
   - Subject: ${PROJECT_NAME} - Build ${BUILD_STATUS} #${BUILD_NUMBER}
   - Body: Use the templates above

2. **Email Extension**
   - Recipient List: ${CHANGE_AUTHOR_EMAIL}
   - Trigger: Success, Failure, Unstable
   - Content Type: HTML
   - Attach Build Log: Yes
