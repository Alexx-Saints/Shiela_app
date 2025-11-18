import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API } from '@/App';
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Package, ArrowLeft, Clock, CheckCircle, XCircle } from 'lucide-react';
import { toast } from 'sonner';

const OrdersPage = () => {
  const navigate = useNavigate();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await axios.get(`${API}/orders`);
      setOrders(response.data);
    } catch (error) {
      console.error('Failed to fetch orders', error);
      toast.error('Failed to load orders');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending':
        return <Clock className="w-5 h-5 text-yellow-500" />;
      case 'processing':
      case 'shipped':
        return <Package className="w-5 h-5 text-blue-500" />;
      case 'delivered':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'cancelled':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'shipped':
        return 'bg-purple-100 text-purple-800';
      case 'delivered':
        return 'bg-green-100 text-green-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen">
        <Navbar />
        <div className="pt-24 flex items-center justify-center">
          <div className="text-xl">Loading orders...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <div className="pt-24 pb-20 px-4" data-testid="orders-page">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <Button
            variant="ghost"
            onClick={() => navigate('/')}
            className="mb-6"
            data-testid="back-button"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>

          <h1 className="text-4xl font-bold mb-8" data-testid="page-title">
            My <span className="gradient-text">Orders</span>
          </h1>

          {orders.length === 0 ? (
            <div className="text-center py-20 glass-effect rounded-2xl" data-testid="no-orders">
              <Package className="w-16 h-16 mx-auto mb-4 text-slate-400" />
              <p className="text-xl text-slate-600 mb-6">No orders yet</p>
              <Button
                onClick={() => navigate('/products')}
                className="bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600"
                data-testid="start-shopping-button"
              >
                Start Shopping
              </Button>
            </div>
          ) : (
            <div className="space-y-6" data-testid="orders-list">
              {orders.map((order) => (
                <div
                  key={order.id}
                  className="glass-effect rounded-2xl p-6"
                  data-testid={`order-${order.id}`}
                >
                  {/* Order Header */}
                  <div className="flex items-center justify-between mb-4 pb-4 border-b">
                    <div>
                      <div className="flex items-center space-x-3 mb-2">
                        <span className="text-sm text-slate-600">Order ID:</span>
                        <span className="font-mono text-sm" data-testid={`order-id-${order.id}`}>
                          {order.id.substring(0, 8).toUpperCase()}
                        </span>
                      </div>
                      <div className="text-sm text-slate-600">
                        {new Date(order.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="flex items-center space-x-2 mb-2">
                        {getStatusIcon(order.status)}
                        <span
                          className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}
                          data-testid={`order-status-${order.id}`}
                        >
                          {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                        </span>
                      </div>
                      <div className="text-sm">
                        <span className="text-slate-600">Payment: </span>
                        <span
                          className={`font-medium ${
                            order.payment_status === 'paid' ? 'text-green-600' : 'text-yellow-600'
                          }`}
                          data-testid={`payment-status-${order.id}`}
                        >
                          {order.payment_status.charAt(0).toUpperCase() + order.payment_status.slice(1)}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Order Items */}
                  <div className="space-y-3 mb-4">
                    {order.items.map((item, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between py-2"
                        data-testid={`order-item-${index}`}
                      >
                        <div className="flex-1">
                          <span className="font-medium">{item.product_name}</span>
                          <span className="text-slate-600 ml-2">× {item.quantity}</span>
                        </div>
                        <span className="font-semibold" data-testid={`item-price-${index}`}>
                          ₱{(item.price * item.quantity).toFixed(2)}
                        </span>
                      </div>
                    ))}
                  </div>

                  {/* Order Total */}
                  <div className="flex items-center justify-between pt-4 border-t">
                    <span className="text-lg font-semibold">Total</span>
                    <span className="text-2xl font-bold gradient-text" data-testid={`order-total-${order.id}`}>
                      ${order.total_amount.toFixed(2)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OrdersPage;