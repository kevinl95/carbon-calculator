import argparse
from carbon.calculator import CarbonCalculator
from carbon.services import LighthouseService


def main():
    """ """
    parser = argparse.ArgumentParser(
        description="Carbon Calculator - the tool calculates the carbon emissions (CO2) and green infos of any website"
    )

    parser.add_argument(
        "-lh",
        "--lighthouse",
        type=str,
        help="(Optional) - The path of the Lighthouse tool",
        required=False,
    )

    parser.add_argument(
        "-r",
        "--requests",
        type=int,
        help="(Optional) - Estimated number of requests your site experiences",
        required=False,
    )
    parser.add_argument("website", type=str, help="The URL to analyze")

    args = parser.parse_args()

    try:
        lighthouse = (
            LighthouseService()
            if not args.lighthouse
            else LighthouseService(args.lighthouse)
        )
        website = args.website
        if args.requests:
            carbon = CarbonCalculator(lighthouse=lighthouse, reqs=args.requests)
        else:
            carbon = CarbonCalculator(lighthouse=lighthouse, reqs=10000)
        carbon.footprint(website)
        f = open("badge.svg", "w")
        if carbon.hosting_green:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="130" height="20" role="img" aria-label="Green Webhost: True"><title>Green Webhost: True</title><linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient><clipPath id="r"><rect width="130" height="20" rx="3" fill="#fff"/></clipPath><g clip-path="url(#r)"><rect width="95" height="20" fill="#555"/><rect x="95" width="35" height="20" fill="#97ca00"/><rect width="130" height="20" fill="url(#s)"/></g><g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110"><text aria-hidden="true" x="485" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="850">Green Webhost</text><text x="485" y="140" transform="scale(.1)" fill="#fff" textLength="850">Green Webhost</text><text aria-hidden="true" x="1115" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="250">True</text><text x="1115" y="140" transform="scale(.1)" fill="#fff" textLength="250">True</text></g></svg>')
        else:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="134" height="20" role="img" aria-label="Green Webhost: False"><title>Green Webhost: False</title><linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient><clipPath id="r"><rect width="134" height="20" rx="3" fill="#fff"/></clipPath><g clip-path="url(#r)"><rect width="95" height="20" fill="#555"/><rect x="95" width="39" height="20" fill="#e05d44"/><rect width="134" height="20" fill="url(#s)"/></g><g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110"><text aria-hidden="true" x="485" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="850">Green Webhost</text><text x="485" y="140" transform="scale(.1)" fill="#fff" textLength="850">Green Webhost</text><text aria-hidden="true" x="1135" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="290">False</text><text x="1135" y="140" transform="scale(.1)" fill="#fff" textLength="290">False</text></g></svg>')
        f.close()
        # Write metrics
        f = open("metrics.txt", "w")
        f.write(carbon.to_string())
        f.close()
        print(carbon.to_json())
    except Exception as e:
        print(e)
