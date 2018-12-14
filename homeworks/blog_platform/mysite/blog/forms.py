from django import forms
from django.forms import ModelForm, HiddenInput
from blog.models import Comment, Blogg, Post, User

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['user_id', 'comment_text', 'post_id']
		widgets = {
			'post_id': HiddenInput(),
            'user_id': HiddenInput()
        }

class NewBlogForm(ModelForm):
    class Meta:
        model = Blogg
        fields = ['user_id', 'blog_name']
        widgets = {
            'user_id': HiddenInput()
        }

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['user_id', 'blog_id', 'headline', 'text']
        widgets = {
            'user_id': HiddenInput,
            'blog_id': HiddenInput
        }
        
class EditPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['headline', 'text']


# class NewUserForm(ModelForm):
    # class Meta:
        # model = User
        # fields = ['username', 'password', 'email', 'first_name', 'last_name']
       
class NewUserForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=250)
    
    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username)
        user.set_password(password)
        user.save()
        return user