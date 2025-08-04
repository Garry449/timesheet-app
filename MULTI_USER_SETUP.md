# Multi-User Timesheet System Setup Guide

## 🏢 Local Network Hosting for Multiple Users

This guide will help you set up your timesheet system so multiple users can access it from their computers using their own usernames and passwords.

## 📋 Prerequisites

1. **Your Computer (Server)**:
   - Windows 10/11
   - Python 3.7+ installed
   - SQL Server Express running
   - At least 2GB RAM free

2. **User Computers**:
   - Any device with a web browser (Windows, Mac, Linux, mobile)
   - Connected to the same network as your computer

## 🚀 Quick Start

### Step 1: Start the Server
1. Double-click `start_production_server.bat`
2. Wait for the server to start
3. Note your computer's IP address (shown in the console)

### Step 2: Configure Windows Firewall
1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Add Python and allow it on Private networks
4. Or temporarily disable firewall for testing

### Step 3: Share with Users
Share this URL with your users:
```
http://YOUR_COMPUTER_IP:8080
```

## 👥 User Management

### For New Users:
1. Users visit: `http://YOUR_IP:8080/register`
2. They create their own account
3. They can immediately start using the system

### For Admin Management:
1. You (admin) visit: `http://YOUR_IP:8080/admin`
2. Manage users, projects, and assignments
3. Monitor timesheet submissions

## 🔧 Advanced Setup

### Auto-Start on Boot:
1. Create a shortcut to `start_production_server.bat`
2. Press `Win + R`, type `shell:startup`
3. Copy the shortcut to the startup folder

### Custom Port (if 8080 is busy):
1. Edit `production_server.py`
2. Change `PORT = 8080` to `PORT = 8081` (or any free port)
3. Update user URLs accordingly

### Database Backup:
1. Set up SQL Server backup jobs
2. Or use the CSV export feature in the admin panel

## 🌐 Network Access URLs

### For Users:
- **Registration**: `http://YOUR_IP:8080/register`
- **Login**: `http://YOUR_IP:8080/login`
- **Dashboard**: `http://YOUR_IP:8080/dashboard`

### For Admin:
- **Admin Panel**: `http://YOUR_IP:8080/admin`
- **User Management**: `http://YOUR_IP:8080/admin/users`
- **Project Management**: `http://YOUR_IP:8080/admin/projects`

## 🔒 Security Considerations

1. **Network Security**: Only trusted users should have network access
2. **User Passwords**: Users should use strong passwords
3. **Regular Backups**: Backup your database regularly
4. **Updates**: Keep Python and dependencies updated

## 🛠️ Troubleshooting

### Server Won't Start:
- Check if Python is installed: `python --version`
- Install dependencies: `pip install -r requirements-local.txt`
- Check if port 8080 is free: `netstat -an | findstr 8080`

### Users Can't Connect:
- Check Windows Firewall settings
- Verify users are on the same network
- Test with `ping YOUR_IP` from user computers
- Try accessing from your own computer first

### Database Issues:
- Ensure SQL Server Express is running
- Check connection string in `db_local.py`
- Verify database exists and tables are created

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify all prerequisites are met
3. Test with a single user first
4. Check Windows Event Viewer for system errors

## 🎯 Success Checklist

- [ ] Server starts without errors
- [ ] You can access from your computer
- [ ] Users can access from their computers
- [ ] Users can register and login
- [ ] Admin panel works
- [ ] Timesheet functionality works
- [ ] Database is accessible

---

**Happy Timesheet Management!** 📊 