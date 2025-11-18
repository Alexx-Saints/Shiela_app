import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { API } from '@/App';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Lock, CreditCard, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';

const MockCheckoutPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('order_id');
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  
  const [cardDetails, setCardDetails] = useState({
    cardNumber: '',
    expiry: '',
    cvc: '',
    name: '',
    email: ''
  });

  useEffect(() => {
    if (orderId) {
      fetchOrder();
    } else {
      navigate('/cart');
    }
  }, [orderId]);

  const fetchOrder = async () => {
    try {
      const response = await axios.get(`${API}/orders/${orderId}`);
      setOrder(response.data);
    } catch (error) {
      console.error('Failed to fetch order', error);
      toast.error('Invalid order');
      navigate('/cart');
    } finally {
      setLoading(false);
    }
  };

  const formatCardNumber = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = (matches && matches[0]) || '';
    const parts = [];

    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }

    if (parts.length) {
      return parts.join(' ');
    } else {
      return value;
    }
  };

  const formatExpiry = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    if (v.length >= 2) {
      return v.slice(0, 2) + ' / ' + v.slice(2, 4);
    }
    return v;
  };

  const handleCardNumberChange = (e) => {
    const formatted = formatCardNumber(e.target.value);
    setCardDetails({ ...cardDetails, cardNumber: formatted });
  };

  const handleExpiryChange = (e) => {
    const formatted = formatExpiry(e.target.value);
    setCardDetails({ ...cardDetails, expiry: formatted });
  };

  const handleCvcChange = (e) => {
    const value = e.target.value.replace(/[^0-9]/gi, '').slice(0, 3);
    setCardDetails({ ...cardDetails, cvc: value });
  };

  const handlePayment = async (e) => {
    e.preventDefault();
    
    // Validate
    if (cardDetails.cardNumber.replace(/\s/g, '').length < 15) {
      toast.error('Invalid card number');
      return;
    }
    if (!cardDetails.expiry.includes('/')) {
      toast.error('Invalid expiry date');
      return;
    }
    if (cardDetails.cvc.length < 3) {
      toast.error('Invalid CVC');
      return;
    }

    setProcessing(true);
    
    // Simulate payment processing
    setTimeout(async () => {
      try {
        // Update order to paid status
        await axios.patch(`${API}/orders/${orderId}/mock-payment`, {
          payment_method: 'Mock Card',
          last4: cardDetails.cardNumber.slice(-4)
        });
        
        toast.success('Payment successful!');
        navigate(`/order-success?mock=true&order_id=${orderId}`);
      } catch (error) {
        console.error('Payment failed', error);
        toast.error('Payment failed. Please try again.');
        setProcessing(false);
      }
    }, 2000);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  if (!order) return null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12 px-4" data-testid="mock-checkout-page">
      <div className="max-w-5xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          {/* Payment Form */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              {/* Header */}
              <div className="flex items-center justify-between mb-8 pb-6 border-b">
                <h1 className="text-2xl font-bold">Secure Checkout</h1>
                <div className="flex items-center text-green-600">
                  <Lock className="w-5 h-5 mr-2" />
                  <span className="text-sm font-medium">Secured by SSL</span>
                </div>
              </div>

              {/* Form */}
              <form onSubmit={handlePayment}>
                {/* Email */}
                <div className="mb-6">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="customer@example.com"
                    value={cardDetails.email}
                    onChange={(e) => setCardDetails({ ...cardDetails, email: e.target.value })}
                    required
                    className="mt-2"
                    data-testid="email-input"
                  />
                </div>

                {/* Card Information */}
                <div className="mb-6">
                  <Label>Card Information</Label>
                  <div className="mt-2 border rounded-lg overflow-hidden">
                    <div className="relative">
                      <CreditCard className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
                      <Input
                        type="text"
                        placeholder="1234 1234 1234 1234"
                        value={cardDetails.cardNumber}
                        onChange={handleCardNumberChange}
                        maxLength={19}
                        required
                        className="pl-10 border-0 border-b rounded-none"
                        data-testid="card-number-input"
                      />
                    </div>
                    <div className="grid grid-cols-2">
                      <Input
                        type="text"
                        placeholder="MM / YY"
                        value={cardDetails.expiry}
                        onChange={handleExpiryChange}
                        maxLength={7}
                        required
                        className="border-0 border-r rounded-none"
                        data-testid="expiry-input"
                      />
                      <Input
                        type="text"
                        placeholder="CVC"
                        value={cardDetails.cvc}
                        onChange={handleCvcChange}
                        maxLength={3}
                        required
                        className="border-0 rounded-none"
                        data-testid="cvc-input"
                      />
                    </div>
                  </div>
                  <p className="text-xs text-slate-500 mt-2">
                    Use any test card: 4242 4242 4242 4242
                  </p>
                </div>

                {/* Cardholder Name */}
                <div className="mb-6">
                  <Label htmlFor="name">Cardholder Name</Label>
                  <Input
                    id="name"
                    type="text"
                    placeholder="Full name on card"
                    value={cardDetails.name}
                    onChange={(e) => setCardDetails({ ...cardDetails, name: e.target.value })}
                    required
                    className="mt-2"
                    data-testid="name-input"
                  />
                </div>

                {/* Submit Button */}
                <Button
                  type="submit"
                  disabled={processing}
                  className="w-full py-6 text-lg font-semibold bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800"
                  data-testid="pay-button"
                >
                  {processing ? (
                    <span className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                      Processing...
                    </span>
                  ) : (
                    `Pay ₱${order.total_amount.toFixed(2)}`
                  )}
                </Button>
              </form>

              {/* Security Info */}
              <div className="mt-6 pt-6 border-t text-center text-sm text-slate-500">
                <p>Powered by <span className="font-semibold">ApplianceHub</span> Secure Payments</p>
                <p className="mt-2">Your payment information is encrypted and secure</p>
              </div>
            </div>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-2">
            <div className="bg-slate-50 rounded-2xl p-6 sticky top-6">
              <h2 className="text-xl font-bold mb-6">Order Summary</h2>
              
              {/* Items */}
              <div className="space-y-4 mb-6">
                {order.items.map((item, index) => (
                  <div key={index} className="flex justify-between text-sm">
                    <div className="flex-1">
                      <p className="font-medium">{item.product_name}</p>
                      <p className="text-slate-500">Qty: {item.quantity}</p>
                    </div>
                    <span className="font-semibold">₱{(item.price * item.quantity).toFixed(2)}</span>
                  </div>
                ))}
              </div>

              {/* Totals */}
              <div className="border-t pt-4 space-y-3">
                <div className="flex justify-between text-sm">
                  <span>Subtotal</span>
                  <span>₱{order.total_amount.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Shipping</span>
                  <span className="text-green-600 font-semibold">FREE</span>
                </div>
                <div className="flex justify-between text-lg font-bold pt-3 border-t">
                  <span>Total</span>
                  <span className="text-blue-600">₱{order.total_amount.toFixed(2)}</span>
                </div>
              </div>

              {/* Trust Badges */}
              <div className="mt-6 pt-6 border-t">
                <div className="flex items-center justify-center space-x-4 text-slate-400">
                  <Lock className="w-5 h-5" />
                  <span className="text-xs">256-bit SSL Encrypted</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MockCheckoutPage;
