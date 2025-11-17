import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API } from '@/App';
import Navbar from '@/components/Navbar';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Plus, Edit, Trash2, Package, DollarSign } from 'lucide-react';
import { toast } from 'sonner';

const AdminPage = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [showProductModal, setShowProductModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [productForm, setProductForm] = useState({
    name: '',
    description: '',
    price: '',
    category: '',
    image_url: '',
    brand: '',
    stock: '',
    features: ''
  });

  useEffect(() => {
    fetchProducts();
    fetchOrders();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API}/products`);
      setProducts(response.data);
    } catch (error) {
      console.error('Failed to fetch products', error);
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await axios.get(`${API}/admin/orders`);
      setOrders(response.data);
    } catch (error) {
      console.error('Failed to fetch orders', error);
    }
  };

  const handleProductSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = {
        ...productForm,
        price: parseFloat(productForm.price),
        stock: parseInt(productForm.stock),
        features: productForm.features.split('\n').filter(f => f.trim())
      };

      if (editingProduct) {
        await axios.put(`${API}/products/${editingProduct.id}`, formData);
        toast.success('Product updated successfully');
      } else {
        await axios.post(`${API}/products`, formData);
        toast.success('Product created successfully');
      }

      setShowProductModal(false);
      setEditingProduct(null);
      resetProductForm();
      fetchProducts();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to save product');
    }
  };

  const handleDeleteProduct = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return;

    try {
      await axios.delete(`${API}/products/${productId}`);
      toast.success('Product deleted successfully');
      fetchProducts();
    } catch (error) {
      toast.error('Failed to delete product');
    }
  };

  const handleEditProduct = (product) => {
    setEditingProduct(product);
    setProductForm({
      name: product.name,
      description: product.description,
      price: product.price.toString(),
      category: product.category,
      image_url: product.image_url,
      brand: product.brand,
      stock: product.stock.toString(),
      features: product.features.join('\n')
    });
    setShowProductModal(true);
  };

  const resetProductForm = () => {
    setProductForm({
      name: '',
      description: '',
      price: '',
      category: '',
      image_url: '',
      brand: '',
      stock: '',
      features: ''
    });
  };

  const updateOrderStatus = async (orderId, status) => {
    try {
      await axios.patch(`${API}/admin/orders/${orderId}?status=${status}`);
      toast.success('Order status updated');
      fetchOrders();
    } catch (error) {
      toast.error('Failed to update order status');
    }
  };

  const calculateStats = () => {
    const totalRevenue = orders
      .filter(o => o.payment_status === 'paid')
      .reduce((sum, o) => sum + o.total_amount, 0);
    const totalOrders = orders.length;
    const pendingOrders = orders.filter(o => o.status === 'pending').length;

    return { totalRevenue, totalOrders, pendingOrders };
  };

  const stats = calculateStats();

  return (
    <div className="min-h-screen">
      <Navbar />
      
      <div className="pt-24 pb-20 px-4" data-testid="admin-page">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl font-bold mb-8" data-testid="page-title">
            Admin <span className="gradient-text">Dashboard</span>
          </h1>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="glass-effect rounded-2xl p-6" data-testid="revenue-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-600 mb-1">Total Revenue</p>
                  <p className="text-3xl font-bold gradient-text" data-testid="total-revenue">
                    ${stats.totalRevenue.toFixed(2)}
                  </p>
                </div>
                <DollarSign className="w-12 h-12 text-sky-500" />
              </div>
            </div>
            <div className="glass-effect rounded-2xl p-6" data-testid="orders-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-600 mb-1">Total Orders</p>
                  <p className="text-3xl font-bold gradient-text" data-testid="total-orders">
                    {stats.totalOrders}
                  </p>
                </div>
                <Package className="w-12 h-12 text-sky-500" />
              </div>
            </div>
            <div className="glass-effect rounded-2xl p-6" data-testid="pending-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-600 mb-1">Pending Orders</p>
                  <p className="text-3xl font-bold gradient-text" data-testid="pending-orders">
                    {stats.pendingOrders}
                  </p>
                </div>
                <Package className="w-12 h-12 text-yellow-500" />
              </div>
            </div>
          </div>

          {/* Tabs */}
          <Tabs defaultValue="products" className="space-y-6">
            <TabsList>
              <TabsTrigger value="products" data-testid="products-tab">Products</TabsTrigger>
              <TabsTrigger value="orders" data-testid="orders-tab">Orders</TabsTrigger>
            </TabsList>

            {/* Products Tab */}
            <TabsContent value="products" data-testid="products-content">
              <div className="glass-effect rounded-2xl p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold">Products</h2>
                  <Button
                    onClick={() => {
                      setEditingProduct(null);
                      resetProductForm();
                      setShowProductModal(true);
                    }}
                    className="bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600"
                    data-testid="add-product-button"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Product
                  </Button>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full" data-testid="products-table">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left py-3 px-4">Product</th>
                        <th className="text-left py-3 px-4">Category</th>
                        <th className="text-left py-3 px-4">Price</th>
                        <th className="text-left py-3 px-4">Stock</th>
                        <th className="text-right py-3 px-4">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {products.map((product) => (
                        <tr key={product.id} className="border-b" data-testid={`product-row-${product.id}`}>
                          <td className="py-3 px-4">
                            <div className="flex items-center space-x-3">
                              <img
                                src={product.image_url}
                                alt={product.name}
                                className="w-12 h-12 object-cover rounded-lg"
                              />
                              <div>
                                <p className="font-medium">{product.name}</p>
                                <p className="text-sm text-slate-600">{product.brand}</p>
                              </div>
                            </div>
                          </td>
                          <td className="py-3 px-4">{product.category}</td>
                          <td className="py-3 px-4 font-semibold">${product.price.toFixed(2)}</td>
                          <td className="py-3 px-4">
                            <span className={`px-2 py-1 rounded-full text-sm ${
                              product.stock > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}>
                              {product.stock}
                            </span>
                          </td>
                          <td className="py-3 px-4">
                            <div className="flex items-center justify-end space-x-2">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleEditProduct(product)}
                                data-testid={`edit-product-${product.id}`}
                              >
                                <Edit className="w-4 h-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleDeleteProduct(product.id)}
                                className="text-red-500 hover:text-red-700"
                                data-testid={`delete-product-${product.id}`}
                              >
                                <Trash2 className="w-4 h-4" />
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </TabsContent>

            {/* Orders Tab */}
            <TabsContent value="orders" data-testid="orders-content">
              <div className="glass-effect rounded-2xl p-6">
                <h2 className="text-2xl font-bold mb-6">Orders</h2>
                <div className="space-y-4" data-testid="orders-list">
                  {orders.map((order) => (
                    <div key={order.id} className="border rounded-xl p-4" data-testid={`order-${order.id}`}>
                      <div className="flex items-center justify-between mb-3">
                        <div>
                          <span className="font-mono text-sm" data-testid={`order-id-${order.id}`}>
                            {order.id.substring(0, 8).toUpperCase()}
                          </span>
                          <span className="text-sm text-slate-600 ml-3">
                            {new Date(order.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        <div className="flex items-center space-x-4">
                          <span className="font-bold" data-testid={`order-total-${order.id}`}>
                            ${order.total_amount.toFixed(2)}
                          </span>
                          <Select
                            value={order.status}
                            onValueChange={(status) => updateOrderStatus(order.id, status)}
                          >
                            <SelectTrigger className="w-32" data-testid={`status-select-${order.id}`}>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="pending">Pending</SelectItem>
                              <SelectItem value="processing">Processing</SelectItem>
                              <SelectItem value="shipped">Shipped</SelectItem>
                              <SelectItem value="delivered">Delivered</SelectItem>
                              <SelectItem value="cancelled">Cancelled</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                      <div className="text-sm text-slate-600">
                        {order.items.length} item(s) • Payment: {order.payment_status}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>

      {/* Product Modal */}
      {showProductModal && (
        <Dialog open={showProductModal} onOpenChange={setShowProductModal}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto" data-testid="product-modal">
            <DialogHeader>
              <DialogTitle>{editingProduct ? 'Edit Product' : 'Add New Product'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleProductSubmit} className="space-y-4" data-testid="product-form">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Product Name</Label>
                  <Input
                    value={productForm.name}
                    onChange={(e) => setProductForm({ ...productForm, name: e.target.value })}
                    required
                    data-testid="product-name-input"
                  />
                </div>
                <div>
                  <Label>Brand</Label>
                  <Input
                    value={productForm.brand}
                    onChange={(e) => setProductForm({ ...productForm, brand: e.target.value })}
                    required
                    data-testid="product-brand-input"
                  />
                </div>
              </div>
              <div>
                <Label>Description</Label>
                <Textarea
                  value={productForm.description}
                  onChange={(e) => setProductForm({ ...productForm, description: e.target.value })}
                  required
                  data-testid="product-description-input"
                />
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label>Price ($)</Label>
                  <Input
                    type="number"
                    step="0.01"
                    value={productForm.price}
                    onChange={(e) => setProductForm({ ...productForm, price: e.target.value })}
                    required
                    data-testid="product-price-input"
                  />
                </div>
                <div>
                  <Label>Stock</Label>
                  <Input
                    type="number"
                    value={productForm.stock}
                    onChange={(e) => setProductForm({ ...productForm, stock: e.target.value })}
                    required
                    data-testid="product-stock-input"
                  />
                </div>
                <div>
                  <Label>Category</Label>
                  <Input
                    value={productForm.category}
                    onChange={(e) => setProductForm({ ...productForm, category: e.target.value })}
                    required
                    data-testid="product-category-input"
                  />
                </div>
              </div>
              <div>
                <Label>Image URL</Label>
                <Input
                  type="url"
                  value={productForm.image_url}
                  onChange={(e) => setProductForm({ ...productForm, image_url: e.target.value })}
                  required
                  data-testid="product-image-input"
                />
              </div>
              <div>
                <Label>Features (one per line)</Label>
                <Textarea
                  value={productForm.features}
                  onChange={(e) => setProductForm({ ...productForm, features: e.target.value })}
                  rows={4}
                  placeholder="Feature 1&#10;Feature 2&#10;Feature 3"
                  data-testid="product-features-input"
                />
              </div>
              <div className="flex space-x-4">
                <Button
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600"
                  data-testid="save-product-button"
                >
                  {editingProduct ? 'Update Product' : 'Create Product'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    setShowProductModal(false);
                    setEditingProduct(null);
                    resetProductForm();
                  }}
                  data-testid="cancel-button"
                >
                  Cancel
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      )}
    </div>
  );
};

export default AdminPage;