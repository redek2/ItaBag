import gpxpy

def parse_gpx_file(file_path: str) -> dict:
    """
    Parses a GPX file and extracts relevant information.

    Args:
        file_path (str): The path to the GPX file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

            uphill = gpx.get_uphill_downhill()[0]
            duration = gpx.get_duration()

            # Extract relevant information from the GPX file
            distance_km = round(gpx.length_3d() / 1000, 2)  # Convert meters to kilometers
            elevation_gain_m = int(round(uphill)) if uphill is not None else None
            duration_minutes = int(round(duration / 60)) if duration is not None else None  # Convert seconds to minutes

            return {
                "distance_km": distance_km,
                "elevation_gain_m": elevation_gain_m,
                "duration_minutes": duration_minutes
            }
    except Exception as e:
        # Handle exceptions (e.g., file not found, parsing error)
        print(f"Error parsing GPX file: {e}")
        raise ValueError("Failed to parse GPX file. Please ensure the file is valid and try again.")