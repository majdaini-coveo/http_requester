def generate_hierarchy(path: str):
    elements = path.split('|')
    return ['|'.join(elements[:i+1]) for i in range(len(elements))]

def transform_categories(categories):
    transformed = []
    for path in categories:
        parts = path.split('/')
        transformed_path = parts[0].capitalize()
        for part in parts[1:]:
            transformed_path += '|' + part.capitalize()
        transformed += generate_hierarchy(transformed_path)
    return transformed

# Example usage:
categories = [
    "Home-living/Badezimmer/Badtextilien/Bad-kapuzenbadetuecher",
    "Home-living/Heimtextilien/Heimtextilien-badematten",
    "Home-living/Heimtextilien/Heimtextilien-badematten/Kapuzenbadetuecher",
    "Sale/Sale-home-living",
    "Sale/Sale-home-living/Sale-home-living-heimtextilien"
]
output = transform_categories(categories)
print(output)