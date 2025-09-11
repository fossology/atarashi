#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2025 Rajul Jha (rajuljha49@gmail.com)

SPDX-License-Identifier: GPL-2.0

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import argparse
import os
import csv
import zipfile
import tempfile
from atarashi.agents.keywordAgent import KeywordAgent

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

def evaluate_folder(folder_path, agent, output_path, verbose=0):
    """
    Scans a folder and writes the results to a CSV file.
    
    :param: folder_path: to evaluate
    :param: KeywordAgent object
    :param: output_path: Path to save the result csv to.
    :param: verbose Whether to get verbose output or not.
    """
    results = []
    file_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, start=folder_path)

            # Skip macOS system files and resource forks
            if "__MACOSX" in relative_file_path or os.path.basename(file).startswith("._"):
                continue
            if file_path.endswith(".zip"):
                continue

            file_list.append(file_path)

    if TQDM_AVAILABLE:
        iterator = tqdm(file_list, desc="Scanning files", unit="file")
    else:
        iterator = file_list

    for file_path in iterator:
        scan_results = agent.scan(file_path)
        relative_file_path = os.path.relpath(file_path, start=folder_path)
        if scan_results:
            for result in scan_results:
                results.append({
                    "file": relative_file_path,
                    "detected": True,
                    "matched_keywords": result.get("description", "")
                })
        else:
            results.append({
                "file": relative_file_path,
                "detected": False,
                "matched_keywords": ""
            })
        if verbose:
            print(f"Scanned {file_path}: Detected={bool(scan_results)}")

    # Write results to CSV
    with open(output_path, "w", newline="") as csvfile:
        fieldnames = ["file", "detected", "matched_keywords"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"Results written to {output_path}")


def print_results_summary(csv_path):
    """
    Reads the results CSV and prints a summary of detection accuracy.
    :param: Path to the CSV file to evaluate Keyword results.
    """
    total = 0
    detected_correct = 0
    detected_wrong = 0

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            total += 1
            detected = row["detected"].strip().lower() == "true"
            file_path = row["file"]

            if detected:
                detected_correct += 1
            else:
                if "No_license_found" in file_path:
                    detected_correct += 1
                else:
                    detected_wrong += 1

    accuracy = (detected_correct / total) * 100 if total > 0 else 0

    print("\n--- Scan Summary ---")
    print(f"Total files scanned: {total}")
    print(f"Detected Correctly: {detected_correct}")
    print(f"Detected Wrongly: {detected_wrong}")
    print(f"Accuracy: {accuracy:.2f}%")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    default_zip = os.path.join(script_dir, "NomosTestFiles.zip")
    default_output = os.path.join(script_dir, "keyword_results.csv")

    parser = argparse.ArgumentParser(description="Evaluate KeywordAgent on a folder or zip file and store results in CSV.")
    parser.add_argument("input_path", nargs='?', default=default_zip,
                        help=f"Path to the folder or .zip file to scan. Defaults to {default_zip}")
    parser.add_argument("-o", "--output", default=default_output,
                        help=f"Output CSV file (default: {default_output})")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increase output verbosity.")
    args = parser.parse_args()

    agent = KeywordAgent(verbose=args.verbose)
    input_path = os.path.expanduser(args.input_path)

    if input_path.endswith('.zip'):
        if not os.path.exists(input_path):
            print(f"Error: Default zip file not found at {input_path}")
            return
        
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Extracting {input_path} to a temporary directory...")
            with zipfile.ZipFile(input_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            print("Extraction complete. Starting scan...")
            evaluate_folder(temp_dir, agent, args.output, args.verbose)
        print("Temporary directory has been removed.")
        print_results_summary(args.output)

    elif os.path.isdir(input_path):
        evaluate_folder(input_path, agent, args.output, args.verbose)
        print_results_summary(args.output)
    else:
        print(f"Error: The specified path is not a valid directory or .zip file: {input_path}")


if __name__ == "__main__":
    main()
