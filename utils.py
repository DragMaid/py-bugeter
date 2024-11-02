from datetime import date
import gspread

SHEET_ID   = "1jQKlCuGA-Q4RVlBI11webRfmhbYfixtbcKzGelmJE-A"
CLIENT_ID = "138101106363-5m2v4m0qfkh7gjn4kh6p2g9bnragq9cd.apps.googleusercontent.com"

# SHEET_NAME = "september-2024"
CREADENTIAL_PATH = "./client_secret.json"

GOOGLE_ACCOUNT = gspread.oauth(credentials_filename = CREADENTIAL_PATH) #type: ignore
GOOGLE_SHEET   = GOOGLE_ACCOUNT.open_by_key(SHEET_ID)

TODAY_MONTH = date.today().strftime("%B").lower() 
TODAY_YEAR  = date.today().strftime("%Y")

USERS = ["Binh", "Hoang"]
STATUSES = ["Paid", "Pending"]
PAID_FOR_OPTIONS = USERS + ["Both"]

# | date | product | category | cost | status | paid_for | paid_by
STRUCTURE_DICT = {"date": 0, "product": 1, "category": 2,  "cost": 3, "paid for": 4, "paid by": 5}
FILTER_TYPES = ["Paid by", "Paid for", "Cost - Low to High", "Cost - High to Low"]


class sheet_manager:
    def __init__(self):
        self.active_worksheet = self.get_latest_worksheet()

    def get_element_index(self, element):
        return STRUCTURE_DICT[element]

    def get_data_by_name(self, data, name):
        return data[STRUCTURE_DICT[name.lower()]]

    def get_latest_worksheet(self):
        return GOOGLE_SHEET.worksheets()[0]

    def get_sheet_format(self, month = TODAY_MONTH, year = TODAY_YEAR):
        return f"{month}-{year}"

    def get_last_sheet_date(self):
        last_sheet_name = GOOGLE_SHEET.worksheets()[-1].title.lower()
        last_date = last_sheet_name.split("-")
        return {"month": last_date[0], "year": last_date[1]}

    def set_active_worksheet(self, worksheet):
        self.active_worksheet = worksheet

    def create_new_month_sheet(self):
        last_date = self.get_last_sheet_date()
        if (TODAY_MONTH != last_date["month"] or
            TODAY_YEAR != last_date["year"]):
            self.active_worksheet.duplicate(new_sheet_name = self.get_sheet_format()) 
            new_sheet = self.get_latest_worksheet()
            new_sheet.clear()

    def get_active_rows(self):
        return len(self.active_worksheet.get_all_values())

    def get_active_worksheet_data(self):
        return self.active_worksheet.get_all_values()[1:]

    def get_today_format(self):
        return date.today().strftime("%m/%d/%Y")

    def create_entry(self, Date = "", expense = "",
                    cost = 0, status = "", paid_for = "",
                    paid_by = ""):
        if Date == "": Date  = self.get_today_format()
        row_index = self.get_active_rows() + 1
        work_range = f"A{row_index}:G{row_index}"
        work_data = [[Date, expense, cost, status,  paid_for, paid_by]]
        self.active_worksheet.update(work_data, work_range)

    def delete_entry(self, index):
        self.active_worksheet.delete_rows(index)

    def calculate_with_filter(self, filter = None, target = ""):
        data = active_worksheet.get_all_values(value_render_option=gspread.utils.ValueRenderOption.unformatted) #type: ignore
        total_cost = 0
        if not filter:
            for index in range(1, len(data)):
                total_cost += float(data[index][self.get_element_index("Cost")])
        else:
            for index in range(1, len(data)):
                if target == data[index][self.get_element_index(filter)]:
                    total_cost += float(data[index][self.get_element_index("Cost")])

        return round(total_cost, 2)
