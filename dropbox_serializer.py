import dropbox


class DropboxSerializer:

    def __init__(self, dbx: dropbox.Dropbox):
        self.dbx = dbx

    def upload_file(self, file_location: str, file: str):
        with open(file, "rb") as f:
            self.dbx.files_upload(f.read(), file_location, autorename=True)
