import os
import csv
from pathlib import Path
from typing import List, Dict, Any
from reader import DataReader


def process_data(
    data_type: str,  # 'legislators' or 'bills'
    items: List[Dict[str, str]],
    votes: List[Dict[str, str]],
    vote_results: List[Dict[str, str]],
    legislators: List[Dict[str, str]] = None,  # Added to get sponsor names for bills
) -> Dict[int, Dict[str, Any]]:
    """
    Processes data for either legislators or bills' support and opposition.

    :param data_type: The type of data to process ('legislators' or 'bills').
    :param items: List of items (legislators or bills).
    :param votes: List of votes.
    :param vote_results: List of vote results.
    :param legislators: List of legislators (only required for processing bills to get sponsor names).
    :return: Dictionary with either legislator or bill statistics.
    """
    if data_type == "legislators":
        stats = {
            int(item["id"]): {
                "id": int(item["id"]),
                "name": item["name"],
                "num_supported_bills": 0,
                "num_opposed_bills": 0,
            }
            for item in items
        }
    elif data_type == "bills":
        stats = {
            int(item["id"]): {
                "id": int(item["id"]),
                "title": item["title"],
                "primary_sponsor": item["sponsor_id"],
                "num_supporting_legislators": 0,
                "num_opposing_legislators": 0,
            }
            for item in items
        }

        # Add sponsor names to bills
        if legislators:
            sponsor_map = {int(leg["id"]): leg["name"] for leg in legislators}
            for bill in stats.values():
                bill["primary_sponsor"] = sponsor_map.get(
                    bill["primary_sponsor"], "Unknown"
                )
    else:
        raise ValueError("Invalid data_type, should be 'legislators' or 'bills'.")

    # Map votes to their results
    vote_map: Dict[int, Dict[str, str]] = {
        int(vote_result["vote_id"]): vote_result for vote_result in vote_results
    }

    # Process votes and update stats
    for vote in votes:
        vote_id = int(vote["id"])
        if vote_id in vote_map:
            vote_type = int(vote_map[vote_id]["vote_type"])
            if data_type == "legislators":
                item_id = int(vote_map[vote_id]["legislator_id"])
                if vote_type == 1:  # Yes
                    stats[item_id]["num_supported_bills"] += 1
                elif vote_type == 2:  # No
                    stats[item_id]["num_opposed_bills"] += 1
            elif data_type == "bills":
                item_id = int(vote["bill_id"])
                if vote_type == 1:  # Yes
                    stats[item_id]["num_supporting_legislators"] += 1
                elif vote_type == 2:  # No
                    stats[item_id]["num_opposing_legislators"] += 1

    return stats


def write_csv(
    file_path: Path, data: Dict[int, Dict[str, Any]], fieldnames: List[str]
) -> None:
    """
    Writes data to a CSV file.

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
    # Dynamically determine paths
    base_dir = Path(__file__).resolve().parent.parent  # Navigate to project root
    data_dir = base_dir / "data"
    output_dir = base_dir / "output"

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    # Reading data
    legislators: List[Dict[str, str]] = DataReader.read_csv(
        data_dir / "legislators.csv"
    )
    bills: List[Dict[str, str]] = DataReader.read_csv(data_dir / "bills.csv")
    votes: List[Dict[str, str]] = DataReader.read_csv(data_dir / "votes.csv")
    vote_results: List[Dict[str, str]] = DataReader.read_csv(
        data_dir / "vote_results.csv"
    )

    # Process data
    legislator_stats: Dict[int, Dict[str, Any]] = process_data(
        "legislators", legislators, votes, vote_results
    )
    bill_stats: Dict[int, Dict[str, Any]] = process_data(
        "bills", bills, votes, vote_results, legislators
    )

    # Write outputs
    write_csv(
        output_dir / "legislators-support-oppose-count.csv",
        legislator_stats,
        ["id", "name", "num_supported_bills", "num_opposed_bills"],
    )
    write_csv(
        output_dir / "bills-support-oppose-count.csv",
        bill_stats,
        [
            "id",
            "title",
            "primary_sponsor",
            "num_supporting_legislators",
            "num_opposing_legislators",
        ],
    )
