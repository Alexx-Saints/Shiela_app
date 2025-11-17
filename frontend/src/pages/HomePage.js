import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '@/App';
import Navbar from '@/components/Navbar';
import AuthModal from '@/components/AuthModal';
import { Button } from '@/components/ui/button';
import { ShoppingCart, Zap, Shield, Truck } from 'lucide-react';

const HomePage = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [showAuthModal, setShowAuthModal] = useState(false);

  const features = [
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Fast Delivery',
      description: 'Get your appliances delivered within 24-48 hours'
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'Warranty Included',
      description: 'All products come with manufacturer warranty'
    },
    {
      icon: <Truck className="w-8 h-8" />,
      title: 'Free Installation',
      description: 'Professional installation service at no extra cost'
    }
  ];

  const categories = [
    { name: 'Refrigerators', image: 'https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=500' },
    { name: 'Washing Machines', image: 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=500' },
    { name: 'Air Conditioners', image: 'https://images.unsplash.com/photo-1631545804641-2b0e18f3c28d?w=500' },
    { name: 'Microwaves', image: 'https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=500' }
  ];

  return (
    <div className="min-h-screen">
      <Navbar onAuthClick={() => setShowAuthModal(true)} />
      
      {/* Hero Section */}
      <section className="relative pt-24 pb-20 px-4 overflow-hidden" data-testid="hero-section">
        <div className="absolute inset-0 z-0">
          <div className="absolute top-20 left-20 w-72 h-72 bg-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-sky-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style={{animationDelay: '1s'}}></div>
        </div>
        
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="text-center mb-16">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6" data-testid="hero-title">
              Premium Home <span className="gradient-text">Appliances</span>
            </h1>
            <p className="text-lg sm:text-xl text-slate-600 mb-8 max-w-2xl mx-auto">
              Transform your home with cutting-edge appliances from the world's leading brands
            </p>
            <Button
              onClick={() => navigate('/products')}
              className="bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600 text-white px-8 py-6 text-lg rounded-full"
              data-testid="shop-now-button"
            >
              <ShoppingCart className="w-5 h-5 mr-2" />
              Shop Now
            </Button>
          </div>

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
            {features.map((feature, index) => (
              <div
                key={index}
                className="glass-effect rounded-2xl p-8 text-center smooth-transition hover:scale-105"
                data-testid={`feature-card-${index}`}
              >
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r from-sky-500 to-cyan-500 text-white mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-slate-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-20 px-4 bg-white/50" data-testid="categories-section">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">Shop by Category</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {categories.map((category, index) => (
              <div
                key={index}
                onClick={() => navigate(`/products?category=${category.name}`)}
                className="group relative h-64 rounded-2xl overflow-hidden cursor-pointer"
                data-testid={`category-card-${index}`}
              >
                <img
                  src={category.image}
                  alt={category.name}
                  className="w-full h-full object-cover group-hover:scale-110 smooth-transition"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent flex items-end p-6">
                  <h3 className="text-white text-2xl font-semibold">{category.name}</h3>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4" data-testid="cta-section">
        <div className="max-w-4xl mx-auto glass-effect rounded-3xl p-12 text-center">
          <h2 className="text-4xl font-bold mb-4">Ready to Upgrade Your Home?</h2>
          <p className="text-lg text-slate-600 mb-8">
            Browse our extensive collection of premium appliances and enjoy exclusive deals
          </p>
          {!user ? (
            <Button
              onClick={() => setShowAuthModal(true)}
              className="bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600 text-white px-8 py-6 text-lg rounded-full"
              data-testid="get-started-button"
            >
              Get Started
            </Button>
          ) : (
            <Button
              onClick={() => navigate('/products')}
              className="bg-gradient-to-r from-sky-500 to-cyan-500 hover:from-sky-600 hover:to-cyan-600 text-white px-8 py-6 text-lg rounded-full"
              data-testid="browse-products-button"
            >
              Browse Products
            </Button>
          )}
        </div>
      </section>

      {/* Auth Modal */}
      {showAuthModal && (
        <AuthModal onClose={() => setShowAuthModal(false)} />
      )}
    </div>
  );
};

export default HomePage;