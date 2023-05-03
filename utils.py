def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join("[{}, {}]".format(p.x, p.y) for p in polygon)


def format_bounding_region(bounding_region):
    if not bounding_region:
        return "N/A"
    return ", ".join("Page #{}: {}".format(
                    region.page_number, format_polygon(region.polygon)
                    )for region in bounding_region
                    )