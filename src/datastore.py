import gspread


class DataStore:
    _data = []
    worksheet_name = "web3-bot"
    gc = gspread.oauth(credentials_filename="credential.json", flow={"port": 8000})
    ws: gspread.Worksheet

    try:
        sh = gc.open(worksheet_name)
    except gspread.SpreadsheetNotFound:
        sh = gc.create(worksheet_name)

    def __init__(self, sheet_name, cols) -> None:
        self.sheet_name = sheet_name
        self.cols = cols

        self.add_worksheet()
        self._data = self.ws.get_all_values()

        # print(self.data)

    def add_worksheet(self):
        try:
            self.ws = self.sh.worksheet(self.sheet_name)
        except gspread.WorksheetNotFound:
            self.ws = self.sh.add_worksheet(
                self.sheet_name, 100, len(self.cols), index=0
            )
            self.ws.append_row(self.cols)

    @property
    def data(self):
        return self._data[1:]

    def insert(self, data: list):
        self._data.append(data)
        self.ws.append_row(data)

    @classmethod
    def add_user(cls, email, role="reader"):
        cls.sh.share(email, perm_type="user", role=role)

    @classmethod
    def get_url(cls):
        return cls.sh.url
