Sure! Here's a more structured and enhanced version of your deployment documentation with the addition of headings, subheadings, emojis, logos, and code formatting for better readability and usefulness:

---

# 🚀 Dokku Deployment Guide for **Shortly Link Shortener**

This guide walks you through the process of deploying the **Shortly Link Shortener** app using **Dokku** on a remote VPS server. Dokku simplifies application deployment by leveraging Docker containers, making it easy to scale, deploy, and manage your applications.

---

## 🛠️ **Prerequisites**

Before setting up **Dokku**, you need to ensure that you have:

- A **VPS** server (Ubuntu 20.04+ recommended).
- **Docker** installed on the server.
- A **domain name** configured for your app.
- A **GitHub repository** for the app.

---

## **Step 1: Install Dokku on Your VPS**

### 📥 Download and Install Dokku

Run the following commands on your **VPS** to install Dokku.

```bash
wget https://dokku.com/install/v0.29.3/bootstrap.sh
sudo DOKKU_TAG=v0.29.3 bash bootstrap.sh
```

---

## **Step 2: Create Your Application on Dokku**

### 📦 Create the Application

Once Dokku is installed, create a new app on your server.

```bash
dokku apps:create shortly
```

---

## **Step 3: Configure Your Domain**

### 🌐 Add Your Domain to Dokku

To bind your domain to the app, use the following command. Replace `shortly.anujjamdade.site` with your domain.

```bash
dokku domains:add shortly shortly.anujjamdade.site
```

---

## **Step 4: Set Up SSH Access for Deployment**

### 🔑 Generate SSH Key (if not already generated)

On your local machine, generate an SSH key pair.

```bash
ssh-keygen -t rsa -b 4096
```

### 🖥️ Copy Your Public SSH Key to the VPS

Copy the public key to your Dokku VPS to enable SSH access for deployment.

```bash
cat ~/.ssh/id_rsa.pub | ssh root@107.173.2.159 "dokku ssh-keys:add <your-username> -"
```

---

## **Step 5: Set Up SSL for Your Domain** 🔒

Dokku supports **Let's Encrypt** for SSL certificates, ensuring secure communication with your app.

### 🔧 Install the Let's Encrypt Plugin

```bash
sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
```

### ⚡ Enable SSL for Your Domain

```bash
dokku letsencrypt:set shortly email ajk952626@gmail.com
dokku letsencrypt:enable shortly
```

### 🔄 Automatic Certificate Renewal

Set up a cron job for automatic SSL certificate renewal.

```bash
dokku letsencrypt:cron-job --add
```

---

## **Step 6: Set Environment Variables** ⚙️

Set the necessary environment variables for your app.

```bash
dokku config:set shortly SECRET_KEY=<your-secret-key> DEBUG=False DATABASE_URL=postgres://postgres:your_password@db:5432/shortlydb
```

---

## **Step 7: Deploy Your Code to Dokku** 💻

### 🛠️ Push Your Code Using Git

To deploy your application to Dokku, add the remote and push your code.

```bash
ssh root@107.173.2.159
git remote add dokku dokku@107.173.2.159:shortly
git push dokku main
```

Alternatively, use the following command to deploy directly from GitHub:

```bash
dokku git:sync --build shortly https://github.com/anujjamdade007/Shortly-link-Shortner-Using-Django.git main
```

---

## **Step 8: Database Configuration** 🗄️

### 🔌 Install PostgreSQL Plugin

Install the PostgreSQL plugin to set up a database for your app.

```bash
dokku plugin:install https://github.com/dokku/dokku-postgres.git
```

### 🏗️ Create a PostgreSQL Database

```bash
dokku postgres:create shortly-db
```

### 🔗 Link the Database to Your App

```bash
dokku postgres:link shortly-db shortly
```

### 📋 View the Database Link

```bash
dokku config:show shortly
```

---

## **Other Useful Commands** 📋

### 🔍 View Application Logs

Check the logs to debug or monitor your app.

```bash
dokku logs shortly
```

### 🛑 Stop the App

Stop the app when necessary.

```bash
dokku ps:stop shortly
```

### 🔄 Restart the App

Restart your app after making changes.

```bash
dokku ps:restart shortly
```

---

## 🔄 **Summary of Key Commands**

| Command                                           | Description                                             |
| ------------------------------------------------- | ------------------------------------------------------- |
| `dokku apps:create <app-name>`                    | Create a new application                                 |
| `dokku domains:add <app-name> <your-domain>`      | Set a domain for your app                                |
| `dokku plugin:install <plugin-url>`               | Install a plugin (e.g., Let's Encrypt or PostgreSQL)     |
| `dokku config:set <app-name> <key=value>`         | Set environment variables                                |
| `dokku git:sync --build <app-name> <repo-url>`     | Deploy app directly from GitHub                          |
| `dokku logs <app-name>`                           | View logs for the app                                    |
| `dokku ps:stop <app-name>`                        | Stop the app                                            |
| `dokku ps:restart <app-name>`                     | Restart the app                                         |

---

## 🎉 **You're All Set!** 🎉

Once you've completed these steps, your **Shortly Link Shortener** app should be up and running on **Dokku**, complete with a secure SSL certificate and a working PostgreSQL database.

Creating a **superuser** for your application, especially for a **Django** project, is an important step in managing your app's admin panel. Below are the steps on how to do that along with other necessary configurations using **Dokku**.

---

## 🔑 **Creating a Superuser for Your Django App**

If you're using **Django** and need to create a superuser, follow these steps.

### 📋 **Step 1: Access the Application’s Container**

First, you need to access the running container where your app is deployed. Use the following command to open a **bash shell** within your container.

```bash
dokku run shortly bash
```

This command will log you into the container for the `shortly` app.

### 🛠️ **Step 2: Create the Superuser**

Once you're inside the container, you can run Django's management command to create a superuser. The command to create a superuser in Django is:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter a **username**, **email address**, and **password** for the superuser.

#### Example Prompt:
```bash
Username (leave blank to use 'root'): admin
Email address: admin@example.com
Password: ********
Password (again): ********
```

After filling out the prompts, the superuser will be created successfully!

### 🏁 **Step 3: Exit the Container**

Once the superuser is created, you can exit the container by typing:

```bash
exit
```

---