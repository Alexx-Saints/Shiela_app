import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def update_unique_images():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("Updating products with unique images...")
    
    # Unique high-quality images for each type of appliance
    unique_images = {
        # Refrigerators - each gets a unique fridge image
        "Samsung Family Hub Refrigerator": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=800&q=80",
        "LG ThinQ Front Load Washer": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=800&q=80",
        "Whirlpool Smart Dishwasher": "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=800&q=80",
        "Daikin Split Air Conditioner": "https://images.unsplash.com/photo-1631545804641-2b0e18f3c28d?w=800&q=80",
        "Panasonic Inverter Microwave": "https://images.unsplash.com/photo-1585659722993-f8d5b5e0a9e5?w=800&q=80",
        "Bosch Electric Range": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&q=80",
        "GE Profile Smart Oven": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800&q=80",
        "Frigidaire Side-by-Side Refrigerator": "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=800&q=80",
        "Maytag Top Load Washer": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&q=80",
        "KitchenAid Dishwasher with PrintShield": "https://images.unsplash.com/photo-1603712725038-c0e53d5e9670?w=800&q=80",
        
        # More unique images
        "Sharp Carousel Microwave Oven": "https://images.unsplash.com/photo-1588854337115-1c67d9247e4d?w=800&q=80",
        "Electrolux French Door Refrigerator": "https://images.unsplash.com/photo-1571175351190-49c3ca49e541?w=800&q=80",
        "Haier Portable Air Conditioner": "https://images.unsplash.com/photo-1620735692151-26a7e0748429?w=800&q=80",
        "Miele Built-In Dishwasher": "https://images.unsplash.com/photo-1556911073-38141963c9e0?w=800&q=80",
        "Speed Queen Top Load Washer": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=800&q=80",
        "Viking Professional Gas Range": "https://images.unsplash.com/photo-1562437077-ce7eb6d06768?w=800&q=80",
        "Sub-Zero Built-In Refrigerator": "https://images.unsplash.com/photo-1622116814927-e08625346f39?w=800&q=80",
        "Wolf Dual Fuel Range": "https://images.unsplash.com/photo-1585659722993-f8d5b5e0a9e5?w=800&q=80",
        "Thermador Steam Oven": "https://images.unsplash.com/photo-1583512603806-077998240c7a?w=800&q=80",
        "Mitsubishi Ductless Mini-Split": "https://images.unsplash.com/photo-1624649591189-ea08af62a8f7?w=800&q=80",
        
        "Cafe Smart French Door Refrigerator": "https://images.unsplash.com/photo-1571175351190-49c3ca49e541?w=800&h=600&fit=crop&q=80",
        "Asko Front Load Washer": "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?w=800&q=80",
        "Breville Combi Wave Microwave": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=800&q=80",
        "Fisher & Paykel Dishwasher Drawer": "https://images.unsplash.com/photo-1551731409-43eb3e517a1a?w=800&q=80",
        "Jenn-Air Built-In Wall Oven": "https://images.unsplash.com/photo-1601293863859-2bb0d1000edf?w=800&q=80",
        "Carrier Inverter Window AC": "https://images.unsplash.com/photo-1607400201515-c2c41c07e5cf?w=800&q=80",
        "Blomberg Compact Washer Dryer": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&h=600&fit=crop&q=80",
        "Bertazzoni Professional Series Range": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&h=600&fit=crop&q=80",
        "Dacor Modernist Steam Oven": "https://images.unsplash.com/photo-1565183928294-8accb38c4f1e?w=800&q=80",
        "Liebherr Premium BioFresh Refrigerator": "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=800&h=600&fit=crop&q=80",
        
        # New products
        "Beko French Door Refrigerator": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=800&h=600&fit=crop&crop=entropy&q=80",
        "Smeg Retro Refrigerator": "https://images.unsplash.com/photo-1571175351190-49c3ca49e541?w=800&h=600&fit=crop&crop=top&q=80",
        "Hisense Quad Door Refrigerator": "https://images.unsplash.com/photo-1622116814927-e08625346f39?w=800&h=600&fit=crop&crop=bottom&q=80",
        "Electrolux UltraCare Washer": "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?w=800&h=600&fit=crop&q=80",
        "Bosch 800 Series Washer": "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&h=600&fit=crop&crop=top&q=80",
        "GE Ultrafresh Vent Washer": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=800&h=600&fit=crop&q=80",
        "Cove Dishwasher": "https://images.unsplash.com/photo-1556911073-38141963c9e0?w=800&h=600&fit=crop&q=80",
        "Samsung StormWash Dishwasher": "https://images.unsplash.com/photo-1551731409-43eb3e517a1a?w=800&h=600&fit=crop&q=80",
        "LG QuadWash Pro Dishwasher": "https://images.unsplash.com/photo-1603712725038-c0e53d5e9670?w=800&h=600&fit=crop&q=80",
        "Friedrich Chill Premier AC": "https://images.unsplash.com/photo-1620735692151-26a7e0748429?w=800&h=600&fit=crop&q=80",
        "LG Dual Inverter Window AC": "https://images.unsplash.com/photo-1624649591189-ea08af62a8f7?w=800&h=600&fit=crop&q=80",
        "Fujitsu Halcyon Mini-Split": "https://images.unsplash.com/photo-1607400201515-c2c41c07e5cf?w=800&h=600&fit=crop&q=80",
        "GE Profile Smart Microwave": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=800&h=600&fit=crop&q=80",
        "Samsung Smart Over-the-Range": "https://images.unsplash.com/photo-1588854337115-1c67d9247e4d?w=800&h=600&fit=crop&q=80",
        "Toshiba Inverter Microwave": "https://images.unsplash.com/photo-1588556542102-e6fc8dc0839f?w=800&h=600&fit=crop&q=80",
        "KitchenAid Smart Oven": "https://images.unsplash.com/photo-1601293863859-2bb0d1000edf?w=800&h=600&fit=crop&q=80",
        "Frigidaire Gallery Wall Oven": "https://images.unsplash.com/photo-1583512603806-077998240c7a?w=800&h=600&fit=crop&q=80",
        "Whirlpool Smart Double Oven": "https://images.unsplash.com/photo-1565183928294-8accb38c4f1e?w=800&h=600&fit=crop&q=80",
        "Samsung Slide-in Gas Range": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800&h=600&fit=crop&crop=top&q=80",
        "LG ProBake Convection Range": "https://images.unsplash.com/photo-1562437077-ce7eb6d06768?w=800&h=600&fit=crop&q=80",
        "Cafe Induction Range": "https://images.unsplash.com/photo-1585659722993-f8d5b5e0a9e5?w=800&h=600&fit=crop&crop=bottom&q=80",
    }
    
    # Update each product with its unique image
    updated_count = 0
    for product_name, image_url in unique_images.items():
        result = await db.products.update_one(
            {"name": product_name},
            {"$set": {"image_url": image_url}}
        )
        if result.modified_count > 0:
            updated_count += 1
    
    print(f"✓ Updated {updated_count} products with unique images")
    
    # Verify - get all products and show their images
    products = await db.products.find({}, {"name": 1, "image_url": 1, "_id": 0}).to_list(100)
    
    print(f"\n📊 Total products: {len(products)}")
    
    # Check for duplicate images
    image_counts = {}
    for product in products:
        img = product.get('image_url', '')
        # Extract base URL without parameters
        base_img = img.split('?')[0] if '?' in img else img
        if base_img in image_counts:
            image_counts[base_img].append(product['name'])
        else:
            image_counts[base_img] = [product['name']]
    
    # Show duplicates if any
    duplicates = {k: v for k, v in image_counts.items() if len(v) > 1}
    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} images used by multiple products:")
        for img, products in duplicates.items():
            print(f"\n  Image: {img[:50]}...")
            for p in products:
                print(f"    - {p}")
    else:
        print("\n✅ All products have unique images!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_unique_images())
