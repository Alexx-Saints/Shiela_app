import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pathlib import Path
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def add_more_products():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("Adding more appliances to the catalog...")
    
    # Additional products
    new_products = [
        {
            "id": str(uuid.uuid4()),
            "name": "Sharp Carousel Microwave Oven",
            "description": "1.4 cu. ft. countertop microwave with 1000W power and sensor cooking. Features 11 power levels and express cook options.",
            "price": 189.99,
            "category": "Microwaves",
            "image_url": "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=800",
            "brand": "Sharp",
            "stock": 30,
            "features": [
                "1.4 cu. ft. capacity",
                "1000W cooking power",
                "Sensor cooking technology",
                "11 power levels",
                "Express cook buttons"
            ],
            "rating": 4.3,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Electrolux French Door Refrigerator",
            "description": "Counter-depth 27.8 cu. ft. French door refrigerator with Perfect Temp drawer and luxury design.",
            "price": 3299.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=800",
            "brand": "Electrolux",
            "stock": 8,
            "features": [
                "27.8 cu. ft. capacity",
                "Counter-depth design",
                "Perfect Temp drawer",
                "Luxury-Close doors",
                "IQ-Touch controls"
            ],
            "rating": 4.9,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Haier Portable Air Conditioner",
            "description": "12,000 BTU portable AC with dehumidifier and fan modes. Easy to install window kit included.",
            "price": 449.99,
            "category": "Air Conditioners",
            "image_url": "https://images.unsplash.com/photo-1631545804641-2b0e18f3c28d?w=800",
            "brand": "Haier",
            "stock": 25,
            "features": [
                "12,000 BTU cooling",
                "3-in-1: AC, dehumidifier, fan",
                "Easy-roll casters",
                "Remote control included",
                "Auto-evaporation system"
            ],
            "rating": 4.1,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Miele Built-In Dishwasher",
            "description": "Premium dishwasher with AutoDos automatic dispensing and QuickIntenseWash. Whisper-quiet at 44 dBA.",
            "price": 1799.99,
            "category": "Dishwashers",
            "image_url": "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=800",
            "brand": "Miele",
            "stock": 12,
            "features": [
                "AutoDos automatic dispensing",
                "QuickIntenseWash 58 min",
                "44 dBA ultra-quiet",
                "Knock2open feature",
                "Perfect GlassCare"
            ],
            "rating": 4.9,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Speed Queen Top Load Washer",
            "description": "Commercial-grade 3.3 cu. ft. top load washer with 840 RPM spin speed. Built to last 25 years.",
            "price": 1099.99,
            "category": "Washing Machines",
            "image_url": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=800",
            "brand": "Speed Queen",
            "stock": 15,
            "features": [
                "3.3 cu. ft. capacity",
                "Commercial-grade build",
                "840 RPM spin speed",
                "7-year warranty",
                "Stainless steel tub"
            ],
            "rating": 4.8,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Viking Professional Gas Range",
            "description": "48-inch professional gas range with 6 burners and griddle. Restaurant-quality cooking at home.",
            "price": 8999.99,
            "category": "Ranges",
            "image_url": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800",
            "brand": "Viking",
            "stock": 4,
            "features": [
                "48-inch professional width",
                "6 sealed burners + griddle",
                "VariSimmer setting",
                "Convection oven",
                "Gourmet-Glo broiler"
            ],
            "rating": 5.0,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Sub-Zero Built-In Refrigerator",
            "description": "42-inch built-in side-by-side refrigerator with advanced air purification. The ultimate in food preservation.",
            "price": 11999.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=800",
            "brand": "Sub-Zero",
            "stock": 3,
            "features": [
                "42-inch built-in design",
                "Air purification system",
                "Dual refrigeration",
                "LED lighting",
                "Water filtration"
            ],
            "rating": 5.0,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Wolf Dual Fuel Range",
            "description": "36-inch dual fuel range combining gas cooktop with electric convection oven. Professional performance.",
            "price": 7499.99,
            "category": "Ranges",
            "image_url": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800",
            "brand": "Wolf",
            "stock": 6,
            "features": [
                "Dual fuel technology",
                "4.4 cu. ft. oven capacity",
                "Dual convection",
                "18,000 BTU burners",
                "Self-clean mode"
            ],
            "rating": 4.9,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Thermador Steam Oven",
            "description": "24-inch built-in steam oven with 20 cooking modes. Perfect for healthy cooking and bread baking.",
            "price": 3499.99,
            "category": "Ovens",
            "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800",
            "brand": "Thermador",
            "stock": 7,
            "features": [
                "20 cooking modes",
                "1.4 cu. ft. capacity",
                "Temperature probe",
                "Touch controls",
                "Self-descaling"
            ],
            "rating": 4.7,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Mitsubishi Ductless Mini-Split",
            "description": "24,000 BTU ductless mini-split heat pump with hyper-heating technology. Efficient heating and cooling.",
            "price": 2799.99,
            "category": "Air Conditioners",
            "image_url": "https://images.unsplash.com/photo-1631545804641-2b0e18f3c28d?w=800",
            "brand": "Mitsubishi",
            "stock": 10,
            "features": [
                "24,000 BTU capacity",
                "Hyper-heat technology",
                "Zone control",
                "WiFi enabled",
                "ENERGY STAR certified"
            ],
            "rating": 4.8,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Cafe Smart French Door Refrigerator",
            "description": "27.7 cu. ft. smart refrigerator with Keurig K-Cup brewing system built-in. Modern matte finish.",
            "price": 3799.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=800",
            "brand": "Cafe",
            "stock": 11,
            "features": [
                "Built-in Keurig K-Cup system",
                "27.7 cu. ft. capacity",
                "WiFi connectivity",
                "Hands-free autofill",
                "Matte finish options"
            ],
            "rating": 4.6,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Asko Front Load Washer",
            "description": "Scandinavian design 2.7 cu. ft. washer with 1600 RPM spin speed. Steel Seal door for maximum durability.",
            "price": 1599.99,
            "category": "Washing Machines",
            "image_url": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=800",
            "brand": "Asko",
            "stock": 13,
            "features": [
                "2.7 cu. ft. capacity",
                "1600 RPM spin speed",
                "Steel Seal door",
                "Active Drum technology",
                "Scandinavian design"
            ],
            "rating": 4.7,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Breville Combi Wave Microwave",
            "description": "3-in-1 microwave with air fryer and convection oven. Smart cooking with 19 preset programs.",
            "price": 499.99,
            "category": "Microwaves",
            "image_url": "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=800",
            "brand": "Breville",
            "stock": 20,
            "features": [
                "3-in-1: microwave, air fryer, oven",
                "19 smart presets",
                "1.1 cu. ft. capacity",
                "Element IQ system",
                "Power smoothing inverter"
            ],
            "rating": 4.8,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Fisher & Paykel Dishwasher Drawer",
            "description": "Double DishDrawer with SmartDrive technology. Independent drawers for ultimate flexibility.",
            "price": 1899.99,
            "category": "Dishwashers",
            "image_url": "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=800",
            "brand": "Fisher & Paykel",
            "stock": 9,
            "features": [
                "Double drawer design",
                "SmartDrive technology",
                "6 wash programs each",
                "Quiet operation",
                "Adjustable racks"
            ],
            "rating": 4.5,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Jenn-Air Built-In Wall Oven",
            "description": "30-inch wall oven with V2 Vertical Dual-Fan Convection. Precision cooking with WiFi connectivity.",
            "price": 3299.99,
            "category": "Ovens",
            "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800",
            "brand": "Jenn-Air",
            "stock": 8,
            "features": [
                "V2 Vertical Dual-Fan",
                "5.0 cu. ft. capacity",
                "WiFi connected",
                "Temperature probe",
                "Rapid preheat"
            ],
            "rating": 4.6,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Carrier Inverter Window AC",
            "description": "10,000 BTU inverter window air conditioner with ultra-quiet operation and WiFi control.",
            "price": 599.99,
            "category": "Air Conditioners",
            "image_url": "https://images.unsplash.com/photo-1631545804641-2b0e18f3c28d?w=800",
            "brand": "Carrier",
            "stock": 18,
            "features": [
                "10,000 BTU cooling",
                "Inverter technology",
                "WiFi smart control",
                "Ultra-quiet operation",
                "Energy efficient"
            ],
            "rating": 4.4,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Blomberg Compact Washer Dryer",
            "description": "24-inch ventless washer dryer combo. Perfect for apartments with limited space.",
            "price": 1399.99,
            "category": "Washing Machines",
            "image_url": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=800",
            "brand": "Blomberg",
            "stock": 14,
            "features": [
                "Washer dryer combo",
                "Ventless design",
                "24-inch compact width",
                "16 wash programs",
                "Delay start"
            ],
            "rating": 4.2,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Bertazzoni Professional Series Range",
            "description": "36-inch Italian-made range with 6 brass burners. Combines style and professional performance.",
            "price": 5999.99,
            "category": "Ranges",
            "image_url": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800",
            "brand": "Bertazzoni",
            "stock": 7,
            "features": [
                "Italian craftsmanship",
                "6 brass burners",
                "Electric convection oven",
                "5.7 cu. ft. capacity",
                "Continuous grates"
            ],
            "rating": 4.7,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Dacor Modernist Steam Oven",
            "description": "30-inch combi steam oven with sous vide precision. 10 cooking modes for culinary perfection.",
            "price": 4499.99,
            "category": "Ovens",
            "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800",
            "brand": "Dacor",
            "stock": 5,
            "features": [
                "Combi steam technology",
                "Sous vide precision",
                "10 cooking modes",
                "WiFi connectivity",
                "Touch screen controls"
            ],
            "rating": 4.9,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Liebherr Premium BioFresh Refrigerator",
            "description": "30-inch bottom freezer refrigerator with BioFresh technology. Keeps food fresh up to 3x longer.",
            "price": 4299.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=800",
            "brand": "Liebherr",
            "stock": 6,
            "features": [
                "BioFresh technology",
                "16 cu. ft. capacity",
                "PowerCooling system",
                "LED lighting",
                "German engineering"
            ],
            "rating": 4.9,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    result = await db.products.insert_many(new_products)
    print(f"✓ Added {len(result.inserted_ids)} new appliances!")
    
    # Get total count
    total = await db.products.count_documents({})
    print(f"\nTotal products in catalog: {total}")
    
    # Show categories
    categories = await db.products.distinct("category")
    print(f"Categories: {', '.join(categories)}")
    
    # Show brands
    brands = await db.products.distinct("brand")
    print(f"Total brands: {len(brands)}")
    print(f"Brands: {', '.join(sorted(brands))}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_more_products())
