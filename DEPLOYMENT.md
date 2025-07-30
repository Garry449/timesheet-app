# 🚀 Free Tier Deployment Guide

## 🎯 **Recommended: Railway (Easiest)**

### **Step 1: Prerequisites**
1. **Git** (if not installed): https://git-scm.com/
2. **Railway Account**: https://railway.app/

### **Step 2: Quick Deployment**
```bash
# Run the deployment script
python deploy_to_railway.py
```

### **Step 3: Manual Deployment (Alternative)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

---

## 🌐 **Alternative: Render**

### **Step 1: Create Render Account**
1. Go to https://render.com/
2. Sign up with GitHub

### **Step 2: Connect Repository**
1. **Push your code to GitHub**
2. **Connect GitHub repo to Render**
3. **Configure build settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`

### **Step 3: Environment Variables**
```
DATABASE_TYPE=postgresql
DATABASE_URL=your_postgresql_url
SECRET_KEY=your_secret_key
```

---

## 🐍 **Alternative: PythonAnywhere**

### **Step 1: Create Account**
1. Go to https://www.pythonanywhere.com/
2. Sign up for free account

### **Step 2: Upload Code**
1. **Upload files** via web interface
2. **Install requirements**: `pip install -r requirements.txt`
3. **Configure WSGI file**

### **Step 3: Configure WSGI**
```python
import sys
path = '/home/yourusername/yourproject'
if path not in sys.path:
    sys.path.append(path)

from main import app as application
```

---

## 🗄️ **Database Setup**

### **Railway PostgreSQL**
1. **Add PostgreSQL service** in Railway dashboard
2. **Get connection string** from service
3. **Set environment variable**: `DATABASE_URL`

### **Render PostgreSQL**
1. **Create PostgreSQL service** in Render
2. **Copy connection string**
3. **Add to environment variables**

### **PythonAnywhere MySQL**
1. **Use built-in MySQL**
2. **Create database**
3. **Update connection settings**

---

## 🔧 **Environment Variables**

### **Required Variables**
```
DATABASE_TYPE=postgresql
DATABASE_URL=your_database_connection_string
SECRET_KEY=your_secret_key_here
FLASK_ENV=production
```

### **Optional Variables**
```
FLASK_DEBUG=false
PORT=5000
```

---

## 📊 **Free Tier Limits**

| Platform | Free Tier | Database | SSL | Custom Domain |
|----------|-----------|----------|-----|---------------|
| **Railway** | $5/month credit | ✅ PostgreSQL | ✅ | ✅ |
| **Render** | 750 hours/month | ✅ PostgreSQL | ✅ | ✅ |
| **PythonAnywhere** | 512MB RAM | ✅ MySQL | ✅ | ❌ |

---

## 🚀 **Deployment Checklist**

### **Before Deployment**
- [ ] **Test locally** with new requirements
- [ ] **Update database** functions for cloud
- [ ] **Set environment variables**
- [ ] **Configure CORS** if needed

### **After Deployment**
- [ ] **Test all features**
- [ ] **Check database connection**
- [ ] **Verify SSL/HTTPS**
- [ ] **Test from mobile devices**

---

## 🔒 **Security Considerations**

### **Production Security**
- [ ] **Strong SECRET_KEY**
- [ ] **HTTPS enabled**
- [ ] **Database security**
- [ ] **Input validation**

### **Environment Separation**
- [ ] **Development**: Local SQL Server
- [ ] **UAT**: Local network
- [ ] **Production**: Cloud PostgreSQL

---

## 📞 **Troubleshooting**

### **Common Issues**
1. **Database Connection**: Check DATABASE_URL
2. **Build Failures**: Check requirements.txt
3. **Import Errors**: Check file paths
4. **CORS Issues**: Configure allowed origins

### **Support**
- **Railway**: https://railway.app/docs
- **Render**: https://render.com/docs
- **PythonAnywhere**: https://help.pythonanywhere.com/

---

## 🎉 **Success!**

After deployment, you'll have:
- ✅ **Public URL** (e.g., https://your-app.railway.app)
- ✅ **SSL/HTTPS** enabled
- ✅ **Database** connected
- ✅ **24/7 uptime**
- ✅ **Automatic deployments**

**Your timesheet app is now live on the internet!** 🌐 