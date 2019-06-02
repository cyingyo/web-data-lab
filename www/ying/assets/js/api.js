let api = {
    login: '/api/account/login',

    cart: {
        purchase: '/api/order', // POST
        list: '/api/cart/list', // GET
        addNew: '/api/cart/',   // POST {bookId}
    },

    book: {
        listStock: '/api/book/stock',       // GET
        listPre: '/api/book/pre',           // GET
        one: '/api/book/',                  // GET
        listKeyStock: '/api/book/stock/',   // GET
        listKeyPre: '/api/book/pre/',       // GET
    },

    order: {
        purchase: '/api/order/pay/',    // PUT
        list: '/api/order/list',        // GET
        refund: '/api/order/',          // PUT
        one: '/api/order/one/'          // GET
    },

    admin: {
        account: {
            ban: '/api/admin/account/',             // PUT {userId}
            list: '/api/admin/account/list'         // GET
        },
        book: {
            list: '/api/admin/book/list',           // GET
            add: '/api/admin/book',                 // POST
            update: '/api/admin/book/',             // PUT {bookId}
            delete: '/api/admin/book/'              // DELETE {bookId}
        },
        order: {
            list: '/api/admin/order/list',          // GET
        }
    }
};
