I have made a twitter like social network website.
A user can make posts, edit posts, delete posts, like and unlike posts, follow and unfollow users, can see his/her followers and following list. 

**Link to the youtube video**
https://youtu.be/I6UAnPrGiIE?si=YTDZIglYj2kAdH7n

**Deployed on Amazon EC2**
http://16.171.129.151/login?next=/

# How to run your application

**Prerequisites**:\
Make sure you have the following installed:
- Python (3.6 or higher)

**Create a Virtual environment**
```python -m venv env```

**Activate your environement**
```env\Scripts\activate```

**Install these requirements**
```
pip install django==3.2
pip install django-crispy-forms==1.11.2
pip install django-debug-toolbar==3.2.4
```

**Clone the repository**
```
git clone <repository-url>
cd <repository-directory>
```

**Run the Development Server:**
```
python manage.py runserver

```
