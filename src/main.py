import os
import csv
from pathlib import Path
from typing import List, Dict, Any
from reader import DataReader


def process_legislators_data(
    legislators: List[Dict[str, str]],
    bills: List[Dict[str, str]],
    votes: List[Dict[str, str]],
    vote_results: List[Dict[str, str]]
) -> Dict[int, Dict[str, Any]]:
    """
    Processes data for legislators' support and opposition.
    
    :param legislators: List of legislators.
    :param bills: List of bills.
    :param votes: List of votes.
    :param vote_results: List of vote results.
    :return: Dictionary with legislator statistics.
    """
    legislator_stats: Dict[int, Dict[str, Any]] = {
        int(legislator['id']): {'id': int(legislator['id']), 'name': legislator['name'], 'num_supported_bills': 0, 'num_opposed_bills': 0}
        for legislator in legislators
    }

    # Map votes to their results
    vote_map: Dict[int, Dict[str, str]] = {int(vote_result['vote_id']): vote_result for vote_result in vote_results}

    # Process legislator votes
    for vote in votes:
        vote_id = int(vote['id'])
        if vote_id in vote_map:
            legislator_id = int(vote_map[vote_id]['legislator_id'])
            vote_type = int(vote_map[vote_id]['vote_type'])
            if vote_type == 1:  # Yea
                legislator_stats[legislator_id]['num_supported_bills'] += 1
            elif vote_type == 2:  # Nay
                legislator_stats[legislator_id]['num_opposed_bills'] += 1

    return legislator_stats


def process_bills_data(
    bills: List[Dict[str, str]],
    votes: List[Dict[str, str]],
    vote_results: List[Dict[str, str]]
) -> Dict[int, Dict[str, Any]]:
    """
    Processes data for bills' support and opposition.
    
    :param bills: List of bills.
    :param votes: List of votes.
    :param vote_results: List of vote results.
    :return: Dictionary with bill statistics.
    """
    bill_stats: Dict[int, Dict[str, Any]] = {
        int(bill['id']): {'id': int(bill['id']), 'title': bill['title'], 'primary_sponsor': bill['sponsor_id'], 'num_supporting_legislators': 0, 'num_opposing_legislators': 0}
        for bill in bills
    }

    # Map votes to their results
    vote_map: Dict[int, Dict[str, str]] = {int(vote_result['vote_id']): vote_result for vote_result in vote_results}

    # Process bill votes
    for vote in votes:
        bill_id = int(vote['bill_id'])
        vote_id = int(vote['id'])
        if vote_id in vote_map:
            vote_type = int(vote_map[vote_id]['vote_type'])
            if vote_type == 1:  # Yea
                bill_stats[bill_id]['num_supporting_legislators'] += 1
            elif vote_type == 2:  # Nay
                bill_stats[bill_id]['num_opposing_legislators'] += 1

    return bill_stats


def write_csv(file_path: Path, data: Dict[int, Dict[str, Any]], fieldnames: List[str]) -> None:
    """
    Writes data to a CSV file.
    
    :param file_path: Path to the output CSV file.
    :param data: Dictionary of data to write.
    :param fieldnames: List of field names for the CSV.
    """
    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)


if __name__ == '__main__':
    # Dynamically determine paths
    base_dir = Path(__file__).resolve().parent.parent  # Navigate to project root
    data_dir = base_dir / 'data'
    output_dir = base_dir / 'output'

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    # Reading data
    legislators: List[Dict[str, str]] = DataReader.read_csv(data_dir / 'legislators.csv')
    bills: List[Dict[str, str]] = DataReader.read_csv(data_dir / 'bills.csv')
    votes: List[Dict[str, str]] = DataReader.read_csv(data_dir / 'votes.csv')
    vote_results: List[Dict[str, str]] = DataReader.read_csv(data_dir / 'vote_results.csv')

    # Process data
    legislator_stats: Dict[int, Dict[str, Any]] = process_legislators_data(legislators, bills, votes, vote_results)
    bill_stats: Dict[int, Dict[str, Any]] = process_bills_data(bills, votes, vote_results)

    # Write outputs
    write_csv(
        output_dir / 'legislators-support-oppose-count.csv',
        legislator_stats,
        ['id', 'name', 'num_supported_bills', 'num_opposed_bills']
    )
    write_csv(
        output_dir / 'bills-support-oppose-count.csv',
        bill_stats,
        ['id', 'title', 'primary_sponsor', 'num_supporting_legislators', 'num_opposing_legislators']
    )
