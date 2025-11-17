import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API, AuthContext } from '@/App';
import Navbar from '@/components/Navbar';
import AuthModal from '@/components/AuthModal';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Star, ShoppingCart, Package, Shield, ArrowLeft } from 'lucide-react';
import { toast } from 'sonner';

const ProductDetailPage = () => {
  const { id } = useParams();
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [reviewForm, setReviewForm] = useState({ rating: 5, comment: '' });

  useEffect(() => {
    fetchProduct();
    fetchReviews();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await axios.get(`${API}/products/${id}`);
      setProduct(response.data);
    } catch (error) {
      console.error('Failed to fetch product', error);
      toast.error('Product not found');
      navigate('/products');
    } finally {
      setLoading(false);
    }
  };

  const fetchReviews = async () => {
    try {
      const response = await axios.get(`${API}/reviews/${id}`);
      setReviews(response.data);
    } catch (error) {
      console.error('Failed to fetch reviews', error);
    }
  };

  const addToCart = async () => {
    if (!user) {
      setShowAuthModal(true);
      return;
    }

    try {
      await axios.post(`${API}/cart/items`, { product_id: id, quantity });
      toast.success('Added to cart!');
      navigate('/cart');
    } catch (error) {
      toast.error('Failed to add to cart');
    }
  };

  const submitReview = async (e) => {
    e.preventDefault();
    if (!user) {
      setShowAuthModal(true);
      return;
    }

    try {
      await axios.post(`${API}/reviews`, {
        product_id: id,
        rating: reviewForm.rating,
        comment: reviewForm.comment
      });
      toast.success('Review submitted!');
      setShowReviewForm(false);
      setReviewForm({ rating: 5, comment: '' });
      fetchReviews();
      fetchProduct();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to submit review');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen">
        <Navbar onAuthClick={() => setShowAuthModal(true)} />
        <div className="pt-24 flex items-center justify-center">
          <div className="text-xl">Loading...</div>
        </div>
      </div>
    );
  }

  if (!product) return null;

  return (
    <div className="min-h-screen">
      <Navbar onAuthClick={() => setShowAuthModal(true)} />
      
      <div className="pt-24 pb-20 px-4" data-testid="product-detail-page">
        <div className="max-w-7xl mx-auto">
          {/* Back Button */}
          <Button
            variant="ghost"
            onClick={() => navigate('/products')}
            className="mb-6"
            data-testid="back-button"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Products
          </Button>

          {/* Product Details */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-12">
            {/* Image */}
            <div className="glass-effect rounded-2xl overflow-hidden p-8">
              <img
                src={product.image_url}
                alt={product.name}
                className="w-full h-96 object-contain"
                data-testid="product-image"
              />
            </div>

            {/* Info */}
            <div>
              <h1 className="text-4xl font-bold mb-2" data-testid="product-name">{product.name}</h1>
              <p className="text-lg text-slate-600 mb-4">{product.brand}</p>
              
              <div className="flex items-center mb-6">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`w-5 h-5 ${i < Math.floor(product.rating) ? 'fill-yellow-400 text-yellow-400' : 'text-slate-300'}`}
                    />
                  ))}
                </div>
                <span className="ml-2 text-lg font-medium">{product.rating.toFixed(1)}</span>
                <span className="ml-2 text-slate-600">({product.reviews_count} reviews)</span>
              </div>

              <div className="mb-6">
                <span className="text-5xl font-bold gradient-text" data-testid="product-price">
                  ${product.price.toFixed(2)}
                </span>
              </div>

              <p className="text-slate-700 mb-6" data-testid="product-description">{product.description}</p>

              {/* Features */}
              {product.features && product.features.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-xl font-semibold mb-3">Key Features</h3>
                  <ul className="space-y-2">
                    {product.features.map((feature, index) => (
                      <li key={index} className="flex items-start">
                        <Package className="w-5 h-5 text-sky-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Stock */}
              <div className="mb-6">
                {product.stock > 0 ? (
                  <span className="inline-flex items-center px-3 py-1 rounded-full bg-green-100 text-green-800 text-sm font-medium">
                    <Shield className="w-4 h-4 mr-1" />
                    In Stock ({product.stock} available)
                  </span>
                ) : (
                  <span className="inline-flex items-center px-3 py-1 rounded-full bg-red-100 text-red-800 text-sm font-medium">
                    Out of Stock
                  </span>
                )}
              </div>

              {/* Quantity & Add to Cart */}
              <div className="flex items-center space-x-4 mb-6">
                <div>
                  <Label>Quantity</Label>
                  <div className="flex items-center space-x-2 mt-2">
                    <Button
                      variant="outline"
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      data-testid="decrease-quantity"
                    >
                      -
                    </Button>
                    <span className="w-12 text-center font-semibold" data-testid="quantity-display">{quantity}</span>
                    <Button
                      variant="outline"
                      onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                      disabled={quantity >= product.stock}
                      data-testid="increase-quantity"
                    >
                      +
                    </Button>
                  </div>
                </div>
              </div>

              <Button
                onClick={addToCart}
                disabled={product.stock === 0}
                className="w-full py-6 text-lg bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600 disabled:opacity-50"
                data-testid="add-to-cart-button"
              >
                <ShoppingCart className="w-5 h-5 mr-2" />
                {product.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
              </Button>
            </div>
          </div>

          {/* Reviews Section */}
          <div className="glass-effect rounded-2xl p-8" data-testid="reviews-section">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-3xl font-bold">Customer Reviews</h2>
              {user && (
                <Button
                  onClick={() => setShowReviewForm(!showReviewForm)}
                  variant="outline"
                  data-testid="write-review-button"
                >
                  Write a Review
                </Button>
              )}
            </div>

            {/* Review Form */}
            {showReviewForm && (
              <form onSubmit={submitReview} className="mb-8 p-6 bg-white rounded-xl" data-testid="review-form">
                <div className="mb-4">
                  <Label>Rating</Label>
                  <div className="flex space-x-2 mt-2">
                    {[1, 2, 3, 4, 5].map((rating) => (
                      <button
                        key={rating}
                        type="button"
                        onClick={() => setReviewForm({ ...reviewForm, rating })}
                        data-testid={`rating-star-${rating}`}
                      >
                        <Star
                          className={`w-8 h-8 cursor-pointer ${rating <= reviewForm.rating ? 'fill-yellow-400 text-yellow-400' : 'text-slate-300'}`}
                        />
                      </button>
                    ))}
                  </div>
                </div>
                <div className="mb-4">
                  <Label>Comment</Label>
                  <Textarea
                    value={reviewForm.comment}
                    onChange={(e) => setReviewForm({ ...reviewForm, comment: e.target.value })}
                    placeholder="Share your experience with this product..."
                    rows={4}
                    required
                    data-testid="review-comment-input"
                  />
                </div>
                <Button
                  type="submit"
                  className="bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600"
                  data-testid="submit-review-button"
                >
                  Submit Review
                </Button>
              </form>
            )}

            {/* Reviews List */}
            <div className="space-y-6">
              {reviews.length === 0 ? (
                <p className="text-center text-slate-600" data-testid="no-reviews">No reviews yet. Be the first to review!</p>
              ) : (
                reviews.map((review) => (
                  <div key={review.id} className="p-6 bg-white rounded-xl" data-testid={`review-${review.id}`}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold">{review.user_name}</span>
                      <div className="flex items-center">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`w-4 h-4 ${i < review.rating ? 'fill-yellow-400 text-yellow-400' : 'text-slate-300'}`}
                          />
                        ))}
                      </div>
                    </div>
                    <p className="text-slate-700">{review.comment}</p>
                    <p className="text-sm text-slate-500 mt-2">
                      {new Date(review.created_at).toLocaleDateString()}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {showAuthModal && <AuthModal onClose={() => setShowAuthModal(false)} />}
    </div>
  );
};

export default ProductDetailPage;