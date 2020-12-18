import bcrypt
from django.db import models
from django_random_queryset import RandomManager

class UserManager(models.Manager):
    def validateRegister(self, post_data): 
        errors={}
        
        if len(post_data['first_name']) == 0 and len(post_data['password']) == 0 and len(post_data['email']) == 0:
            errors['all']='All fields are required'            
#--------------------------------------------First Name------------------------------------------
        else:
            if post_data['first_name'] == '' :
                errors['first_name']='First Name field is required'
            elif len(post_data['first_name']) < 3:
                errors['first_name']='First Name should be at least 3 characters'
            elif not post_data['first_name'].isalpha():
                errors['first_name']='First Name should only contain letters'
#--------------------------------------------Email-----------------------------------------------
            if post_data['email'] == '' :
                errors['email']='Email field is required'
            if self.validate_email_exist(post_data) is True:
                errors['email']='Sorry. An account with that email already exists'    
#-------------------------------------------Password-----------------------------------------
            if len(post_data['password']) < 8 :
                errors['password']='Password should be at least 8 characters'
            elif post_data['password'] != post_data['password_confirm']:
                errors['password'] = "Please make sure that both passwords match"
        return errors

    def validateLogin(self, post_data):
        error={}
        if len(post_data['email']) == 0  or len(post_data['password']) == 0:
            error['all']='Please type your email and password' 
        else:
            user = User.objects.filter(email=post_data['email'].lower()) 
            if len(user) < 1:
                error['email']='Sorry. This email does not exist in our database'
                return  error
            current_logged_user = user[0]   
            check_password = bcrypt.checkpw(post_data['password'].encode(), current_logged_user.password.encode()) 
            if not check_password:
                error['password']='Your email/password combination is incorrect'
        return error

    def validate_email_exist(self, post_data):
        check_email_exist=len(self.filter(email=post_data['email'].lower()))
        if check_email_exist > 0:
            return True
        return False

class User(models.Model):
    first_name= models.CharField(max_length=40)
    last_name= models.CharField(max_length=40, blank=True)
    email= models.EmailField()
    password= models.CharField(max_length=120)
    isadmin=models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #commented_by = a list of comments written by the current user    FROM Comment
    #reply_by  = a list of users that replied to a specific comment   FROM Reply
    #written_by = a list of questions written by the current user     FROM Question
    #quiz_details = FROM Score
    
    objects = UserManager() 
    
    def __repr__(self):
        return f'<User object: ID:{self.id} First Name:{self.first_name} Last Name:{self.last_name} Email:{self.email} isadmin:{self.isadmin}>'