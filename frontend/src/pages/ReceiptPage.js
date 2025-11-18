import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API } from '@/App';
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Download, Mail, Printer, ArrowLeft, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';

const ReceiptPage = () => {
  const { orderId } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [emailSending, setEmailSending] = useState(false);

  useEffect(() => {
    fetchReceipt();
  }, [orderId]);

  const fetchReceipt = async () => {
    try {
      const response = await axios.get(`${API}/orders/${orderId}/receipt`);
      setOrder(response.data);
    } catch (error) {
      console.error('Failed to fetch receipt', error);
      toast.error('Failed to load receipt');
      navigate('/orders');
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async () => {
    try {
      const response = await axios.get(`${API}/orders/${orderId}/receipt/pdf`, {
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `receipt_${orderId.substring(0, 8)}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('Receipt downloaded!');
    } catch (error) {
      console.error('Failed to download PDF', error);
      toast.error('Failed to download receipt');
    }
  };

  const emailReceipt = async () => {
    setEmailSending(true);
    try {
      await axios.post(`${API}/orders/${orderId}/email-receipt`);
      toast.success('Receipt sent to your email!');
    } catch (error) {
      console.error('Failed to email receipt', error);
      toast.error('Failed to send email');
    } finally {
      setEmailSending(false);
    }
  };

  const printReceipt = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="min-h-screen">
        <Navbar />
        <div className="pt-24 flex items-center justify-center">
          <div className="text-xl">Loading receipt...</div>
        </div>
      </div>
    );
  }

  if (!order) return null;

  const orderDate = new Date(order.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <div className="pt-24 pb-20 px-4" data-testid="receipt-page">
        <div className="max-w-4xl mx-auto">
          {/* Action Buttons - Hide on print */}
          <div className="no-print mb-6 flex items-center justify-between">
            <Button
              variant="ghost"
              onClick={() => navigate('/orders')}
              data-testid="back-button"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Orders
            </Button>
            
            <div className="flex space-x-3">
              <Button
                variant="outline"
                onClick={printReceipt}
                data-testid="print-button"
              >
                <Printer className="w-4 h-4 mr-2" />
                Print
              </Button>
              <Button
                variant="outline"
                onClick={downloadPDF}
                data-testid="download-pdf-button"
              >
                <Download className="w-4 h-4 mr-2" />
                Download PDF
              </Button>
              <Button
                onClick={emailReceipt}
                disabled={emailSending}
                className="bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600"
                data-testid="email-button"
              >
                <Mail className="w-4 h-4 mr-2" />
                {emailSending ? 'Sending...' : 'Email Receipt'}
              </Button>
            </div>
          </div>

          {/* Receipt */}
          <div className="glass-effect rounded-3xl p-12" data-testid="receipt-content" id="receipt-content">
            {/* Header */}
            <div className="text-center border-b-4 border-sky-500 pb-6 mb-8">
              <h1 className="text-4xl font-bold gradient-text mb-2">ApplianceHub</h1>
              <h2 className="text-2xl font-semibold text-slate-600">ORDER RECEIPT</h2>
            </div>

            {/* Success Badge */}
            <div className="flex justify-center mb-8">
              <div className="inline-flex items-center px-6 py-3 rounded-full bg-green-100 text-green-800">
                <CheckCircle className="w-5 h-5 mr-2" />
                <span className="font-semibold">Payment Successful</span>
              </div>
            </div>

            {/* Order Info */}
            <div className="grid grid-cols-2 gap-6 mb-8 p-6 bg-slate-50 rounded-xl">
              <div>
                <p className="text-sm text-slate-600 mb-1">Order ID</p>
                <p className="font-mono font-bold" data-testid="receipt-order-id">
                  {order.id.substring(0, 8).toUpperCase()}
                </p>
              </div>
              <div>
                <p className="text-sm text-slate-600 mb-1">Order Date</p>
                <p className="font-semibold">{orderDate}</p>
              </div>
              <div>
                <p className="text-sm text-slate-600 mb-1">Payment Status</p>
                <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
                  order.payment_status === 'paid' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {order.payment_status.toUpperCase()}
                </span>
              </div>
              <div>
                <p className="text-sm text-slate-600 mb-1">Order Status</p>
                <span className="inline-block px-3 py-1 rounded-full text-sm font-semibold bg-blue-100 text-blue-800">
                  {order.status.toUpperCase()}
                </span>
              </div>
            </div>

            {/* Items Table */}
            <div className="mb-8">
              <h3 className="text-xl font-bold mb-4">Order Items</h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-gradient-to-r from-sky-500 to-cyan-500 text-white">
                      <th className="text-left py-4 px-4 rounded-tl-lg">Product</th>
                      <th className="text-center py-4 px-4">Quantity</th>
                      <th className="text-right py-4 px-4">Price</th>
                      <th className="text-right py-4 px-4 rounded-tr-lg">Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {order.items.map((item, index) => (
                      <tr key={index} className="border-b border-slate-200" data-testid={`receipt-item-${index}`}>
                        <td className="py-4 px-4 font-medium">{item.product_name}</td>
                        <td className="py-4 px-4 text-center">{item.quantity}</td>
                        <td className="py-4 px-4 text-right">₱{item.price.toFixed(2)}</td>
                        <td className="py-4 px-4 text-right font-semibold">
                          ₱{(item.price * item.quantity).toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Totals */}
            <div className="flex justify-end mb-8">
              <div className="w-80">
                <div className="flex justify-between py-3 text-slate-600">
                  <span>Subtotal</span>
                  <span data-testid="receipt-subtotal">₱{order.total_amount.toFixed(2)}</span>
                </div>
                <div className="flex justify-between py-3 text-slate-600">
                  <span>Shipping</span>
                  <span className="text-green-600 font-semibold">FREE</span>
                </div>
                <div className="border-t-2 border-sky-500 pt-4 mt-2">
                  <div className="flex justify-between text-2xl font-bold">
                    <span>TOTAL</span>
                    <span className="gradient-text" data-testid="receipt-total">
                      ₱{order.total_amount.toFixed(2)}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Footer */}
            <div className="text-center pt-8 border-t border-slate-200 text-slate-500 text-sm">
              <p className="mb-2">Thank you for shopping with ApplianceHub!</p>
              <p>For questions or support, please contact us at support@appliancehub.com</p>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @media print {
          .no-print {
            display: none !important;
          }
          
          body {
            print-color-adjust: exact;
            -webkit-print-color-adjust: exact;
          }
        }
      `}</style>
    </div>
  );
};

export default ReceiptPage;
