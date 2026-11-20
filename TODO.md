# Task: Add user registration with roles (customer, admin/operator, farmer)

## Information Gathered
- Custom UserProfile model (phone, farm_name etc.).
- Registration template exists (`templates/django_registration/registration_form.html`).
- `django_registration` commented in settings.
- Roles to implement via Django Groups.

## Plan
1. Enable django_registration in settings.
2. Create groups: customer, operator, farmer, admin.
3. Custom registration form to assign role.
4. Add /register/ link in login template.
5. Sample users.

## Steps:
- [ ] 1. Add 'django_registration' to INSTALLED_APPS in LearningDjango/settings.py.
- [ ] 2. Uncomment django_registration urls in LearningDjango/urls.py.
- [ ] 3. Create groups and sample users.
- [ ] 4. Update login template to link register.
- [ ] 5. Test.

