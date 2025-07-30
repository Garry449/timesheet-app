# 🚀 Hosting Guide - Timesheet Management System

## Quick Start (Local Network Hosting)

### Option 1: Using the Batch File (Windows)
1. **Double-click** `start_server.bat`
2. The server will start automatically
3. Access from any device on your network

### Option 2: Manual Start
```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python run_server.py
```

## 🌐 Accessing Your Application

### From Your Computer
- **Local Access**: http://localhost:5000
- **Network Access**: http://YOUR_IP:5000

### From Other Devices (Same Network)
1. **Find your computer's IP address**:
   - Windows: Open CMD and type `ipconfig`
   - Look for "IPv4 Address" (usually 192.168.x.x)
   
2. **Access the app**:
   - Use: `http://YOUR_IP:5000`
   - Example: `http://192.168.1.100:5000`

## 🔧 Configuration

### Environment Variables (Optional)
```bash
# Set port (default: 5000)
set PORT=8080

# Enable debug mode
set FLASK_DEBUG=true

# Start server
python run_server.py
```

### Firewall Settings
- **Windows**: Allow Python/Flask through Windows Firewall
- **Router**: No special configuration needed for local network

## 📱 Network Access Troubleshooting

### If other devices can't access:
1. **Check Windows Firewall**:
   - Open Windows Defender Firewall
   - Allow Python through firewall
   
2. **Check Antivirus**:
   - Some antivirus software blocks network access
   - Add exception for Python/Flask

3. **Check Network**:
   - Ensure all devices are on the same network
   - Try accessing from different devices

## 🚀 Production Hosting Options

### Option 1: Heroku (Free Tier)
```bash
# Install Heroku CLI
# Create Procfile
echo "web: python run_server.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Option 2: PythonAnywhere (Free Tier)
1. Upload your code to PythonAnywhere
2. Set up WSGI configuration
3. Deploy

### Option 3: Railway (Free Tier)
1. Connect your GitHub repository
2. Railway auto-deploys your app
3. Get a public URL

## 🔒 Security Considerations

### For Local Network Hosting:
- ✅ Safe for office/home networks
- ✅ No internet exposure
- ⚠️ Anyone on your network can access

### For Internet Hosting:
- 🔒 Use HTTPS
- 🔒 Strong passwords
- 🔒 Regular updates
- 🔒 Database security

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Ensure SQL Server is running
3. Verify database connection settings in `db.py`
4. Check Windows Firewall settings

## 🎯 Next Steps

After hosting:
1. **Test access** from different devices
2. **Create admin user** if needed
3. **Add projects and tasks**
4. **Invite team members** to use the system 