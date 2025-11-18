from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import jwt
from io import BytesIO
from fastapi.responses import StreamingResponse, Response
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# JWT settings
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 1440))

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# ============== MODELS ==============

# User Models
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    is_admin: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

# Product Models
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image_url: str
    brand: str
    stock: int = 0
    features: List[str] = []

class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: str
    image_url: str
    brand: str
    stock: int = 0
    features: List[str] = []
    rating: float = 0.0
    reviews_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Cart Models
class CartItem(BaseModel):
    product_id: str
    quantity: int

class Cart(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    items: List[CartItem] = []
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Order Models
class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float

class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"
    payment_status: str = "pending"
    session_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Review Models
class ReviewCreate(BaseModel):
    product_id: str
    rating: int
    comment: str

class Review(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    user_id: str
    user_name: str
    rating: int
    comment: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Payment Transaction Model
class PaymentTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    user_id: str
    order_id: str
    amount: float
    currency: str = "usd"
    payment_status: str = "pending"
    metadata: Dict = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ============== AUTH HELPERS ==============

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_data = await db.users.find_one({"id": user_id}, {"_id": 0})
        if user_data is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return User(**user_data)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# ============== AUTH ROUTES ==============

@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserRegister):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        name=user_data.name,
        email=user_data.email,
        is_admin=False
    )
    
    user_dict = user.model_dump()
    user_dict['password'] = hash_password(user_data.password)
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    
    await db.users.insert_one(user_dict)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.post("/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    # Find user
    user_data = await db.users.find_one({"email": credentials.email})
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(credentials.password, user_data['password']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    user = User(**{k: v for k, v in user_data.items() if k != 'password'})
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return Token(access_token=access_token, token_type="bearer", user=user)

@api_router.get("/auth/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# ============== PRODUCT ROUTES ==============

@api_router.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None, search: Optional[str] = None):
    query = {}
    if category:
        query['category'] = category
    if search:
        query['$or'] = [
            {'name': {'$regex': search, '$options': 'i'}},
            {'description': {'$regex': search, '$options': 'i'}},
            {'brand': {'$regex': search, '$options': 'i'}}
        ]
    
    products = await db.products.find(query, {"_id": 0}).to_list(1000)
    return products

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@api_router.post("/products", response_model=Product)
async def create_product(product_data: ProductCreate, admin: User = Depends(get_admin_user)):
    product = Product(**product_data.model_dump())
    product_dict = product.model_dump()
    product_dict['created_at'] = product_dict['created_at'].isoformat()
    
    await db.products.insert_one(product_dict)
    return product

@api_router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product_data: ProductCreate, admin: User = Depends(get_admin_user)):
    existing_product = await db.products.find_one({"id": product_id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_data.model_dump()
    await db.products.update_one({"id": product_id}, {"$set": update_data})
    
    updated_product = await db.products.find_one({"id": product_id}, {"_id": 0})
    return updated_product

@api_router.delete("/products/{product_id}")
async def delete_product(product_id: str, admin: User = Depends(get_admin_user)):
    result = await db.products.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@api_router.get("/categories")
async def get_categories():
    categories = await db.products.distinct("category")
    return {"categories": categories}

# ============== CART ROUTES ==============

@api_router.get("/cart", response_model=Cart)
async def get_cart(current_user: User = Depends(get_current_user)):
    cart = await db.carts.find_one({"user_id": current_user.id}, {"_id": 0})
    if not cart:
        cart = Cart(user_id=current_user.id)
        cart_dict = cart.model_dump()
        cart_dict['updated_at'] = cart_dict['updated_at'].isoformat()
        await db.carts.insert_one(cart_dict)
    return cart

@api_router.post("/cart/items")
async def add_to_cart(item: CartItem, current_user: User = Depends(get_current_user)):
    # Check if product exists
    product = await db.products.find_one({"id": item.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get or create cart
    cart = await db.carts.find_one({"user_id": current_user.id})
    if not cart:
        cart = Cart(user_id=current_user.id, items=[item])
        cart_dict = cart.model_dump()
        cart_dict['updated_at'] = cart_dict['updated_at'].isoformat()
        await db.carts.insert_one(cart_dict)
    else:
        # Check if item already in cart
        existing_item = next((i for i in cart.get('items', []) if i['product_id'] == item.product_id), None)
        if existing_item:
            # Update quantity
            await db.carts.update_one(
                {"user_id": current_user.id, "items.product_id": item.product_id},
                {"$set": {"items.$.quantity": item.quantity, "updated_at": datetime.now(timezone.utc).isoformat()}}
            )
        else:
            # Add new item
            await db.carts.update_one(
                {"user_id": current_user.id},
                {"$push": {"items": item.model_dump()}, "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}}
            )
    
    return {"message": "Item added to cart"}

@api_router.delete("/cart/items/{product_id}")
async def remove_from_cart(product_id: str, current_user: User = Depends(get_current_user)):
    await db.carts.update_one(
        {"user_id": current_user.id},
        {"$pull": {"items": {"product_id": product_id}}, "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    return {"message": "Item removed from cart"}

@api_router.delete("/cart")
async def clear_cart(current_user: User = Depends(get_current_user)):
    await db.carts.update_one(
        {"user_id": current_user.id},
        {"$set": {"items": [], "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    return {"message": "Cart cleared"}

# ============== ORDER ROUTES ==============

@api_router.post("/orders")
async def create_order(current_user: User = Depends(get_current_user)):
    # Get user's cart
    cart = await db.carts.find_one({"user_id": current_user.id})
    if not cart or not cart.get('items'):
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total and prepare order items
    order_items = []
    total_amount = 0.0
    
    for cart_item in cart['items']:
        product = await db.products.find_one({"id": cart_item['product_id']})
        if not product:
            continue
        
        if product['stock'] < cart_item['quantity']:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product['name']}")
        
        order_item = OrderItem(
            product_id=product['id'],
            product_name=product['name'],
            quantity=cart_item['quantity'],
            price=product['price']
        )
        order_items.append(order_item)
        total_amount += product['price'] * cart_item['quantity']
    
    # Create order
    order = Order(
        user_id=current_user.id,
        items=order_items,
        total_amount=total_amount,
        status="pending",
        payment_status="pending"
    )
    
    order_dict = order.model_dump()
    order_dict['created_at'] = order_dict['created_at'].isoformat()
    
    await db.orders.insert_one(order_dict)
    
    return order

@api_router.get("/orders", response_model=List[Order])
async def get_orders(current_user: User = Depends(get_current_user)):
    orders = await db.orders.find({"user_id": current_user.id}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    return orders

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str, current_user: User = Depends(get_current_user)):
    order = await db.orders.find_one({"id": order_id, "user_id": current_user.id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Admin: Get all orders
@api_router.get("/admin/orders", response_model=List[Order])
async def get_all_orders(admin: User = Depends(get_admin_user)):
    orders = await db.orders.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    return orders

# Admin: Update order status
@api_router.patch("/admin/orders/{order_id}")
async def update_order_status(order_id: str, status: str, admin: User = Depends(get_admin_user)):
    await db.orders.update_one({"id": order_id}, {"$set": {"status": status}})
    return {"message": "Order status updated"}

# ============== PAYMENT ROUTES ==============
# Note: Stripe payment routes disabled - using mock checkout instead

# class CheckoutRequest(BaseModel):
#     order_id: str
#     origin_url: str

# @api_router.post("/checkout")
async def create_checkout(request: CheckoutRequest, http_request: Request, current_user: User = Depends(get_current_user)):
    # Get order
    order = await db.orders.find_one({"id": request.order_id, "user_id": current_user.id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order['payment_status'] == 'paid':
        raise HTTPException(status_code=400, detail="Order already paid")
    
    # Initialize Stripe
    api_key = os.environ.get('STRIPE_API_KEY')
    host_url = str(http_request.base_url)
    webhook_url = f"{host_url}api/webhook/stripe"
    stripe_checkout = StripeCheckout(api_key=api_key, webhook_url=webhook_url)
    
    # Create checkout session
    success_url = f"{request.origin_url}/order-success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{request.origin_url}/cart"
    
    checkout_request = CheckoutSessionRequest(
        amount=float(order['total_amount']),
        currency="usd",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "order_id": order['id'],
            "user_id": current_user.id
        }
    )
    
    session = await stripe_checkout.create_checkout_session(checkout_request)
    
    # Create payment transaction
    transaction = PaymentTransaction(
        session_id=session.session_id,
        user_id=current_user.id,
        order_id=order['id'],
        amount=float(order['total_amount']),
        currency="usd",
        payment_status="pending",
        metadata=checkout_request.metadata
    )
    
    transaction_dict = transaction.model_dump()
    transaction_dict['created_at'] = transaction_dict['created_at'].isoformat()
    transaction_dict['updated_at'] = transaction_dict['updated_at'].isoformat()
    
    await db.payment_transactions.insert_one(transaction_dict)
    
    # Update order with session_id
    await db.orders.update_one(
        {"id": order['id']},
        {"$set": {"session_id": session.session_id}}
    )
    
    return {"url": session.url, "session_id": session.session_id}

@api_router.get("/checkout/status/{session_id}")
async def get_checkout_status(session_id: str, current_user: User = Depends(get_current_user)):
    # Check if already processed
    transaction = await db.payment_transactions.find_one({"session_id": session_id})
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if transaction['payment_status'] == 'paid':
        return {"status": "complete", "payment_status": "paid", "order_id": transaction['order_id']}
    
    # Check with Stripe
    api_key = os.environ.get('STRIPE_API_KEY')
    stripe_checkout = StripeCheckout(api_key=api_key, webhook_url="")
    
    try:
        checkout_status = await stripe_checkout.get_checkout_status(session_id)
        
        # Update transaction
        await db.payment_transactions.update_one(
            {"session_id": session_id},
            {"$set": {
                "payment_status": checkout_status.payment_status,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        # If payment successful and not already processed
        if checkout_status.payment_status == 'paid' and transaction['payment_status'] != 'paid':
            order_id = transaction['order_id']
            order = await db.orders.find_one({"id": order_id})
            
            if order:
                # Update order status
                await db.orders.update_one(
                    {"id": order_id},
                    {"$set": {"payment_status": "paid", "status": "processing"}}
                )
                
                # Update product stock
                for item in order['items']:
                    await db.products.update_one(
                        {"id": item['product_id']},
                        {"$inc": {"stock": -item['quantity']}}
                    )
                
                # Clear user's cart
                await db.carts.update_one(
                    {"user_id": transaction['user_id']},
                    {"$set": {"items": [], "updated_at": datetime.now(timezone.utc).isoformat()}}
                )
        
        return {
            "status": checkout_status.status,
            "payment_status": checkout_status.payment_status,
            "order_id": transaction['order_id']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("Stripe-Signature")
    
    api_key = os.environ.get('STRIPE_API_KEY')
    stripe_checkout = StripeCheckout(api_key=api_key, webhook_url="")
    
    try:
        webhook_response = await stripe_checkout.handle_webhook(body, signature)
        
        # Handle webhook event
        if webhook_response.event_type == 'checkout.session.completed':
            session_id = webhook_response.session_id
            transaction = await db.payment_transactions.find_one({"session_id": session_id})
            
            if transaction and transaction['payment_status'] != 'paid':
                # Update transaction
                await db.payment_transactions.update_one(
                    {"session_id": session_id},
                    {"$set": {"payment_status": "paid", "updated_at": datetime.now(timezone.utc).isoformat()}}
                )
                
                # Update order
                await db.orders.update_one(
                    {"id": transaction['order_id']},
                    {"$set": {"payment_status": "paid", "status": "processing"}}
                )
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== REVIEW ROUTES ==============

@api_router.post("/reviews")
async def create_review(review_data: ReviewCreate, current_user: User = Depends(get_current_user)):
    # Check if product exists
    product = await db.products.find_one({"id": review_data.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user already reviewed
    existing_review = await db.reviews.find_one({
        "product_id": review_data.product_id,
        "user_id": current_user.id
    })
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this product")
    
    # Create review
    review = Review(
        product_id=review_data.product_id,
        user_id=current_user.id,
        user_name=current_user.name,
        rating=review_data.rating,
        comment=review_data.comment
    )
    
    review_dict = review.model_dump()
    review_dict['created_at'] = review_dict['created_at'].isoformat()
    
    await db.reviews.insert_one(review_dict)
    
    # Update product rating
    all_reviews = await db.reviews.find({"product_id": review_data.product_id}).to_list(1000)
    avg_rating = sum(r['rating'] for r in all_reviews) / len(all_reviews)
    
    await db.products.update_one(
        {"id": review_data.product_id},
        {"$set": {"rating": round(avg_rating, 1), "reviews_count": len(all_reviews)}}
    )
    
    return review

@api_router.get("/reviews/{product_id}", response_model=List[Review])
async def get_reviews(product_id: str):
    reviews = await db.reviews.find({"product_id": product_id}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    return reviews

# ============== AI RECOMMENDATION ROUTES ==============
# Note: AI recommendations disabled - emergentintegrations removed

# @api_router.post("/recommendations")
# async def get_recommendations_disabled(current_user: User = Depends(get_current_user)):
    # Get user's order history
    orders = await db.orders.find({"user_id": current_user.id, "payment_status": "paid"}).to_list(100)
    
    # Get all products
    all_products = await db.products.find({}, {"_id": 0}).to_list(1000)
    
    # Build context for AI
    purchased_products = []
    for order in orders:
        for item in order.get('items', []):
            purchased_products.append(item.get('product_name', ''))
    
    product_list = "\n".join([f"- {p['name']} ({p['category']}, ${p['price']})" for p in all_products[:50]])
    
    prompt = f"""User has purchased: {', '.join(purchased_products) if purchased_products else 'No previous purchases'}.

Available products:
{product_list}

Based on the user's purchase history and available products, recommend 3-5 products they might be interested in. Provide only product names in a comma-separated list."""
    
    # Call AI
    api_key = os.environ.get('EMERGENT_LLM_KEY')
    chat = LlmChat(
        api_key=api_key,
        session_id=f"recommendations_{current_user.id}",
        system_message="You are a helpful shopping assistant that recommends appliances based on user preferences."
    ).with_model("openai", "gpt-4o-mini")
    
    user_message = UserMessage(text=prompt)
    response = await chat.send_message(user_message)
    
    # Parse recommendations
    recommended_names = [name.strip() for name in response.split(',')]
    
    # Find matching products
    recommended_products = []
    for name in recommended_names:
        for product in all_products:
            if name.lower() in product['name'].lower():
                recommended_products.append(product)
                break
    
    return {"recommendations": recommended_products[:5]}

# ============== RECEIPT ROUTES ==============

@api_router.get("/orders/{order_id}/receipt")
async def get_receipt(order_id: str, current_user: User = Depends(get_current_user)):
    # Get order details
    order = await db.orders.find_one({"id": order_id, "user_id": current_user.id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@api_router.get("/orders/{order_id}/receipt/pdf")
async def download_receipt_pdf(order_id: str, current_user: User = Depends(get_current_user)):
    # Get order details
    order = await db.orders.find_one({"id": order_id, "user_id": current_user.id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get user details
    user = await db.users.find_one({"id": current_user.id}, {"_id": 0})
    
    # Generate PDF using reportlab
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0ea5e9'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    # Company name and title
    story.append(Paragraph("ApplianceHub", title_style))
    story.append(Paragraph("ORDER RECEIPT", styles['Heading2']))
    story.append(Spacer(1, 0.3*inch))
    
    # Order info
    order_date = datetime.fromisoformat(order['created_at']).strftime('%B %d, %Y %I:%M %p')
    info_data = [
        ['Order ID:', order['id'][:8].upper()],
        ['Date:', order_date],
        ['Customer:', user['name']],
        ['Email:', user['email']],
        ['Payment Status:', order['payment_status'].upper()]
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#64748b')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Items table
    items_data = [['Product', 'Qty', 'Price', 'Total']]
    for item in order['items']:
        item_total = item['price'] * item['quantity']
        items_data.append([
            item['product_name'],
            str(item['quantity']),
            f"₱{item['price']:.2f}",
            f"₱{item_total:.2f}"
        ])
    
    items_table = Table(items_data, colWidths=[3*inch, 0.8*inch, 1.2*inch, 1.2*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0ea5e9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Totals
    totals_data = [
        ['Subtotal:', f"₱{order['total_amount']:.2f}"],
        ['Shipping:', 'FREE'],
        ['', ''],
        ['TOTAL:', f"₱{order['total_amount']:.2f}"]
    ]
    
    totals_table = Table(totals_data, colWidths=[5*inch, 1.2*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, 1), 'Helvetica'),
        ('FONTNAME', (0, 3), (0, 3), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 2), 10),
        ('FONTSIZE', (0, 3), (-1, 3), 14),
        ('TEXTCOLOR', (0, 3), (-1, 3), colors.HexColor('#0ea5e9')),
        ('LINEABOVE', (0, 3), (-1, 3), 2, colors.HexColor('#0ea5e9')),
        ('TOPPADDING', (0, 3), (-1, 3), 10),
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#94a3b8'),
        alignment=TA_CENTER
    )
    story.append(Paragraph("Thank you for shopping with ApplianceHub!", footer_style))
    story.append(Paragraph("For questions or support, please contact us at support@appliancehub.com", footer_style))
    
    # Build PDF
    doc.build(story)
    pdf_buffer.seek(0)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=receipt_{order['id'][:8]}.pdf"}
    )

@api_router.post("/orders/{order_id}/email-receipt")
async def email_receipt(order_id: str, current_user: User = Depends(get_current_user)):
    # Get order details
    order = await db.orders.find_one({"id": order_id, "user_id": current_user.id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Note: Email functionality would require SMTP configuration
    # For now, we'll return success and log the action
    logger.info(f"Email receipt requested for order {order_id} by user {current_user.email}")
    
    return {
        "message": "Receipt email sent successfully!",
        "email": current_user.email,
        "order_id": order_id
    }

# ============== MOCK PAYMENT ROUTE ==============

@api_router.patch("/orders/{order_id}/mock-payment")
async def mock_payment(order_id: str, current_user: User = Depends(get_current_user)):
    # Get order
    order = await db.orders.find_one({"id": order_id, "user_id": current_user.id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order['payment_status'] == 'paid':
        return {"message": "Order already paid"}
    
    # Update order status
    await db.orders.update_one(
        {"id": order_id},
        {"$set": {"payment_status": "paid", "status": "processing"}}
    )
    
    # Update product stock
    for item in order['items']:
        await db.products.update_one(
            {"id": item['product_id']},
            {"$inc": {"stock": -item['quantity']}}
        )
    
    # Clear user's cart
    await db.carts.update_one(
        {"user_id": current_user.id},
        {"$set": {"items": [], "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"message": "Payment successful", "order_id": order_id}

# ============== GENERAL ROUTES ==============

@api_router.get("/")
async def root():
    return {"message": "Appliance Shop API"}

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()