from chat.models.langchat import LangChatModels
from chat.models.langgeneral import LangGeneralModels

class ChatRouter:
    route_app_label = 'chat'
    chat_model_collections = [LangChatModels, LangGeneralModels]
    def db_for_read(self, model, **hints):
        if model._meta.app_label != ChatRouter.route_app_label:
          return None
        for model_collection in ChatRouter.chat_model_collections:
            if model.__name__ in model_collection.models:
                return model_collection.db_name
        return None


    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label != ChatRouter.route_app_label:
          return None
        for model_collection in ChatRouter.chat_model_collections:
            if model.__name__ in model_collection.models:
                return model_collection.db_name
        return None
    
    def is_same_db(self, model1, model2):
      for model_collection in ChatRouter.chat_model_collections:
        if model1.__name__ in model_collection.models and model2.__name__ in model_collection.models:
            return True
      return False
    

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if obj1._meta.app_label != ChatRouter.route_app_label or obj2._meta.app_label != ChatRouter.route_app_label:
          return None
        
        # Check if two models is in the same database
        if self.is_same_db(obj1, obj2):
          return True
        
        return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        return None