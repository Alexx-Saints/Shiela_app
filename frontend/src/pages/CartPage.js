import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API, AuthContext } from '@/App';
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Trash2, ShoppingBag, ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';

const CartPage = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [cart, setCart] = useState(null);
  const [cartDetails, setCartDetails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [checkoutLoading, setCheckoutLoading] = useState(false);

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await axios.get(`${API}/cart`);
      setCart(response.data);
      
      // Fetch product details for each item
      const details = await Promise.all(
        response.data.items.map(async (item) => {
          const productResponse = await axios.get(`${API}/products/${item.product_id}`);
          return { ...productResponse.data, quantity: item.quantity };
        })
      );
      setCartDetails(details);
    } catch (error) {
      console.error('Failed to fetch cart', error);
      toast.error('Failed to load cart');
    } finally {
      setLoading(false);
    }
  };

  const removeItem = async (productId) => {
    try {
      await axios.delete(`${API}/cart/items/${productId}`);
      toast.success('Item removed from cart');
      fetchCart();
    } catch (error) {
      toast.error('Failed to remove item');
    }
  };

  const updateQuantity = async (productId, newQuantity) => {
    if (newQuantity < 1) return;
    
    try {
      await axios.post(`${API}/cart/items`, { product_id: productId, quantity: newQuantity });
      fetchCart();
    } catch (error) {
      toast.error('Failed to update quantity');
    }
  };

  const handleCheckout = async () => {
    setCheckoutLoading(true);
    try {
      // Create order
      const orderResponse = await axios.post(`${API}/orders`);
      const order = orderResponse.data;

      // Create checkout session
      const checkoutResponse = await axios.post(`${API}/checkout`, {
        order_id: order.id,
        origin_url: window.location.origin
      });

      // Redirect to Stripe
      window.location.href = checkoutResponse.data.url;
    } catch (error) {
      console.error('Checkout failed', error);
      toast.error(error.response?.data?.detail || 'Checkout failed');
      setCheckoutLoading(false);
    }
  };

  const calculateTotal = () => {
    return cartDetails.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  };

  if (loading) {
    return (
      <div className="min-h-screen">
        <Navbar />
        <div className="pt-24 flex items-center justify-center">
          <div className="text-xl">Loading cart...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <div className="pt-24 pb-20 px-4" data-testid="cart-page">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <Button
            variant="ghost"
            onClick={() => navigate('/products')}
            className="mb-6"
            data-testid="back-button"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Continue Shopping
          </Button>

          <h1 className="text-4xl font-bold mb-8" data-testid="page-title">
            Shopping <span className="gradient-text">Cart</span>
          </h1>

          {cartDetails.length === 0 ? (
            <div className="text-center py-20 glass-effect rounded-2xl" data-testid="empty-cart">
              <ShoppingBag className="w-16 h-16 mx-auto mb-4 text-slate-400" />
              <p className="text-xl text-slate-600 mb-6">Your cart is empty</p>
              <Button
                onClick={() => navigate('/products')}
                className="bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600"
                data-testid="shop-now-button"
              >
                Start Shopping
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Cart Items */}
              <div className="lg:col-span-2 space-y-4" data-testid="cart-items">
                {cartDetails.map((item) => (
                  <div
                    key={item.id}
                    className="glass-effect rounded-2xl p-6 flex items-center space-x-6"
                    data-testid={`cart-item-${item.id}`}
                  >
                    <img
                      src={item.image_url}
                      alt={item.name}
                      className="w-24 h-24 object-cover rounded-xl"
                      data-testid={`item-image-${item.id}`}
                    />
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg mb-1" data-testid={`item-name-${item.id}`}>{item.name}</h3>
                      <p className="text-slate-600 mb-2">{item.brand}</p>
                      <p className="text-2xl font-bold gradient-text" data-testid={`item-price-${item.id}`}>
                        ₱{item.price.toFixed(2)}
                      </p>
                    </div>
                    <div className="flex items-center space-x-3">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        data-testid={`decrease-qty-${item.id}`}
                      >
                        -
                      </Button>
                      <span className="w-12 text-center font-semibold" data-testid={`item-quantity-${item.id}`}>
                        {item.quantity}
                      </span>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        disabled={item.quantity >= item.stock}
                        data-testid={`increase-qty-${item.id}`}
                      >
                        +
                      </Button>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeItem(item.id)}
                      className="text-red-500 hover:text-red-700 hover:bg-red-50"
                      data-testid={`remove-item-${item.id}`}
                    >
                      <Trash2 className="w-5 h-5" />
                    </Button>
                  </div>
                ))}
              </div>

              {/* Order Summary */}
              <div className="lg:col-span-1">
                <div className="glass-effect rounded-2xl p-6 sticky top-24" data-testid="order-summary">
                  <h2 className="text-2xl font-bold mb-6">Order Summary</h2>
                  
                  <div className="space-y-3 mb-6">
                    <div className="flex justify-between text-slate-600">
                      <span>Subtotal</span>
                      <span data-testid="subtotal">₱{calculateTotal().toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between text-slate-600">
                      <span>Shipping</span>
                      <span className="text-green-600 font-medium">FREE</span>
                    </div>
                    <div className="border-t pt-3 flex justify-between text-xl font-bold">
                      <span>Total</span>
                      <span className="gradient-text" data-testid="total">₱{calculateTotal().toFixed(2)}</span>
                    </div>
                  </div>

                  <Button
                    onClick={handleCheckout}
                    disabled={checkoutLoading}
                    className="w-full py-6 text-lg bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600"
                    data-testid="checkout-button"
                  >
                    {checkoutLoading ? 'Processing...' : 'Proceed to Checkout'}
                  </Button>

                  <p className="text-sm text-slate-500 text-center mt-4">
                    Secure checkout powered by Stripe
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CartPage;