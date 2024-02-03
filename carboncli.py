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
        "-o",
        "--output",
        type=str,
        help="Report output path",
        required=True,
    )
    parser.add_argument("website", type=str, help="The URL to analyze")

    args = parser.parse_args()
    lighthouse = (
        LighthouseService(args.output)
        if not args.lighthouse
        else LighthouseService(args.lighthouse, args.output)
    )
    website = args.website

    carbon = CarbonCalculator(lighthouse=lighthouse)
    carbon.footprint(website)

    print(carbon.to_json())

    try:
        pass
    except Exception as e:
        print(e)
