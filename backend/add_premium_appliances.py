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

async def add_premium_appliances():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("Adding premium appliances with unique images...")
    
    # Premium appliances with diverse images
    premium_products = [
        # Refrigerators
        {
            "id": str(uuid.uuid4()),
            "name": "Beko French Door Refrigerator",
            "description": "30 cu. ft. French door refrigerator with HarvestFresh technology that preserves vitamins in fruits and vegetables.",
            "price": 2199.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=800",
            "brand": "Beko",
            "stock": 12,
            "features": [
                "HarvestFresh technology",
                "30 cu. ft. capacity",
                "NeoFrost dual cooling",
                "Active Fresh Blue Light",
                "EverFresh+ crispers"
            ],
            "rating": 4.5,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Smeg Retro Refrigerator",
            "description": "Iconic 50's style refrigerator with modern technology. Italian design meets functionality.",
            "price": 3499.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1571175351190-49c3ca49e541?w=800",
            "brand": "Smeg",
            "stock": 8,
            "features": [
                "Retro 50's design",
                "10.4 cu. ft. capacity",
                "Automatic defrost",
                "Adjustable glass shelves",
                "Energy efficient"
            ],
            "rating": 4.8,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Hisense Quad Door Refrigerator",
            "description": "26 cu. ft. quad door refrigerator with convertible zone and independent temperature control.",
            "price": 1999.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1622116814927-e08625346f39?w=800",
            "brand": "Hisense",
            "stock": 15,
            "features": [
                "Convertible middle zone",
                "26 cu. ft. capacity",
                "LED lighting",
                "Door alarm",
                "Fast cooling mode"
            ],
            "rating": 4.3,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # Washing Machines
        {
            "id": str(uuid.uuid4()),
            "name": "Electrolux UltraCare Washer",
            "description": "Front load washer with LuxCare wash system and perfect steam technology.",
            "price": 1499.99,
            "category": "Washing Machines",
            "image_url": "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?w=800",
            "brand": "Electrolux",
            "stock": 18,
            "features": [
                "LuxCare wash system",
                "Perfect steam technology",
                "4.4 cu. ft. capacity",
                "Adaptive dispenser",
                "15-minute fast wash"
            ],
            "rating": 4.6,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Bosch 800 Series Washer",
            "description": "Ultra-quiet front load washer with SpeedPerfect and AllergyPlus options.",
            "price": 1799.99,
            "category": "Washing Machines",
            "image_url": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800",
            "brand": "Bosch",
            "stock": 14,
            "features": [
                "SpeedPerfect technology",
                "AllergyPlus option",
                "2.2 cu. ft. capacity",
                "EcoSilence motor",
                "Home Connect WiFi"
            ],
            "rating": 4.7,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "GE Ultrafresh Vent Washer",
            "description": "Front load washer with UltraFresh Vent System that prevents odors from forming.",
            "price": 999.99,
            "category": "Washing Machines",
            "image_url": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=800",
            "brand": "GE",
            "stock": 22,
            "features": [
                "UltraFresh Vent System",
                "4.8 cu. ft. capacity",
                "Microban protection",
                "Dynamic balancing",
                "Deep fill option"
            ],
            "rating": 4.4,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # Dishwashers
        {
            "id": str(uuid.uuid4()),
            "name": "Cove Dishwasher",
            "description": "Premium dishwasher with FlexSpace racking system and whisper-quiet operation.",
            "price": 2299.99,
            "category": "Dishwashers",
            "image_url": "https://images.unsplash.com/photo-1556911073-38141963c9e0?w=800",
            "brand": "Cove",
            "stock": 10,
            "features": [
                "FlexSpace racking",
                "42 dBA quiet",
                "Time Savr option",
                "Leak prevention",
                "Stainless steel tub"
            ],
            "rating": 4.8,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Samsung StormWash Dishwasher",
            "description": "Dishwasher with StormWash rotating spray jets for powerful cleaning.",
            "price": 899.99,
            "category": "Dishwashers",
            "image_url": "https://images.unsplash.com/photo-1551731409-43eb3e517a1a?w=800",
            "brand": "Samsung",
            "stock": 20,
            "features": [
                "StormWash system",
                "Zone Booster option",
                "48 dBA operation",
                "AutoRelease door",
                "Linear wash system"
            ],
            "rating": 4.5,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "LG QuadWash Pro Dishwasher",
            "description": "Innovative dishwasher with QuadWash Pro and TrueSteam technology.",
            "price": 1299.99,
            "category": "Dishwashers",
            "image_url": "https://images.unsplash.com/photo-1603712725038-c0e53d5e9670?w=800",
            "brand": "LG",
            "stock": 16,
            "features": [
                "QuadWash Pro",
                "TrueSteam technology",
                "Dynamic Dry",
                "Smart ThinQ",
                "3rd rack"
            ],
            "rating": 4.7,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # Air Conditioners
        {
            "id": str(uuid.uuid4()),
            "name": "Friedrich Chill Premier AC",
            "description": "Smart room air conditioner with WiFi and voice control. Ultra-efficient cooling.",
            "price": 799.99,
            "category": "Air Conditioners",
            "image_url": "https://images.unsplash.com/photo-1620735692151-26a7e0748429?w=800",
            "brand": "Friedrich",
            "stock": 24,
            "features": [
                "14,000 BTU cooling",
                "WiFi connectivity",
                "Voice control ready",
                "4-way air direction",
                "Remote control"
            ],
            "rating": 4.6,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "LG Dual Inverter Window AC",
            "description": "Energy-efficient window AC with dual inverter compressor and 40% energy savings.",
            "price": 549.99,
            "category": "Air Conditioners",
            "image_url": "https://images.unsplash.com/photo-1624649591189-ea08af62a8f7?w=800",
            "brand": "LG",
            "stock": 28,
            "features": [
                "Dual inverter compressor",
                "12,000 BTU",
                "40% energy savings",
                "Low noise operation",
                "Smart diagnosis"
            ],
            "rating": 4.5,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Fujitsu Halcyon Mini-Split",
            "description": "Ductless mini-split with advanced filtration and ultra-quiet operation.",
            "price": 2299.99,
            "category": "Air Conditioners",
            "image_url": "https://images.unsplash.com/photo-1607400201515-c2c41c07e5cf?w=800",
            "brand": "Fujitsu",
            "stock": 12,
            "features": [
                "18,000 BTU capacity",
                "Human sensor technology",
                "Advanced air filtration",
                "19 SEER efficiency",
                "Wireless remote"
            ],
            "rating": 4.8,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # Microwaves
        {
            "id": str(uuid.uuid4()),
            "name": "GE Profile Smart Microwave",
            "description": "Over-the-range microwave with scan-to-cook technology and voice control.",
            "price": 649.99,
            "category": "Microwaves",
            "image_url": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=800",
            "brand": "GE",
            "stock": 19,
            "features": [
                "Scan-to-cook technology",
                "2.1 cu. ft. capacity",
                "1050W power",
                "Voice control",
                "Sensor cooking"
            ],
            "rating": 4.6,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Samsung Smart Over-the-Range",
            "description": "Microwave with WiFi connectivity and powerful 400 CFM ventilation.",
            "price": 599.99,
            "category": "Microwaves",
            "image_url": "https://images.unsplash.com/photo-1588854337115-1c67d9247e4d?w=800",
            "brand": "Samsung",
            "stock": 21,
            "features": [
                "WiFi enabled",
                "1.9 cu. ft. capacity",
                "400 CFM ventilation",
                "Ceramic enamel interior",
                "Eco mode"
            ],
            "rating": 4.4,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Toshiba Inverter Microwave",
            "description": "Countertop microwave with inverter technology and smart sensor cooking.",
            "price": 279.99,
            "category": "Microwaves",
            "image_url": "https://images.unsplash.com/photo-1588556542102-e6fc8dc0839f?w=800",
            "brand": "Toshiba",
            "stock": 26,
            "features": [
                "Inverter technology",
                "1.2 cu. ft. capacity",
                "1100W power",
                "One-touch smart sensor",
                "Eco mode"
            ],
            "rating": 4.3,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # Ovens
        {
            "id": str(uuid.uuid4()),
            "name": "KitchenAid Smart Oven",
            "description": "Smart wall oven with Even-Heat True Convection and temperature probe.",
            "price": 2699.99,
            "category": "Ovens",
            "image_url": "https://images.unsplash.com/photo-1601293863859-2bb0d1000edf?w=800",
            "brand": "KitchenAid",
            "stock": 9,
            "features": [
                "Even-Heat convection",
                "5.0 cu. ft. capacity",
                "Temperature probe",
                "WiFi enabled",
                "Self-cleaning"
            ],
            "rating": 4.7,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Frigidaire Gallery Wall Oven",
            "description": "Single wall oven with Air Fry technology and rapid preheat.",
            "price": 1899.99,
            "category": "Ovens",
            "image_url": "https://images.unsplash.com/photo-1583512603806-077998240c7a?w=800",
            "brand": "Frigidaire",
            "stock": 11,
            "features": [
                "Built-in Air Fry",
                "4.6 cu. ft. capacity",
                "Rapid preheat",
                "True convection",
                "Steam clean option"
            ],
            "rating": 4.5,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Whirlpool Smart Double Oven",
            "description": "Double wall oven with frozen bake technology and touchscreen controls.",
            "price": 3199.99,
            "category": "Ovens",
            "image_url": "https://images.unsplash.com/photo-1565183928294-8accb38c4f1e?w=800",
            "brand": "Whirlpool",
            "stock": 7,
            "features": [
                "Double wall oven",
                "Frozen bake technology",
                "Touchscreen controls",
                "10 cu. ft. total capacity",
                "Voice control"
            ],
            "rating": 4.8,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        
        # Ranges
        {
            "id": str(uuid.uuid4()),
            "name": "Samsung Slide-in Gas Range",
            "description": "Slide-in gas range with air fry and convection cooking.",
            "price": 1799.99,
            "category": "Ranges",
            "image_url": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800",
            "brand": "Samsung",
            "stock": 13,
            "features": [
                "Built-in air fry",
                "5.8 cu. ft. oven",
                "Convection cooking",
                "WiFi connectivity",
                "Blue LED knobs"
            ],
            "rating": 4.6,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "LG ProBake Convection Range",
            "description": "Electric range with ProBake Convection for even baking results.",
            "price": 1299.99,
            "category": "Ranges",
            "image_url": "https://images.unsplash.com/photo-1562437077-ce7eb6d06768?w=800",
            "brand": "LG",
            "stock": 17,
            "features": [
                "ProBake Convection",
                "6.3 cu. ft. oven",
                "Air fry mode",
                "InstaView window",
                "EasyClean technology"
            ],
            "rating": 4.5,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Cafe Induction Range",
            "description": "Smart slide-in induction range with precision cooking and WiFi.",
            "price": 3999.99,
            "category": "Ranges",
            "image_url": "https://images.unsplash.com/photo-1585659722993-f8d5b5e0a9e5?w=800",
            "brand": "Cafe",
            "stock": 6,
            "features": [
                "Induction cooktop",
                "True European Convection",
                "5.7 cu. ft. oven",
                "WiFi enabled",
                "Customizable hardware"
            ],
            "rating": 4.9,
            "reviews_count": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    result = await db.products.insert_many(premium_products)
    print(f"✓ Added {len(result.inserted_ids)} premium appliances with unique images!")
    
    # Update total count
    total = await db.products.count_documents({})
    print(f"\n📊 Total products in catalog: {total}")
    
    # Show category breakdown
    print("\n📦 Category Breakdown:")
    categories = await db.products.distinct("category")
    for category in sorted(categories):
        count = await db.products.count_documents({"category": category})
        print(f"  • {category}: {count} products")
    
    # Show brand count
    brands = await db.products.distinct("brand")
    print(f"\n🏷️  Total brands: {len(brands)}")
    
    # Price range
    pipeline = [
        {"$group": {
            "_id": None,
            "min_price": {"$min": "$price"},
            "max_price": {"$max": "$price"},
            "avg_price": {"$avg": "$price"}
        }}
    ]
    price_stats = await db.products.aggregate(pipeline).to_list(1)
    if price_stats:
        stats = price_stats[0]
        print(f"\n💰 Price Range:")
        print(f"  • Lowest: ${stats['min_price']:.2f}")
        print(f"  • Highest: ${stats['max_price']:.2f}")
        print(f"  • Average: ${stats['avg_price']:.2f}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_premium_appliances())
