from django.conf import settings
from panel.models import Theme


def site_settings(request):
    # Create a dictionary to hold all settings attributes
    context = {}

    # Iterate through all attributes of settings
    for attr in dir(settings):
        # Skip private or special attributes (those starting with '_')
        if not attr.startswith('_'):
            context[attr] = getattr(settings, attr)

    return context

def site_theme(request):
    # Default to the first theme marked as default
    default_theme = Theme.objects.filter(default=True).first()

    if request.user.is_authenticated:
        # Try to get the user's default theme if authenticated
        user_profile = getattr(request.user, 'profile', None)
        if user_profile and user_profile.default_theme:
            theme = user_profile.default_theme
        else:
            theme = default_theme
    else:
        # Use the default theme if the user is not authenticated
        theme = default_theme

    return {
        'THEME': theme
    }