# from django.test.runner import DiscoverRunner
# from chat.models.langchat import *
# from chat.models.langgeneral import *
# from django.db import connection

# class ManagedModelTestRunner(DiscoverRunner):
#     """
#     Test runner that automatically makes all unmanaged models in your Django
#     project managed for the duration of the test run, so that one doesn't need
#     to execute the SQL manually to create them.
#     """
#     def setup_databases(self, **kwargs):
#       databases = super().setup_databases(**kwargs)
#       return 
#     def setup_test_environment(self, *args, **kwargs):
#         hello = connection.cursor()
        
#         from django.apps import apps
#         # Import all models before  

#         chat_app_config = apps.get_app_config("chat")
        
#         self.unmanaged_models = [m for m in chat_app_config.get_models()
#                                  if not m._meta.managed]
#         for m in self.unmanaged_models:
#             print("Model {}".format(m))
            
#             m._meta.managed = True
#         super(ManagedModelTestRunner, self).setup_test_environment(*args,
#                                                                    **kwargs)

#     def teardown_test_environment(self, *args, **kwargs):
#         super(ManagedModelTestRunner, self).teardown_test_environment(*args,
#                                                                       **kwargs)
#         # reset unmanaged models
#         for m in self.unmanaged_models:
#             m._meta.managed = False