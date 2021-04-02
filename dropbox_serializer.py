import dropbox


class DropboxSerializer:

    def __init__(self, dbx: dropbox.Dropbox):
        self.dbx = dbx

    def upload_file(self, file: str, path: str):
        with open(file, "rb") as f:
            self.dbx.files_upload(f.read(), path, autorename=True)
