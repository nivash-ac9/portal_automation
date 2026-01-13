import csv
import os
from datetime import datetime
from utils.project_paths import RESULTS_DIR, SUMMARY_DIR

class CSVWriter:

    @staticmethod
    def write_results(page, df, actuals, statuses):
        os.makedirs(RESULTS_DIR, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(RESULTS_DIR, f"{page}_{ts}.csv")

        headers = list(df.columns) + ["actual_result", "status"]

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for i in range(len(df)):
                writer.writerow(
                    list(df.iloc[i].values) +
                    [actuals[i], statuses[i]]
                )

    @staticmethod
    def write_summary(page, total, passed, failed, passed_ids, failed_ids):
        os.makedirs(SUMMARY_DIR, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(
            SUMMARY_DIR,
            f"{page}_summary_{ts}.csv"
        )

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Total",
                "Passed",
                "Failed",
                "Passed_Testcase_IDs",
                "Failed_Testcase_IDs"
            ])
            writer.writerow([
                total,
                passed,
                failed,
                ", ".join(filter(None, passed_ids)),
                ", ".join(filter(None, failed_ids))
            ])

