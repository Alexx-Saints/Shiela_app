import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { API } from '@/App';
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { CheckCircle, Package, Loader2, FileText } from 'lucide-react';
import { toast } from 'sonner';

const OrderSuccessPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');
  const [status, setStatus] = useState('checking');
  const [orderId, setOrderId] = useState(null);
  const [attempts, setAttempts] = useState(0);

  useEffect(() => {
    if (sessionId) {
      pollPaymentStatus();
    } else {
      navigate('/cart');
    }
  }, [sessionId]);

  const pollPaymentStatus = async () => {
    const maxAttempts = 5;
    const pollInterval = 2000;

    if (attempts >= maxAttempts) {
      setStatus('timeout');
      toast.error('Payment verification timed out. Please check your orders.');
      return;
    }

    try {
      const response = await axios.get(`${API}/checkout/status/${sessionId}`);
      
      if (response.data.payment_status === 'paid') {
        setStatus('success');
        setOrderId(response.data.order_id);
        toast.success('Payment successful!');
        return;
      } else if (response.data.status === 'expired') {
        setStatus('failed');
        toast.error('Payment session expired');
        return;
      }

      // Continue polling
      setAttempts(attempts + 1);
      setTimeout(pollPaymentStatus, pollInterval);
    } catch (error) {
      console.error('Error checking payment status:', error);
      setStatus('error');
      toast.error('Failed to verify payment');
    }
  };

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <div className="pt-24 pb-20 px-4" data-testid="order-success-page">
        <div className="max-w-2xl mx-auto">
          <div className="glass-effect rounded-3xl p-12 text-center">
            {status === 'checking' && (
              <div data-testid="payment-checking">
                <Loader2 className="w-16 h-16 mx-auto mb-6 text-sky-500 animate-spin" />
                <h1 className="text-3xl font-bold mb-4">Verifying Payment...</h1>
                <p className="text-slate-600">Please wait while we confirm your payment</p>
              </div>
            )}

            {status === 'success' && (
              <div data-testid="payment-success">
                <CheckCircle className="w-16 h-16 mx-auto mb-6 text-green-500" />
                <h1 className="text-3xl font-bold mb-4">Order Placed Successfully!</h1>
                <p className="text-slate-600 mb-8">
                  Thank you for your purchase. Your order has been confirmed and will be processed shortly.
                </p>
                <div className="space-y-4">
                  {orderId && (
                    <Button
                      onClick={() => navigate(`/receipt/${orderId}`)}
                      className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600"
                      data-testid="view-receipt-button"
                    >
                      <FileText className="w-5 h-5 mr-2" />
                      View Receipt
                    </Button>
                  )}
                  <Button
                    onClick={() => navigate(`/orders`)}
                    className="w-full bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600"
                    data-testid="view-orders-button"
                  >
                    <Package className="w-5 h-5 mr-2" />
                    View My Orders
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => navigate('/products')}
                    className="w-full"
                    data-testid="continue-shopping-button"
                  >
                    Continue Shopping
                  </Button>
                </div>
              </div>
            )}

            {(status === 'failed' || status === 'timeout' || status === 'error') && (
              <div data-testid="payment-failed">
                <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-red-100 flex items-center justify-center">
                  <span className="text-4xl">⚠️</span>
                </div>
                <h1 className="text-3xl font-bold mb-4">Payment Issue</h1>
                <p className="text-slate-600 mb-8">
                  {status === 'timeout'
                    ? 'Payment verification timed out. Please check your order history.'
                    : 'There was an issue processing your payment. Please try again or contact support.'}
                </p>
                <div className="space-y-4">
                  <Button
                    onClick={() => navigate('/orders')}
                    className="w-full bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600"
                    data-testid="check-orders-button"
                  >
                    Check My Orders
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => navigate('/cart')}
                    className="w-full"
                    data-testid="back-to-cart-button"
                  >
                    Back to Cart
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderSuccessPage;