import json
import os
from pathlib import Path
from datetime import datetime

def ensure_data_directory():
    """Ensure the data directory exists"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir

def read_json(filename):
    """Read JSON data from file with error handling"""
    try:
        file_path = Path(filename)
        if not file_path.exists():
            # Return empty list if file doesn't exist
            return []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if data is not None else []
    except json.JSONDecodeError as e:
        print(f"Error reading {filename}: Invalid JSON format - {e}")
        return []
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []

def write_json(filename, data):
    """Write JSON data to file with error handling"""
    try:
        # Ensure directory exists
        file_path = Path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error writing to {filename}: {e}")
        return False

def initialize_default_data():
    """Initialize default data files if they don't exist"""
    ensure_data_directory()
    
    # Default users
    users_file = "data/users.json"
    if not Path(users_file).exists():
        default_users = [
            {
                "username": "admin",
                "password": "admin123",
                "email": "admin@aweelectronics.com",
                "role": "admin",
                "full_name": "System Administrator",
                "created_date": datetime.now().isoformat()
            },
            {
                "username": "customer1",
                "password": "customer123",
                "email": "customer@example.com",
                "role": "customer",
                "full_name": "John Customer",
                "address": "123 Main St, Melbourne VIC 3000",
                "phone_number": "0400000001",
                "cart": [],
                "created_date": datetime.now().isoformat()
            },
            {
                "username": "saqib",
                "password": "saqib1",
                "email": "saqibsoomro@gmail.com",
                "role": "customer",
                "full_name": "Saqib Soomro",
                "address": "4 Kelebel Street",
                "phone_number": "0456456456",
                "cart": [],
                "created_date": datetime.now().isoformat()
            }
        ]
        write_json(users_file, default_users)
        print(f"✅ Created {users_file} with default user accounts")
    
    # Default products
    products_file = "data/products.json"
    if not Path(products_file).exists():
        default_products = [
            {
                "product_id": "P001",
                "name": "Gaming Laptop Pro",
                "price": 1299.99,
                "category": "Computers",
                "stock": 15,
                "description": "High-performance gaming laptop with RTX graphics",
                "created_date": datetime.now().isoformat()
            },
            {
                "product_id": "P002",
                "name": "Wireless Bluetooth Speaker",
                "price": 89.99,
                "category": "Audio",
                "stock": 25,
                "description": "Premium wireless speaker with crystal clear sound",
                "created_date": datetime.now().isoformat()
            },
            {
                "product_id": "P003",
                "name": "Mechanical Gaming Keyboard",
                "price": 149.99,
                "category": "Accessories",
                "stock": 20,
                "description": "RGB mechanical keyboard with cherry MX switches",
                "created_date": datetime.now().isoformat()
            },
            {
                "product_id": "P004",
                "name": "4K Webcam Ultra",
                "price": 199.99,
                "category": "Accessories",
                "stock": 12,
                "description": "Professional 4K webcam for streaming and video calls",
                "created_date": datetime.now().isoformat()
            },
            {
                "product_id": "P005",
                "name": "Smartphone Case Premium",
                "price": 29.99,
                "category": "Cases",
                "stock": 50,
                "description": "Durable premium case with shock protection",
                "created_date": datetime.now().isoformat()
            },
            {
                "product_id": "P006",
                "name": "Wireless Mouse Pro",
                "price": 79.99,
                "category": "Accessories",
                "stock": 30,
                "description": "Ergonomic wireless mouse with precision tracking",
                "created_date": datetime.now().isoformat()
            },
            {
                "product_id": "P007",
                "name": "USB-C Hub Multi-Port",
                "price": 59.99,
                "category": "Accessories",
                "stock": 18,
                "description": "7-in-1 USB-C hub with HDMI, USB 3.0, and SD card slots",
                "created_date": datetime.now().isoformat()
            },
            {
                "product_id": "P008",
                "name": "Noise-Cancelling Headphones",
                "price": 249.99,
                "category": "Audio",
                "stock": 8,
                "description": "Premium noise-cancelling headphones with 30-hour battery",
                "created_date": datetime.now().isoformat()
            }
        ]
        write_json(products_file, default_products)
        print(f"✅ Created {products_file} with default product catalog")
    
    # Default orders (empty)
    orders_file = "data/orders.json"
    if not Path(orders_file).exists():
        write_json(orders_file, [])
        print(f"✅ Created {orders_file} for order storage")
    
    # Check if all files exist now
    all_files_exist = all(Path(f"data/{filename}").exists() for filename in ["users.json", "products.json", "orders.json"])
    
    if all_files_exist:
        print("✅ All data files initialized successfully!")
        return True
    else:
        print("❌ Some data files failed to initialize")
        return False

