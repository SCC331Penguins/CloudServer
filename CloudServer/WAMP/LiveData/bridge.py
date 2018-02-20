
class Bridge():

    def __init__(self, router_id, user=None, router=None):
        self.user_client = user
        self.router_client = router
        self.router_id = router_id

    def get_router_id(self):
        return self.router_id

    def get_user_client(self):
        return self.user_client

    def get_router_client(self):
        return self.router

    def set_router_client(self, router):
        self.router = router

    def set_user_client(self, user):
        self.user_client = user