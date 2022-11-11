import gspread


gc = gspread.oauth(credentials_filename="credential.json")

gspread.auth.console_flow


def create_sheet(name):
    try:
        return gc.open(name)
    except gspread.SpreadsheetNotFound:
        return gc.create(name)

def add_worksheet(sh: gspread.Spreadsheet, name, cols, index):
    try:
        return sh.worksheet(name)
    except gspread.WorksheetNotFound:
        ws: gspread.Worksheet = sh.add_worksheet(name, 100, len(cols), index=index)
        ws.append_row(cols)
        return ws

def add_user(sh: gspread.Spreadsheet, email, role):
    sh.share(email, perm_type="user", role=role)
