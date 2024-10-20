from PySide6.QtWidgets import QStatusBar, QLabel


class AppStatusBar(QStatusBar):
    def __init__(self,
                 current_theme:str = 'Light Mode',
                 build_version:str = 'Unknown',
                 repo_url:str = 'https://github.com/Adrian-Sz1/SteamScraper',
                 author_name:str = 'Default Author',
                 parent=None):
        super(AppStatusBar, self).__init__(parent)

        self.current_theme = current_theme
        self.current_build_version = build_version
        self.current_repo_url = repo_url
        self.current_author_name = author_name

        self.theme_label = None
        self.version_label = None
        self.repo_url = None
        self.author_label = None

        self.initialize()

    def initialize(self):
        self.theme_label = QLabel(self.current_theme)
        self.addWidget(self.theme_label)

        self.version_label = QLabel(self.current_build_version)
        self.addWidget(self.version_label, 1)

        self.repo_url = QLabel(self.current_repo_url)
        self.addWidget(self.repo_url, 1)

        self.author_label = QLabel(self.current_author_name)
        self.addWidget(self.author_label, 1)

        self.setSizeGripEnabled(False)


    def get_theme(self) -> str:
        return self.current_theme

    def get_build_version(self) -> str:
        return self.current_build_version

    def get_repo_url(self) -> str:
        return self.current_repo_url

    def get_author_name(self) -> str:
        return self.current_author_name

    def set_theme(self, theme: str):
        self.current_theme = theme
        self.theme_label.setText(theme)