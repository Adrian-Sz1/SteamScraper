import PySimpleGUI as sg
import modules.programsettings as ps
import modules.core as c
import modules.helpers as helpers

def create_window(
        output_folder_path: str,
        output_file_type: str,
        create_sub_folders: bool,
        previous_parameters: str,
        steam_api_key: str,
        search_for_options: dict
        ):
    FONT_NAME = 'calibri'

    FONT_HEADING = (FONT_NAME, 15)
    FONT_OPTION = (FONT_NAME, 11)
    FONT_MULTILINE = (FONT_NAME, 10)

    sg.theme('DarkGrey15')
    sg.DEFAULT_FONT = 'calibri'
    header_layout = [[sg.StatusBar('DISCLAIMER - Steam User Scraper is NOT affiliated with Valve or Steam.', text_color='#c2ffa7')]]
    settings_layout = [[sg.Text('Preferences', font=FONT_HEADING)], [sg.HorizontalSeparator()],
                       [sg.Text('Your Steam API key'), sg.Push(), sg.Input(steam_api_key, key='steam_api_key', enable_events=True), sg.Text('', key='api_key_test_result'), sg.Button('Check Key', key='validate_api_key')],
                       [sg.Text('Output File Type', font=FONT_OPTION), sg.Push(),
                        sg.Combo(['csv', 'json', 'yaml'], readonly=True, default_value=output_file_type, enable_events=True,
                                      key='-OPTION MENU-')],
                       [sg.Text('Output Folder',font=FONT_OPTION), sg.Input(default_text=output_folder_path, key='output_folder_path', enable_events=True),
                        sg.FolderBrowse()], [sg.Checkbox('Create a sub-folder for each user', key='user_sub_folder', enable_events=True, font=FONT_OPTION,
                                                         default=create_sub_folders,
                                                         tooltip='Each user has their own folder generated which their data is outputted in to')],
                       [sg.Checkbox('Inventory', key='inventory_checkbox', enable_events=True, default=search_for_options['include_inventory']),
                        sg.Checkbox('Games', key='games_checkbox', enable_events=True, default=search_for_options['include_games']),
                        sg.Checkbox('Friends', key='friends_checkbox', enable_events=True, default=search_for_options['include_friends']),
                        sg.Checkbox('Reviews', key='reviews_checkbox', enable_events=True, default=search_for_options['include_reviews']),
                        sg.Checkbox('Profile Comments', key='profile_comments_checkbox', enable_events=True, default=search_for_options['include_profile_comments'])],
                       [sg.Button('Save Preferences', visible=False, key='save_button'), sg.Text('', key='preferences_info_text')],
                       [sg.Frame('Results', [[sg.Multiline('', key='result_output', size=(58, 5), disabled=True)]])]]
    parameters_layout = [[sg.Text('Parameters', font=FONT_HEADING), sg.Push()], [sg.HorizontalSeparator()],
                         [sg.Multiline(default_text=previous_parameters, key='parameters_multiline', font=FONT_MULTILINE, size=(None, 15), ),
                          sg.Push()]]
    footer_layout = [[sg.Button('Start', font=FONT_OPTION), sg.VPush()]]
    window = sg.Window('Steam User Scraper v0.1.0',
                       [header_layout, sg.vtop([sg.Push(), sg.Column(settings_layout), sg.Column(parameters_layout), sg.Push()]),
                        footer_layout], resizable=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks exit
            break
        if event == 'save_button':
            file_type = window['-OPTION MENU-'].Get()
            output_folder = window['output_folder_path'].Get()
            user_sub_folder = window['user_sub_folder'].Get()
            current_parameters = window['parameters_multiline'].Get()
            steam_api_key_input = window['steam_api_key'].Get()

            result_output = window['preferences_info_text']
            result_output.Update(text_color='green')
            result_output.Update('Changes saved')

            window['save_button'].Update(visible=False)

            search_options = {
                "include_inventory": window['inventory_checkbox'].Get(),
                "include_games": window['games_checkbox'].Get(),
                "include_friends": window['friends_checkbox'].Get(),
                "include_reviews": window['reviews_checkbox'].Get(),
                "include_profile_comments": window['profile_comments_checkbox'].Get()
            }

            ps.updateSettings(file_type, output_folder, user_sub_folder, current_parameters, steam_api_key_input, search_options)
        elif event in '-OPTION MENU-output_folder_pathuser_sub_folderparameters_multilinesteam_api_keyinventory_checkboxgames_checkboxfriends_checkboxreviews_checkboxprofile_comments_checkbox':
            window['preferences_info_text'].Update(text_color='orange')
            window['preferences_info_text'].Update('Unsaved Changes')
            window['save_button'].Update(visible=True)

        if event == 'Start':
            ps.updateSettingsFileKey('previous_parameters', window['parameters_multiline'].Get())

            gg = c.start(window['steam_api_key'].Get(), window['parameters_multiline'].Get(), window['output_folder_path'].Get(), ps.search_options)

            window['result_output'].Update(value=helpers.parseDictToString(gg))

        if event == 'validate_api_key':
            api_test_result_element = window['api_key_test_result']
            if c.validate_api_key(window['steam_api_key'].Get()):
                api_test_result_element.Update(text_color='green', value='OK')
            else:
                api_test_result_element.Update(text_color='red', value='NOT OK')

    window.close()
