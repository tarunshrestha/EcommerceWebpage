class Cart:
    def __init__(self, request):
        self.session = request.session

        # Get Session key if it exists
        cart = self.session.get('session_key')

        # If the user is new no session key.
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure the cart is a Availabe on all pages
        self.cart = cart