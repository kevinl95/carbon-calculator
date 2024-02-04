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

        print(carbon.to_json())
    except Exception as e:
        print(e)
