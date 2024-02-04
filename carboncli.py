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
        "-u",
        "--users",
        type=int,
        help="(Optional) - Estimated number of users your site experiences",
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
        if args.users:
            carbon = CarbonCalculator(lighthouse=lighthouse, users=args.users)
        else:
            carbon = CarbonCalculator(lighthouse=lighthouse, users=1000)
        carbon.footprint(website)

        print(carbon.to_json())
    except Exception as e:
        print(e)
