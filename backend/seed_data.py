import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pathlib import Path
import uuid
from datetime import datetime, timezone
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Clear existing data
    await db.products.delete_many({})
    await db.users.delete_many({})
    
    print("Seeding database...")
    
    # Create admin user
    admin_user = {
        "id": str(uuid.uuid4()),
        "name": "Admin User",
        "email": "admin@appliancehub.com",
        "password": pwd_context.hash("admin123"),
        "is_admin": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(admin_user)
    print("✓ Created admin user (admin@appliancehub.com / admin123)")
    
    # Create sample products
    products = [
        {
            "id": str(uuid.uuid4()),
            "name": "Samsung Family Hub Refrigerator",
            "description": "21.5 cu. ft. 4-Door French Door Refrigerator with Touch Screen. Stay connected with built-in WiFi and Family Hub touchscreen.",
            "price": 2499.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=800",
            "brand": "Samsung",
            "stock": 15,
            "features": [
                "21.5 cu. ft. capacity",
                "Built-in WiFi and touchscreen",
                "FlexZone drawer with adjustable temperature",
                "Energy Star certified",
                "French door design"
            ],
            "rating": 4.5,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "LG ThinQ Front Load Washer",
            "description": "4.5 cu. ft. Ultra Large Capacity Smart Front Load Washer with AI DD and TurboDrum technology for superior cleaning.",
            "price": 1299.99,
            "category": "Washing Machines",
            "image_url": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=800",
            "brand": "LG",
            "stock": 20,
            "features": [
                "4.5 cu. ft. capacity",
                "AI Direct Drive technology",
                "TurboWash 360",
                "SmartThinQ app compatible",
                "Steam cleaning"
            ],
            "rating": 4.7,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Whirlpool Smart Dishwasher",
            "description": "Built-in dishwasher with sensor cycle and fingerprint-resistant stainless steel. Voice control enabled.",
            "price": 849.99,
            "category": "Dishwashers",
            "image_url": "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=800",
            "brand": "Whirlpool",
            "stock": 18,
            "features": [
                "Sensor cycle with soil sensor",
                "Voice control compatible",
                "Fingerprint-resistant finish",
                "Adjustable upper rack",
                "Energy efficient"
            ],
            "rating": 4.3,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Daikin Split Air Conditioner",
            "description": "18,000 BTU Ductless Mini Split Air Conditioner with Heat Pump. Whisper-quiet operation with smart control.",
            "price": 1899.99,
            "category": "Air Conditioners",
            "image_url": "https://images.unsplash.com/photo-1631545804641-2b0e18f3c28d?w=800",
            "brand": "Daikin",
            "stock": 12,
            "features": [
                "18,000 BTU cooling capacity",
                "Heating and cooling modes",
                "WiFi enabled smart control",
                "Ultra-quiet operation",
                "Energy Star certified"
            ],
            "rating": 4.8,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Panasonic Inverter Microwave",
            "description": "1.2 cu. ft. Countertop Microwave with Inverter Technology for even cooking and defrosting.",
            "price": 249.99,
            "category": "Microwaves",
            "image_url": "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=800",
            "brand": "Panasonic",
            "stock": 25,
            "features": [
                "1.2 cu. ft. capacity",
                "Inverter technology",
                "Turbo defrost",
                "1200W power",
                "Keep warm feature"
            ],
            "rating": 4.4,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Bosch Electric Range",
            "description": "30-inch electric slide-in range with smooth-top ceramic glass surface and True European Convection.",
            "price": 1599.99,
            "category": "Ranges",
            "image_url": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800",
            "brand": "Bosch",
            "stock": 10,
            "features": [
                "30-inch width",
                "True European Convection",
                "Self-cleaning oven",
                "Ceramic glass cooktop",
                "Storage drawer"
            ],
            "rating": 4.6,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "GE Profile Smart Oven",
            "description": "30-inch built-in double wall oven with WiFi connectivity and voice control. Convection cooking.",
            "price": 2899.99,
            "category": "Ovens",
            "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800",
            "brand": "GE",
            "stock": 8,
            "features": [
                "Double wall oven",
                "WiFi connectivity",
                "Voice control enabled",
                "True European Convection",
                "Self-cleaning with steam"
            ],
            "rating": 4.7,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Frigidaire Side-by-Side Refrigerator",
            "description": "25.5 cu. ft. side-by-side refrigerator with external water and ice dispenser. Store-More shelves.",
            "price": 1899.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=800",
            "brand": "Frigidaire",
            "stock": 14,
            "features": [
                "25.5 cu. ft. capacity",
                "External water dispenser",
                "Ice maker included",
                "Store-More shelves",
                "LED lighting"
            ],
            "rating": 4.2,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Maytag Top Load Washer",
            "description": "5.3 cu. ft. high-efficiency top load washer with PowerWash agitator for tough stain removal.",
            "price": 799.99,
            "category": "Washing Machines",
            "image_url": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=800",
            "brand": "Maytag",
            "stock": 22,
            "features": [
                "5.3 cu. ft. capacity",
                "PowerWash agitator",
                "Deep water wash option",
                "Quick wash cycle",
                "Auto load sensing"
            ],
            "rating": 4.5,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "KitchenAid Dishwasher with PrintShield",
            "description": "44 dBA dishwasher with dynamic wash arms and ProWash cycle. FreeFlex third rack included.",
            "price": 1199.99,
            "category": "Dishwashers",
            "image_url": "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=800",
            "brand": "KitchenAid",
            "stock": 16,
            "features": [
                "44 dBA quiet operation",
                "ProWash cycle",
                "FreeFlex third rack",
                "Dynamic wash arms",
                "PrintShield finish"
            ],
            "rating": 4.8,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.products.insert_many(products)
    print(f"✓ Created {len(products)} sample products")
    
    print("\nDatabase seeded successfully!")
    print("\n" + "="*50)
    print("Admin Login Credentials:")
    print("Email: admin@appliancehub.com")
    print("Password: admin123")
    print("="*50)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
