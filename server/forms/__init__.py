from .auth_forms import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm
from .visitors_forms import ContactForm, SubscriptionForm
from .mail_forms import NewsletterForm
from .posts_forms import NewPostForm, EditPostForm
from .tags_forms import TagForm, PostTagsForm

__all__ = [
    'LoginForm',
    'RegistrationForm',
    'ForgotPasswordForm',
    'ResetPasswordForm',
    'ContactForm',
    'SubscriptionForm',
    'NewsletterForm',
    'NewPostForm',
    'EditPostForm',
    'TagForm',
    'PostTagsForm'
]