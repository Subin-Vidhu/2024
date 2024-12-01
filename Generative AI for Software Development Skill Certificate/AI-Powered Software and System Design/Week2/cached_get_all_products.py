import time
from dogpile.cache import make_region
from sqlalchemy.orm import Session

# Configure the cache region
region = make_region().configure(
    'dogpile.cache.memory',
    expiration_time=3600
)

@region.cache_on_arguments()
def get_all_products_cached():
    with Session(engine) as session:
        query = session.query(Product)
        return [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price
            } for product in query.all()
        ]

def get_all_products_uncached():
    with Session(engine) as session:
        query = session.query(Product)
        return [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price
            } for product in query.all()
        ]

def compare_execution_times(num_iterations=5):
    print(f"Comparing execution times over {num_iterations} iterations:")
    
    # Warm up the cache
    get_all_products_cached()
    
    # Test cached function
    cache_start_time = time.time()
    for _ in range(num_iterations):
        get_all_products_cached()
    cache_end_time = time.time()
    cache_total_time = cache_end_time - cache_start_time
    
    # Test uncached function
    uncache_start_time = time.time()
    for _ in range(num_iterations):
        get_all_products_uncached()
    uncache_end_time = time.time()
    uncache_total_time = uncache_end_time - uncache_start_time
    
    print(f"Cached function total time: {cache_total_time:.6f} seconds")
    print(f"Cached function average time: {cache_total_time/num_iterations:.6f} seconds")
    print(f"Uncached function total time: {uncache_total_time:.6f} seconds")
    print(f"Uncached function average time: {uncache_total_time/num_iterations:.6f} seconds")
    print(f"Speed improvement: {uncache_total_time/cache_total_time:.2f}x faster with caching")

# Run the comparison
compare_execution_times()
