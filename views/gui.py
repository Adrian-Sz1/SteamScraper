import PySimpleGUI as sg

# TODO: Instead of setting each of the setting fields as a parameter, perhaps using dependency injection, the config and settings classes could be used allowing for explicit access to the respective classes
def create_window(
        output_folder_path: str,
        output_file_type: str,
        create_sub_folders: bool,
        overwrite_enabled: bool,
        previous_parameters: str,
        steam_api_key: str,
        search_for_options: dict,
        ):
    FONT_NAME = 'calibri'

    FONT_HEADING = (FONT_NAME, 15)
    FONT_OPTION = (FONT_NAME, 11)
    FONT_MULTILINE = (FONT_NAME, 10)

    sg.theme('DarkGrey15')
    sg.DEFAULT_FONT = 'calibri'
    header_layout = [[sg.StatusBar('DISCLAIMER - Steam User Scraper is NOT affiliated with Valve or Steam.', text_color='#c2ffa7')]]
    settings_layout = [[sg.Text('Preferences', font=FONT_HEADING)], [sg.HorizontalSeparator()],
                       [sg.Text('Your Steam API key'), sg.Push(), sg.Input(steam_api_key, key='steam_api_key', enable_events=True, password_char='*'), sg.Button('Show', key='peek_key'), sg.Text('', key='api_key_test_result'), sg.Button('Check Key', key='validate_api_key')],
                       [sg.Text('Output File Type', font=FONT_OPTION), sg.Push(),
                        sg.Combo(['csv', 'json', 'yaml'], readonly=True, default_value=output_file_type, enable_events=True,
                                      key='-OPTION MENU-')],
                       [sg.Text('Output Folder',font=FONT_OPTION), sg.Input(default_text=output_folder_path, key='output_folder_path', enable_events=True),
                        sg.FolderBrowse()], [sg.Checkbox('Create a user sub-folder', key='user_sub_folder', enable_events=True, font=FONT_OPTION,
                                                         default=create_sub_folders,
                                                         tooltip='Each user has their own folder generated which their data is outputted in to')],
                       [sg.Checkbox('Overwrite files with same name', key='overwrite_enabled', enable_events=True,
                                    font=FONT_OPTION,
                                    default=overwrite_enabled)],
                       [sg.Checkbox('Inventory', key='inventory_checkbox', disabled=True, enable_events=True, default=search_for_options['include_inventory'],
                                                         tooltip='Functionality disabled - to be implemented'),
                        sg.Checkbox('Games', key='games_checkbox', enable_events=True, default=search_for_options['include_games']),
                        sg.Checkbox('Friends', key='friends_checkbox', disabled=True, enable_events=True, default=search_for_options['include_friends'],
                                                         tooltip='Functionality disabled - to be implemented'),
                        sg.Checkbox('Reviews', key='reviews_checkbox', disabled=True, enable_events=True, default=search_for_options['include_reviews'],
                                                         tooltip='Functionality disabled - to be implemented'),
                        sg.Checkbox('Profile Comments', key='profile_comments_checkbox', disabled=True, enable_events=True, default=search_for_options['include_profile_comments'],
                                                         tooltip='Functionality disabled - to be implemented')],
                       [sg.Button('Save Preferences', visible=False, key='save_button'), sg.Text('', key='preferences_info_text')],
                       [sg.Frame('Results', [[sg.Multiline('', key='result_output', size=(58, 5), disabled=True)]])]]
    parameters_layout = [[sg.Text('Parameters', font=FONT_HEADING), sg.Push()], [sg.HorizontalSeparator()],
                         [sg.Multiline(default_text=previous_parameters, key='parameters_multiline', font=FONT_MULTILINE, size=(None, 15), ),
                          sg.Push()]]
    footer_layout = [[sg.Button('Start', font=FONT_OPTION), sg.VPush()]]
    window = sg.Window('Steam User Scraper v0.1.0',
                       [header_layout, sg.vtop([sg.Push(), sg.Column(settings_layout), sg.Column(parameters_layout), sg.Push()]),
                        footer_layout], resizable=True)
    return window