def backup_data():
    """Create backup of all data files"""
    try:
        backup_dir = Path("data/backups")
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        data_files = ["users.json", "products.json", "orders.json"]
        
        for filename in data_files:
            source_path = Path(f"data/{filename}")
            if source_path.exists():
                backup_path = backup_dir / f"{filename.replace('.json', '')}_{timestamp}.json"
                
                with open(source_path, 'r', encoding='utf-8') as source:
                    data = json.load(source)
                
                with open(backup_path, 'w', encoding='utf-8') as backup:
                    json.dump(data, backup, indent=4, ensure_ascii=False)
                
                print(f"✅ Backed up {filename} to {backup_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def restore_data(backup_timestamp):
    """Restore data from backup"""
    try:
        backup_dir = Path("data/backups")
        if not backup_dir.exists():
            print("❌ No backups directory found")
            return False
        
        data_files = ["users.json", "products.json", "orders.json"]
        
        for filename in data_files:
            backup_filename = filename.replace('.json', f'_{backup_timestamp}.json')
            backup_path = backup_dir / backup_filename
            
            if backup_path.exists():
                with open(backup_path, 'r', encoding='utf-8') as backup:
                    data = json.load(backup)
                
                write_json(f"data/{filename}", data)
                print(f"✅ Restored {filename} from {backup_filename}")
            else:
                print(f"⚠️ Backup file {backup_filename} not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False

def get_data_stats():
    """Get statistics about data files"""
    stats = {}
    
    try:
        # Users stats
        users = read_json("data/users.json")
        stats['users'] = {
            'total': len(users),
            'admin': len([u for u in users if u.get('role') == 'admin']),
            'customers': len([u for u in users if u.get('role') == 'customer'])
        }
        
        # Products stats
        products = read_json("data/products.json")
        stats['products'] = {
            'total': len(products),
            'in_stock': len([p for p in products if p.get('stock', 0) > 0]),
            'low_stock': len([p for p in products if 0 < p.get('stock', 0) <= 5]),
            'out_of_stock': len([p for p in products if p.get('stock', 0) == 0])
        }
        
        # Orders stats
        orders = read_json("data/orders.json")
        stats['orders'] = {
            'total': len(orders),
            'total_revenue': sum(order.get('order', {}).get('total', 0) for order in orders)
        }
        
    except Exception as e:
        print(f"Error getting stats: {e}")
    
    return stats

def validate_data_integrity():
    """Validate data integrity across all files"""
    issues = []
    
    try:
        # Check users
        users = read_json("data/users.json")
        for user in users:
            if not user.get('username'):
                issues.append("User found without username")
            if not user.get('role'):
                issues.append(f"User {user.get('username', 'unknown')} has no role")
        
        # Check products
        products = read_json("data/products.json")
        product_ids = []
        for product in products:
            pid = product.get('product_id')
            if not pid:
                issues.append("Product found without product_id")
            elif pid in product_ids:
                issues.append(f"Duplicate product_id: {pid}")
            else:
                product_ids.append(pid)
        
        # Check orders
        orders = read_json("data/orders.json")
        for i, order_data in enumerate(orders):
            order = order_data.get('order', {})
            if not order.get('order_id'):
                issues.append(f"Order {i} has no order_id")
            if not order.get('user_id'):
                issues.append(f"Order {i} has no user_id")
        
    except Exception as e:
        issues.append(f"Error during validation: {e}")
    
    return issues

# Legacy function names for backward compatibility
def create_default_data():
    """Legacy function name - calls initialize_default_data"""
    return initialize_default_data()

def setup_data_files():
    """Legacy function name - calls initialize_default_data"""
    return initialize_default_data()

if __name__ == "__main__":
    """Test the file handler functionality"""
    print("🧪 Testing file handler...")
    
    # Test initialization
    if initialize_default_data():
        print("✅ Data initialization successful")
    else:
        print("❌ Data initialization failed")
    
    # Test stats
    stats = get_data_stats()
    print(f"📊 Data stats: {stats}")
    
    # Test validation
    issues = validate_data_integrity()
    if issues:
        print(f"⚠️ Data integrity issues: {issues}")
    else:
        print("✅ Data integrity check passed")