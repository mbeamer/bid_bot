import PySimpleGUI as sg

bids_button_open_text = 'Open Bids'
bids_button_close_text = 'Close Bids'
bids_button_key = 'bids'

bids_list_bids_key = 'binderlist'

status_prefix = 'Status: '
status_started = 'Bid Bot started.'
status_bids_open = 'Bids are open!'
status_bids_closed = 'Bids are closed!'
bids_status_key = 'status'
layout = [
        [sg.ReadButton(bids_button_open_text, key=bids_button_key)],
        [sg.Txt('Bidders')],
        [sg.Listbox(values=('[bidders go here!]', ''), size=(50, 22), key=bids_list_bids_key)],
        [sg.Text('{}{}'.format(status_prefix, status_started), key=bids_status_key)]
        ]

class bid_bot_main():
    ''' Bid Bot main form manager '''
    form = None
    log_parser = None

    def __init__(self, log_parser):
        self.log_parser = log_parser

    def get_bids_box(self):
        return self.form.FindElement(bids_list_bids_key)

    def start_bids(self):
        print("Starting Bids", flush=True)
        self.form.FindElement(bids_list_bids_key).Update(values=())
        self.log_parser.start_monitoring()

    def stop_bids(self):
        print("Stopping Bids", flush=True)
        self.log_parser.end_monitoring = True

    def main_form(self):
        ''' Create and show main_form '''

        bids_open = False
        self.form = sg.Window('Bid Bot').Layout(layout)
        while True:
            button, _values = self.form.Read()
            if button == bids_button_key:
                bids_open = not bids_open
                if bids_open:
                    self.form.FindElement(
                        bids_button_key).Update(text=bids_button_close_text)
                    self.form.FindElement(
                        bids_status_key).Update('{}{}'.format(status_prefix, status_bids_open))
                    self.start_bids()
                else:
                    self.form.FindElement(
                        bids_button_key).Update(text=bids_button_open_text)
                    self.form.FindElement(
                        bids_status_key).Update('{}{}'.format(status_prefix, status_bids_closed))
                    self.stop_bids()
            else:
                self.stop_bids()
                return None
