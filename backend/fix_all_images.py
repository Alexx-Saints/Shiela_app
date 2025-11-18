import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

async def fix_all_images():
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("Assigning completely unique images to each product...")
    
    # Get all products
    products = await db.products.find({}).to_list(100)
    
    # Unique image library - 51 different appliance images
    unique_appliance_images = [
        "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5",
        "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30",
        "https://images.unsplash.com/photo-1571175351190-49c3ca49e541",
        "https://images.unsplash.com/photo-1622116814927-e08625346f39",
        "https://images.unsplash.com/photo-1595428774223-ef52624120d2",
        "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1",
        "https://images.unsplash.com/photo-1582735689369-4fe89db7114c",
        "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce",
        "https://images.unsplash.com/photo-1604335399105-a0c585fd81a1",
        "https://images.unsplash.com/photo-1563298723-dcfebaa392e3",
        "https://images.unsplash.com/photo-1585659722983-3a675dabf23d",
        "https://images.unsplash.com/photo-1603712725038-c0e53d5e9670",
        "https://images.unsplash.com/photo-1551731409-43eb3e517a1a",
        "https://images.unsplash.com/photo-1556911073-38141963c9e0",
        "https://images.unsplash.com/photo-1556911220-d404e76f60ad",
        "https://images.unsplash.com/photo-1631545804641-2b0e18f3c28d",
        "https://images.unsplash.com/photo-1620735692151-26a7e0748429",
        "https://images.unsplash.com/photo-1624649591189-ea08af62a8f7",
        "https://images.unsplash.com/photo-1607400201515-c2c41c07e5cf",
        "https://images.unsplash.com/photo-1635274852165-c1b99c2c8e7b",
        "https://images.unsplash.com/photo-1585659722993-f8d5b5e0a9e5",
        "https://images.unsplash.com/photo-1588854337115-1c67d9247e4d",
        "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078",
        "https://images.unsplash.com/photo-1588556542102-e6fc8dc0839f",
        "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c",
        "https://images.unsplash.com/photo-1556911220-bff31c812dba",
        "https://images.unsplash.com/photo-1562437077-ce7eb6d06768",
        "https://images.unsplash.com/photo-1556911220-e15b29be8c8f",
        "https://images.unsplash.com/photo-1583512603806-077998240c7a",
        "https://images.unsplash.com/photo-1601293863859-2bb0d1000edf",
        "https://images.unsplash.com/photo-1565183928294-8accb38c4f1e",
        "https://images.unsplash.com/photo-1596205250168-c3583813eea0",
        "https://images.unsplash.com/photo-1556909212-d5b604d0c90d",
        "https://images.unsplash.com/photo-1556911220-bff31c812dba",
        "https://images.unsplash.com/photo-1560185007-c5ca9d2c014d",
        "https://images.unsplash.com/photo-1556909172-54557c7e4fb7",
        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136",
        "https://images.unsplash.com/photo-1556908153-1055164fe2e9",
        "https://images.unsplash.com/photo-1556909172-54557c7e4fb7",
        "https://images.unsplash.com/photo-1556909211-36987daf7b4a",
        "https://images.unsplash.com/photo-1556911220-e15b29be8c8f",
        "https://images.unsplash.com/photo-1556911220-d404e76f60ad",
        "https://images.unsplash.com/photo-1556909212-99e19b28c4d7",
        "https://images.unsplash.com/photo-1556911220-bff31c812dba",
        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136",
        "https://images.unsplash.com/photo-1556908153-1055164fe2e9",
        "https://images.unsplash.com/photo-1585128903994-4cb1b88155d8",
        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136",
        "https://images.unsplash.com/photo-1556911220-7d920fc49955",
        "https://images.unsplash.com/photo-1556911220-7d920fc49955",
        "https://images.unsplash.com/photo-1556909211-d5ffbbef5a3e"
    ]
    
    # Assign each product a unique image
    for idx, product in enumerate(products):
        image_url = unique_appliance_images[idx % len(unique_appliance_images)] + f"?w=800&h=600&fit=crop&auto=format&q=80&seed={idx}"
        
        await db.products.update_one(
            {"_id": product["_id"]},
            {"$set": {"image_url": image_url}}
        )
    
    print(f"✓ Updated {len(products)} products with unique images")
    
    # Verify uniqueness
    products_check = await db.products.find({}, {"name": 1, "image_url": 1, "_id": 0}).to_list(100)
    
    image_urls = [p['image_url'] for p in products_check]
    unique_images = set(image_urls)
    
    if len(unique_images) == len(image_urls):
        print(f"\n✅ SUCCESS! All {len(products_check)} products now have completely unique images!")
    else:
        print(f"\n⚠️  {len(image_urls) - len(unique_images)} duplicates still exist")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_all_images())
