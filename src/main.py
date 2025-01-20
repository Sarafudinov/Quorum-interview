import csv
from pathlib import Path
from typing import List, Dict, Any
from reader import DataReader


def process_legislators(
    legislators: List[Dict[str, str]], vote_results: List[Dict[str, str]]
) -> Dict[int, Dict[str, Any]]:
    """
    Processes legislators' voting records, calculating the number of supported and opposed bills.

    :param legislators: List of legislators with their details.
    :param vote_results: List of vote results linking legislators to their votes.
    :return: Dictionary mapping legislator IDs to their statistics.
    """
    stats: Dict[int, Dict[str, Any]] = {
        int(leg["id"]): {
            "id": int(leg["id"]),
            "name": leg["name"],
            "num_supported_bills": 0,
            "num_opposed_bills": 0,
        }
        for leg in legislators
    }

    for vote in vote_results:
        legislator_id = int(vote["legislator_id"])
        vote_type = int(vote["vote_type"])
        if legislator_id in stats:
            if vote_type == 1:
                stats[legislator_id]["num_supported_bills"] += 1
            elif vote_type == 2:
                stats[legislator_id]["num_opposed_bills"] += 1

    return stats


def process_bills(
    bills: List[Dict[str, str]],
    votes: List[Dict[str, str]],
    vote_results: List[Dict[str, str]],
    legislators: List[Dict[str, str]],
) -> Dict[int, Dict[str, Any]]:
    """
    Processes bills to count the number of supporters and opposers.

    :param bills: List of bills with their details.
    :param votes: List of votes linking to bills.
    :param vote_results: List of vote results linking legislators to votes.
    :param legislators: List of legislators.
    :return: Dictionary mapping bill IDs to their statistics.
    """
    stats: Dict[int, Dict[str, Any]] = {
        int(bill["id"]): {
            "id": int(bill["id"]),
            "title": bill["title"],
            "primary_sponsor": "Unknown",
            "supporter_count": 0,
            "opposer_count": 0,
        }
        for bill in bills
    }

    # Map legislator IDs to names for primary sponsor lookup
    sponsor_map: Dict[int, str] = {int(leg["id"]): leg["name"] for leg in legislators}
    for bill in bills:
        bill_id = int(bill["id"])
        sponsor_id = int(bill["sponsor_id"])
        stats[bill_id]["primary_sponsor"] = sponsor_map.get(sponsor_id, "Unknown")

    # Map vote IDs to bill IDs
    vote_map: Dict[int, int] = {int(vote["id"]): int(vote["bill_id"]) for vote in votes}

    for vote in vote_results:
        vote_id = int(vote["vote_id"])
        bill_id = vote_map.get(vote_id)
        vote_type = int(vote["vote_type"])
        if bill_id in stats:
            if vote_type == 1:
                stats[bill_id]["supporter_count"] += 1
            elif vote_type == 2:
                stats[bill_id]["opposer_count"] += 1

    return stats


def write_csv(
    file_path: Path, data: Dict[int, Dict[str, Any]], fieldnames: List[str]
) -> None:
    """
    Writes processed data to a CSV file.

    :param file_path: Path to the output CSV file.
    :param data: Dictionary of data to write.
    :param fieldnames: List of field names for the CSV.
    """
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)


if __name__ == "__main__":
    # Define base directories
    base_dir: Path = Path(__file__).resolve().parent.parent  # Project root
    data_dir: Path = base_dir / "data"
    output_dir: Path = base_dir / "output"

    # Ensure the output directory exists
    output_dir.mkdir(exist_ok=True)

    # Read input data from CSV files
    legislators: List[Dict[str, str]] = DataReader.read_csv(
        data_dir / "legislators.csv"
    )
    bills: List[Dict[str, str]] = DataReader.read_csv(data_dir / "bills.csv")
    votes: List[Dict[str, str]] = DataReader.read_csv(data_dir / "votes.csv")
    vote_results: List[Dict[str, str]] = DataReader.read_csv(
        data_dir / "vote_results.csv"
    )

    # Process the data
    legislator_stats: Dict[int, Dict[str, Any]] = process_legislators(
        legislators, vote_results
    )
    bill_stats: Dict[int, Dict[str, Any]] = process_bills(
        bills, votes, vote_results, legislators
    )

    # Write results to CSV files
    write_csv(
        output_dir / "legislators-support-oppose-count.csv",
        legislator_stats,
        ["id", "name", "num_supported_bills", "num_opposed_bills"],
    )
    write_csv(
        output_dir / "bills-support-oppose-count.csv",
        bill_stats,
        ["id", "title", "supporter_count", "opposer_count", "primary_sponsor"],
    )
